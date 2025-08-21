"""
School Timetable Generator (toy but extensible)
------------------------------------------------
- Solver: OR-Tools CP-SAT
- Scope:
  * Multiple classes
  * Subjects with weekly hour quotas per class
  * Each subject is taught by a single teacher (global, across classes)
  * Optional special rooms per subject (e.g., Lab, Gym, ArtRoom) — unique per timeslot
  * Hard constraints: no clashes for classes, teachers, special rooms; exact weekly hour quotas
  * Soft constraints (can be extended):
      - discourage PE on the 1st period of any day
      - discourage back-to-back same subject within a day

How to run:
  1) pip install ortools
  2) python timetable.py

Adjust the DATA section for your school and rerun.
"""
from ortools.sat.python import cp_model


# ------------------------
# DATA (edit this section)
# ------------------------
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
PERIODS_PER_DAY = 6  # total weekly slots per class = len(DAYS) * PERIODS_PER_DAY

# Classes (homerooms)
CLASSES = ["5A", "5B"]

# Subjects offered (keys are subject codes)
SUBJECTS = ["Math", "Lang", "Science", "PE", "Art"]

# Each subject is taught by a single teacher across all classes
TEACHER_OF = {
    "Math": "T_Math",
    "Lang": "T_Lang",
    "Science": "T_Sci",
    "PE": "T_PE",
    "Art": "T_Art",
}

TEACHERS = sorted(set(TEACHER_OF.values()))

# If a subject needs a special room, name it here; otherwise None
# (generic classrooms are assumed available and not limited)
ROOM_OF = {
    "Math": None,
    "Lang": None,
    "Science": "Lab",
    "PE": "Gym",
    "Art": "ArtRoom",
}

SPECIAL_ROOMS = sorted({r for r in ROOM_OF.values() if r})

# Weekly hour quotas per class & subject (must sum to DAYS*PERIODS_PER_DAY per class)
# Example sums here: 7+7+6+5+5 = 30 = 5 days * 6 periods
REQUIRED_HOURS = {
    "5A": {"Math": 7, "Lang": 7, "Science": 6, "PE": 5, "Art": 5},
    "5B": {"Math": 7, "Lang": 7, "Science": 6, "PE": 5, "Art": 5},
}

# Soft-constraint weights (tune to taste)
W_AVOID_PE_FIRST = 3          # penalty per PE on 1st period of a day
W_AVOID_BACK_TO_BACK = 2      # penalty per adjacent same-subject pair in a day

# ------------------------
# Helper indexing
# ------------------------
SLOTS = list(range(len(DAYS) * PERIODS_PER_DAY))

def slot_of(day_idx: int, period_idx: int) -> int:
    return day_idx * PERIODS_PER_DAY + period_idx

# Map slot -> (day, period)
SLOT_TO_DP = {s: (s // PERIODS_PER_DAY, s % PERIODS_PER_DAY) for s in SLOTS}

# Quick sanity checks on data
for c in CLASSES:
    total_req = sum(REQUIRED_HOURS[c][s] for s in SUBJECTS)
    assert total_req == len(DAYS) * PERIODS_PER_DAY, (
        f"Class {c}: required hours {total_req} must equal {len(DAYS)*PERIODS_PER_DAY}")

# ------------------------
# Model
# ------------------------
model = cp_model.CpModel()

# Decision vars: x[c, s, slot] = 1 if class c has subject s at slot
x = {}
for c in CLASSES:
    for s in SUBJECTS:
        for sl in SLOTS:
            x[(c, s, sl)] = model.NewBoolVar(f"x[{c},{s},{sl}]")

# 1) Each class has exactly 1 subject per slot
for c in CLASSES:
    for sl in SLOTS:
        model.Add(sum(x[(c, s, sl)] for s in SUBJECTS) == 1)

# 2) Weekly hour quotas: for each class & subject
for c in CLASSES:
    for s in SUBJECTS:
        model.Add(sum(x[(c, s, sl)] for sl in SLOTS) == REQUIRED_HOURS[c][s])

# 3) Teacher no double-booking: for each teacher and slot, at most one class
for t in TEACHERS:
    for sl in SLOTS:
        involved_subjects = [s for s in SUBJECTS if TEACHER_OF[s] == t]
        model.Add(
            sum(x[(c, s, sl)] for c in CLASSES for s in involved_subjects) <= 1
        )

# 4) Special room uniqueness per slot (Lab, Gym, etc.)
for r in SPECIAL_ROOMS:
    for sl in SLOTS:
        subs_needing_r = [s for s in SUBJECTS if ROOM_OF[s] == r]
        model.Add(
            sum(x[(c, s, sl)] for c in CLASSES for s in subs_needing_r) <= 1
        )

# ------------------------
# Soft constraints — build a penalty expression
# ------------------------
penalties = []

# 4a) Avoid PE at period 0 (first period) of any day
for c in CLASSES:
    for d, day in enumerate(DAYS):
        sl = slot_of(d, 0)
        penalties.append(W_AVOID_PE_FIRST * x[(c, "PE", sl)])

# 4b) Avoid back-to-back same subject within a day
for c in CLASSES:
    for s in SUBJECTS:
        for d in range(len(DAYS)):
            for p in range(PERIODS_PER_DAY - 1):
                sl1 = slot_of(d, p)
                sl2 = slot_of(d, p + 1)
                both = model.NewBoolVar(f"adj[{c},{s},{d},{p}]")
                # both == 1 iff x(c,s,sl1)=1 and x(c,s,sl2)=1
                model.AddBoolAnd([x[(c, s, sl1)], x[(c, s, sl2)]]).OnlyEnforceIf(both)
                model.AddBoolOr([x[(c, s, sl1)].Not(), x[(c, s, sl2)].Not()]).OnlyEnforceIf(both.Not())
                penalties.append(W_AVOID_BACK_TO_BACK * both)

# Objective: minimize total penalties
model.Minimize(sum(penalties))

# ------------------------
# Solve
# ------------------------
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 20.0  # adjust as needed
solver.parameters.num_search_workers = 8

result = solver.Solve(model)

status_map = {
    cp_model.OPTIMAL: "OPTIMAL",
    cp_model.FEASIBLE: "FEASIBLE",
    cp_model.INFEASIBLE: "INFEASIBLE",
    cp_model.MODEL_INVALID: "MODEL_INVALID",
    cp_model.UNKNOWN: "UNKNOWN",
}
print(f"Status: {status_map.get(result, 'UNKNOWN')}")
print(f"Objective (penalty): {int(solver.ObjectiveValue())}")

# ------------------------
# Pretty print per class
# ------------------------
if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for c in CLASSES:
        print("\n=== Timetable for class:", c, "===")
        # Build a grid days x periods
        grid = [[None for _ in range(PERIODS_PER_DAY)] for _ in range(len(DAYS))]
        for sl in SLOTS:
            d, p = SLOT_TO_DP[sl]
            for s in SUBJECTS:
                if solver.Value(x[(c, s, sl)]) == 1:
                    grid[d][p] = s
                    break
        # Print header
        print("       " + "  ".join(f"P{p+1}" for p in range(PERIODS_PER_DAY)))
        for d, day in enumerate(DAYS):
            row = "  ".join(f"{grid[d][p]:<7}" for p in range(PERIODS_PER_DAY))
            print(f"{day:<3} | {row}")

    # Teacher load sanity table per slot (optional)
    print("\nTeacher load check (sum per slot should be <= 1 per teacher):")
    for t in TEACHERS:
        line = []
        for sl in SLOTS:
            cnt = 0
            for c in CLASSES:
                for s in SUBJECTS:
                    if TEACHER_OF[s] == t and solver.Value(x[(c, s, sl)]) == 1:
                        cnt += 1
            line.append(str(cnt))
        print(f"{t:<7} : ", " ".join(line))
else:
    print("No feasible timetable found. Try relaxing hour quotas or changing data.")

# ------------------------
# Extension tips:
# ------------------------
# - Per-teacher unavailable slots: For each (t, sl) add constraint sum_{c,s:teacher(s)=t} x[c,s,sl] == 0
# - Per-class forbidden subjects at certain periods: x[c, subj, sl] == 0
# - Max N lessons per day for a class/teacher: sum over periods in day <= N
# - Subject spreading across days: enforce minimum days between lessons using additional boolean linking
# - Different teachers per class+subject: replace TEACHER_OF with TEACHER_OF[(c,s)] mapping
# - Multiple parallel classes per subject (e.g., groups): split the class entity accordingly
