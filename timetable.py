"""
Final School Timetabling with OR-Tools CP-SAT
---------------------------------------------
This script unifies Phase 1 (teacher assignment) and Phase 2 (timetable building).
"""
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt

# ------------------------
# DATA
# ------------------------
teachers = ['T1','T2','T3','T4','T5','T6','T7', 'T8', 'T9', 'T10', 'T11',
            'T12','T13','T14']
subjects = ['math','czech','english','IT','science','biology',
            'history','arts','music','crafts','sport',
            'health','physics','geo','civics', 'chem',
            'elect','prof','german']
classes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
days = ['Mo', 'Tu', 'We', 'Th', 'Fr']
rooms = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11']
H = 7
lessons = list(range(1,H+1))
lunch_lessons = [5, 6, 7]
lunch_limit = 3

# Curriculum (⚠️ сюда нужно вставить все данные из твоего sem.py)
# Curriculum = {
#     (1,'czech'):7, (1,'english'):2, (1,'math'):4, (1,'science'):2,
#     (1,'arts'):2, (1,'music'):1, (1,'crafts'):1, (1,'sport'):2,
#     # ... и так далее для всех классов
# }

Curriculum = dict()

Curriculum[(1, 'czech')] = 7
Curriculum[(1, 'english')] = 2
Curriculum[(1, 'math')] = 4
Curriculum[(1, 'science')] = 2
Curriculum[(1, 'arts')] = 2
Curriculum[(1, 'music')] = 1
Curriculum[(1, 'crafts')] = 1
Curriculum[(1, 'sport')] = 2

Curriculum[(2, 'czech')] = 7
Curriculum[(2, 'english')] = 2
Curriculum[(2, 'math')] = 5
Curriculum[(2, 'science')] = 2
Curriculum[(2, 'arts')] = 1
Curriculum[(2, 'music')] = 1
Curriculum[(2, 'crafts')] = 1
Curriculum[(2, 'sport')] = 3

Curriculum[(3, 'czech')] = 7
Curriculum[(3, 'english')] = 3
Curriculum[(3, 'math')] = 5
Curriculum[(3, 'science')] = 3
Curriculum[(3, 'arts')] = 2
Curriculum[(3, 'music')] = 1
Curriculum[(3, 'crafts')] = 1
Curriculum[(3, 'sport')] = 2

Curriculum[(4, 'czech')] = 7
Curriculum[(4, 'english')] = 3
Curriculum[(4, 'math')] = 5
Curriculum[(4, 'biology')] = 2
Curriculum[(4, 'history')] = 2
Curriculum[(4, 'arts')] = 1
Curriculum[(4, 'music')] = 1
Curriculum[(4, 'crafts')] = 1
Curriculum[(4, 'sport')] = 2
Curriculum[(4, 'IT')] = 1

Curriculum[(5, 'czech')] = 8
Curriculum[(5, 'english')] = 3
Curriculum[(5, 'math')] = 5
Curriculum[(5, 'IT')] = 1
Curriculum[(5, 'biology')] = 2
Curriculum[(5, 'history')] = 2
Curriculum[(5, 'arts')] = 1
Curriculum[(5, 'music')] = 1
Curriculum[(5, 'crafts')] = 1
Curriculum[(5, 'sport')] = 2

Curriculum[(6, 'czech')] = 4
Curriculum[(6, 'english')] = 3
Curriculum[(6, 'math')] = 4
Curriculum[(6, 'IT')] = 1
Curriculum[(6, 'biology')] = 2
Curriculum[(6, 'civics')] = 2
Curriculum[(6, 'physics')] = 2
Curriculum[(6, 'history')] = 2
Curriculum[(6, 'geo')] = 2
Curriculum[(6, 'arts')] = 2
Curriculum[(6, 'music')] = 1
Curriculum[(6, 'crafts')] = 1
Curriculum[(6, 'sport')] = 2
Curriculum[(6, 'health')] = 1

Curriculum[(7, 'czech')] = 5
Curriculum[(7, 'english')] = 3
Curriculum[(7, 'math')] = 4
Curriculum[(7, 'IT')] = 1
Curriculum[(7, 'biology')] = 2
Curriculum[(7, 'civics')] = 2
Curriculum[(7, 'physics')] = 2
Curriculum[(7, 'history')] = 2
Curriculum[(7, 'geo')] = 2
Curriculum[(7, 'arts')] = 2
Curriculum[(7, 'music')] = 1
Curriculum[(7, 'crafts')] = 1
Curriculum[(7, 'sport')] = 2
Curriculum[(7, 'health')] = 1
Curriculum[(7, 'IT')] = 1

Curriculum[(8, 'czech')] = 4
Curriculum[(8, 'english')] = 3
Curriculum[(8, 'german')] = 3
Curriculum[(8, 'math')] = 5
Curriculum[(8, 'biology')] = 1
Curriculum[(8, 'civics')] = 1
Curriculum[(8, 'physics')] = 2
Curriculum[(8, 'history')] = 2
Curriculum[(8, 'chem')] = 2
Curriculum[(8, 'geo')] = 2
Curriculum[(8, 'arts')] = 2
Curriculum[(8, 'sport')] = 2
Curriculum[(8, 'health')] = 1
Curriculum[(8, 'IT')] = 1

Curriculum[(9, 'czech')] = 4
Curriculum[(9, 'english')] = 3
Curriculum[(9, 'german')] = 3
Curriculum[(9, 'math')] = 4
Curriculum[(9, 'biology')] = 2
Curriculum[(9, 'civics')] = 1
Curriculum[(9, 'physics')] = 2
Curriculum[(9, 'history')] = 2
Curriculum[(9, 'chem')] = 2
Curriculum[(9, 'geo')] = 0
Curriculum[(9, 'arts')] = 1
Curriculum[(9, 'music')] = 1
Curriculum[(9, 'sport')] = 2
Curriculum[(9, 'elect')] = 2
Curriculum[(9, 'prof')] = 1


# Approbation (кто какие предметы может вести)
Approbation = {
    ('T5','physics'):1, ('T5','chem'):1, ('T5','elect'):1, ('T5','math'):1,
    ('T6','geo'):1, ('T6','biology'):1,
    ('T7','english'):1, ('T7','czech'):1,
    ('T8','math'):1, ('T8','civics'):1,
    ('T9','music'):1, ('T9','english'):1,
    ('T10','history'):1, ('T10','civics'):1,
    ('T11','czech'):1,
    ('T12','czech'):1, ('T12','german'):1,
    ('T13','arts'):1, ('T13','crafts'):1, ('T13','elect'):1, ('T13','prof'):1,
    ('T14','IT'):1, ('T14','sport'):1, ('T14','health'):1,
}

# ------------------------
# PHASE 1: Teacher assignment
# ------------------------
model1 = cp_model.CpModel()

Teaches = {}
for t in teachers:
    for c in classes:
        for s in subjects:
            Teaches[t,c,s] = model1.NewBoolVar(f"Teach[{t},{c},{s}]")

Lessons = {t:model1.NewIntVar(0,30,f"Lessons[{t}]") for t in teachers}

# First 4 teachers are fixed to first 4 classes (except english)
pairings = list(zip(teachers[:4], classes[:4]))
for t,c in pairings:
    for s in subjects:
        if s != 'english' and Curriculum.get((c,s),0) > 0:
            model1.Add(Teaches[t,c,s] == 1)
    for c2 in classes:
        if c2 != c:
            for s in subjects:
                model1.Add(Teaches[t,c2,s] == 0)
    hours = sum(Curriculum.get((c,s),0) for s in subjects if s != 'english')
    model1.Add(Lessons[t] == hours)

# Other teachers by approbation
for t in teachers[4:]:
    total = []
    for c in classes:
        for s in subjects:
            hrs = Curriculum.get((c,s),0)
            if hrs > 0:
                total.append(hrs * Teaches[t,c,s])
            if Approbation.get((t,s),0) == 0:
                model1.Add(Teaches[t,c,s] == 0)
    if total:
        model1.Add(Lessons[t] == sum(total))
    model1.Add(Lessons[t] <= 22)
    model1.Add(Lessons[t] >= 14)

for c in classes:
    for s in subjects:
        if Curriculum.get((c,s),0) > 0:
            model1.Add(sum(Teaches[t,c,s] for t in teachers) == 1)

solver1 = cp_model.CpSolver()
solver1.parameters.max_time_in_seconds = 20
solver1.Solve(model1)

# Store assignment result in dict teacher_of[(c,s)]
teacher_of = {}
for c in classes:
    for s in subjects:
        for t in teachers:
            if solver1.Value(Teaches[t,c,s]):
                teacher_of[(c,s)] = t

# ------------------------
# PHASE 2: Timetable
# ------------------------
model2 = cp_model.CpModel()

Timetable = {}
for c in classes:
    for s in subjects:
        for r in rooms:
            for d in days:
                for h in lessons:
                    Timetable[c,s,r,d,h] = model2.NewBoolVar(f"TT[{c},{s},{r},{d},{h}]")

# Curriculum adherence
for c in classes:
    for s in subjects:
        hrs = Curriculum.get((c,s),0)
        if hrs > 0:
            model2.Add(sum(Timetable[c,s,r,d,h] for r in rooms for d in days for h in lessons) == hrs)

# Each class ≤1 lesson per slot
for c in classes:
    for d in days:
        for h in lessons:
            model2.Add(sum(Timetable[c,s,r,d,h] for s in subjects for r in rooms) <= 1)

# Each room ≤1 lesson per slot
for r in rooms:
    for d in days:
        for h in lessons:
            model2.Add(sum(Timetable[c,s,r,d,h] for c in classes for s in subjects) <= 1)

# Teacher conflict: no double booking
for t in teachers:
    for d in days:
        for h in lessons:
            model2.Add(sum(Timetable[c,s,r,d,h] for c in classes for s in subjects if teacher_of.get((c,s))==t for r in rooms) <= 1)

# Room-specific constraints
for r in rooms:
    if r != 'R1':
        for d in days:
            for h in lessons:
                model2.Add(sum(Timetable[c,'music',r,d,h] for c in classes) == 0)
    if r != 'R2':
        for d in days:
            for h in lessons:
                model2.Add(sum(Timetable[c,'chem',r,d,h] for c in classes) == 0)

# Objective: minimize later lessons
penalties = []
for c in classes:
    for s in subjects:
        for r in rooms:
            for d in days:
                for h in lessons:
                    penalties.append(h * Timetable[c,s,r,d,h])
model2.Minimize(sum(penalties))

solver2 = cp_model.CpSolver()
solver2.parameters.max_time_in_seconds = 30
status = solver2.Solve(model2)

# ------------------------
# VISUALIZATION
# ------------------------
def show_timetable(Timetable, classes, subjects, rooms, days, lessons, solver, teacher_of):
    n = len(classes)
    fig, axes = plt.subplots(n // 3 + 1, 3, figsize=(12, 2*n))
    axes = axes.flatten()

    for idx,c in enumerate(classes):
        ax = axes[idx]
        ax.set_title(f"Class {c}")
        y = H
        for d in days:
            for h in lessons:
                subj = None
                room = None
                teacher = None
                for s in subjects:
                    for r in rooms:
                        if solver.Value(Timetable[c,s,r,d,h]):
                            subj = s
                            room = r
                            teacher = teacher_of.get((c,s))
                if subj:
                    txt = f"{subj}\n{room}\n{teacher}"
                    ax.text(h, y, txt, ha='center', va='center', fontsize=6,
                            bbox=dict(facecolor='lightgrey', alpha=0.5))
            ax.text(0, y+0.3, d, fontsize=8, ha='right')
            y -= 1
        ax.set_xlim(0, len(lessons)+1)
        ax.set_ylim(0, H+1)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("Feasible timetable found")
    show_timetable(Timetable, classes, subjects, rooms, days, lessons, solver2, teacher_of)
else:
    print("No feasible timetable")
