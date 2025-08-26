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
            'T12','T13','T14', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T22']
subjects = ['arithm', 'math', 'ukrmol', 'ukrm','english','IT','biology',
            'history','arts','music','crafts','sport',
            'physics','geo','pravozn', 'chem', 'prirodozn', 'ippoter', 'navch',
            'CSL', 'OPK', 'JS', 'event']
classes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
days = ['Mo', 'Tu', 'We', 'Th', 'Fr']
rooms = ['R1', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R12', 'R13', 'R14']
H = 7
lessons = list(range(1, H+1))

# classes hours of subj
Curriculum = dict()

Curriculum[(1, 'ukrmol')] = 6
Curriculum[(1, 'english')] = 3
Curriculum[(1, 'arithm')] = 6
Curriculum[(1, 'prirodozn')] = 3
Curriculum[(1, 'arts')] = 1
Curriculum[(1, 'music')] = 1
Curriculum[(1, 'crafts')] = 1
Curriculum[(1, 'sport')] = 2
Curriculum[(1, 'OPK')] = 1
Curriculum[(1, 'JS')] = 1
Curriculum[(1, 'ippoter')] = 1
Curriculum[(1, 'navch')] = 4
Curriculum[(1, 'CSL')] = 1

Curriculum[(2, 'ukrmol')] = 7
Curriculum[(2, 'english')] = 3
Curriculum[(2, 'arithm')] = 6
Curriculum[(2, 'arts')] = 1
Curriculum[(2, 'music')] = 1
Curriculum[(2, 'crafts')] = 1
Curriculum[(2, 'sport')] = 3
Curriculum[(2, 'navch')] = 4
Curriculum[(2, 'IT')] = 1
Curriculum[(2, 'prirodozn')] = 3
Curriculum[(2, 'ippoter')] = 1
Curriculum[(2, 'CSL')] = 1
Curriculum[(2, 'OPK')] = 1

Curriculum[(3, 'ukrmol')] = 6
Curriculum[(3, 'english')] = 3
Curriculum[(3, 'arithm')] = 6
Curriculum[(3, 'prirodozn')] = 3
Curriculum[(3, 'arts')] = 2
Curriculum[(3, 'music')] = 1
Curriculum[(3, 'crafts')] = 1
Curriculum[(3, 'sport')] = 2
Curriculum[(3, 'IT')] = 1
Curriculum[(3, 'ippoter')] = 1
Curriculum[(3, 'CSL')] = 1
Curriculum[(3, 'OPK')] = 1

Curriculum[(4, 'ukrmol')] = 7
Curriculum[(4, 'english')] = 3
Curriculum[(4, 'arithm')] = 6
Curriculum[(4, 'arts')] = 1
Curriculum[(4, 'prirodozn')] = 3
Curriculum[(4, 'music')] = 1
Curriculum[(4, 'crafts')] = 1
Curriculum[(4, 'sport')] = 2
Curriculum[(4, 'IT')] = 1
Curriculum[(4, 'ippoter')] = 1
Curriculum[(4, 'CSL')] = 1
Curriculum[(4, 'OPK')] = 1

Curriculum[(5, 'ukrm')] = 6
Curriculum[(5, 'english')] = 3
Curriculum[(5, 'math')] = 6
Curriculum[(5, 'IT')] = 1
Curriculum[(5, 'prirodozn')] = 2
Curriculum[(5, 'arts')] = 1
Curriculum[(5, 'music')] = 1
Curriculum[(5, 'crafts')] = 1
Curriculum[(5, 'sport')] = 2
Curriculum[(5, 'ippoter')] = 1
Curriculum[(5, 'CSL')] = 1
Curriculum[(5, 'OPK')] = 1

Curriculum[(6, 'ukrm')] = 5
Curriculum[(6, 'english')] = 3
Curriculum[(6, 'math')] = 4
Curriculum[(6, 'IT')] = 1
Curriculum[(6, 'biology')] = 2
Curriculum[(6, 'history')] = 2
Curriculum[(6, 'geo')] = 2
Curriculum[(6, 'arts')] = 2
Curriculum[(6, 'music')] = 1
Curriculum[(6, 'crafts')] = 1
Curriculum[(6, 'sport')] = 2
Curriculum[(6, 'ippoter')] = 1
Curriculum[(6, 'JS')] = 1
Curriculum[(6, 'OPK')] = 1

Curriculum[(7, 'ukrm')] = 6
Curriculum[(7, 'english')] = 3
Curriculum[(7, 'math')] = 4
Curriculum[(7, 'IT')] = 1
Curriculum[(7, 'biology')] = 2
Curriculum[(7, 'physics')] = 2
Curriculum[(7, 'history')] = 2
Curriculum[(7, 'geo')] = 2
Curriculum[(7, 'arts')] = 1
Curriculum[(7, 'music')] = 1
Curriculum[(7, 'crafts')] = 1
Curriculum[(7, 'sport')] = 2
Curriculum[(7, 'IT')] = 1
Curriculum[(7, 'JS')] = 1
Curriculum[(7, 'OPK')] = 1
Curriculum[(7, 'ippoter')] = 1

Curriculum[(8, 'ukrm')] = 4
Curriculum[(8, 'english')] = 3
Curriculum[(8, 'math')] = 5
Curriculum[(8, 'biology')] = 2
Curriculum[(8, 'physics')] = 2
Curriculum[(8, 'history')] = 2
Curriculum[(8, 'chem')] = 2
Curriculum[(8, 'geo')] = 2
Curriculum[(8, 'arts')] = 2
Curriculum[(8, 'sport')] = 2
Curriculum[(8, 'IT')] = 2
Curriculum[(8, 'ippoter')] = 1
Curriculum[(8, 'JS')] = 1
Curriculum[(8, 'OPK')] = 1

Curriculum[(9, 'ukrm')] = 4
Curriculum[(9, 'english')] = 3
Curriculum[(9, 'math')] = 6
Curriculum[(9, 'biology')] = 2
Curriculum[(9, 'pravozn')] = 1
Curriculum[(9, 'physics')] = 2
Curriculum[(9, 'history')] = 2
Curriculum[(9, 'chem')] = 2
Curriculum[(9, 'geo')] = 1
Curriculum[(9, 'music')] = 1
Curriculum[(9, 'sport')] = 2
Curriculum[(9, 'IT')] = 2
Curriculum[(9, 'ippoter')] = 1
Curriculum[(9, 'OPK')] = 1


# Approbation (кто какие предметы может вести)
Approbation = {
    ('T1','navch'):1,
    ('T1','prirodozn'):1,
    ('T1','ukrmol'):1,
    ('T1','arithm'):1,
    ('T2', 'navch'):1,
    ('T2','prirodozn'):1,
    ('T2','ukrmol'):1,
    ('T2','arithm'):1,
    ('T3', 'ukrm'):1,
    ('T3','ukrmol'):1,
    ('T3','arithm'):1,
    ('T3','prirodozn'):1,
    ('T3', 'pravozn'):1,
    ('T4', 'music'):1,
    ('T4','arithm'):1,
    ('T4','ukrmol'):1,
    ('T4','prirodozn'):1,
    ('T5', 'CSL'):1,
    ('T6', 'math'):1,
    ('T7', 'arts'):1,
    ('T7', 'JS'):1,
    ('T8', 'OPK'):1,
    ('T8', 'IT'):1,
    ('T8', 'event'):1,
    ('T9', 'sport'):1,
    ('T10', 'IT'):1,
    ('T10', 'sport'):1,
    ('T11', 'ippoter'):1,
    ('T12', 'biology'):1,
    ('T13', 'history'):1,
    ('T14', 'english'):1,
    ('T15', 'chem'):1,
    ('T16', 'crafts'):1,
    ('T17', 'crafts'):1,
    ('T18', 'OPK'):1,
    ('T18', 'JS'):1,
    ('T19', 'physics'):1,
    ('T20', 'ukrm'):1,
    ('T21', 'ippoter'):1,
    ('T22', 'geo'):1,
}


# ------------------------
# PHASE 1: Teacher assignment (Approbation-driven)
# ------------------------
model1 = cp_model.CpModel()

Teaches = {}
for t in teachers:
    for c in classes:
        for s in subjects:
            Teaches[t, c, s] = model1.NewBoolVar(f"Teach[{t},{c},{s}]")

Lessons = {t: model1.NewIntVar(0, 40, f"Lessons[{t}]") for t in teachers}

# связываем нагрузку с предметами по Approbation
for t in teachers:
    total = []
    for c in classes:
        for s in subjects:
            hrs = Curriculum.get((c, s), 0)
            if hrs > 0:
                # event всегда закреплён за T8
                if s == 'event':
                    if t == 'T8':
                        total.append(hrs * Teaches[t, c, s])
                    else:
                        model1.Add(Teaches[t, c, s] == 0)
                # остальные предметы — по Approbation
                elif Approbation.get((t, s), 0) == 1:
                    total.append(hrs * Teaches[t, c, s])
                else:
                    model1.Add(Teaches[t, c, s] == 0)
            else:
                model1.Add(Teaches[t, c, s] == 0)
    # нагрузка
    if total:
        model1.Add(Lessons[t] == sum(total))
    else:
        model1.Add(Lessons[t] == 0)
    model1.Add(Lessons[t] <= 30)

# у каждого (class, subject) ровно один учитель
for c in classes:
    for s in subjects:
        hrs = Curriculum.get((c, s), 0)
        if hrs > 0:
            if s == 'event':
                # только T8
                model1.Add(Teaches['T8', c, s] == 1)
            else:
                possible_teachers = [t for t in teachers if Approbation.get((t, s), 0) == 1]
                if not possible_teachers:
                    raise ValueError(f"❌ Нет учителя для предмета {s} в классе {c}")
                model1.Add(sum(Teaches[t, c, s] for t in possible_teachers) == 1)

# решаем Phase 1
solver1 = cp_model.CpSolver()
solver1.parameters.max_time_in_seconds = 20
status1 = solver1.Solve(model1)

teacher_of = {}
if status1 in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for c in classes:
        for s in subjects:
            for t in teachers:
                if solver1.Value(Teaches[t, c, s]):
                    teacher_of[(c, s)] = t
    print("✅ Phase 1 solved. Teacher assignment ready.")
else:
    print("❌ Phase 1 has no feasible solution.")


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
                    Timetable[c, s, r, d, h] = model2.NewBoolVar(f"TT[{c},{s},{r},{d},{h}]")

# Curriculum adherence (каждый предмет = заданное количество часов)
for c in classes:
    for s in subjects:
        hrs = Curriculum.get((c, s), 0)
        if hrs > 0:
            model2.Add(sum(Timetable[c, s, r, d, h] for r in rooms for d in days for h in lessons) == hrs)

# Ограничение: в понедельник на первом уроке все классы имеют мероприятие в R1
event_subject = 'event'
event_room = 'R1'
for c in classes:
    # Урок event в нужной комнате
    model2.Add(Timetable[c, event_subject, event_room, 'Mo', 1] == 1)
    # Все остальные предметы и комнаты запрещены
    for s in subjects:
        for r in rooms:
            if s != event_subject or r != event_room:
                model2.Add(Timetable[c, s, r, 'Mo', 1] == 0)

# Ограничение: у 6-9 классов OPK вместе и в одном кабинете
opk_room = 'R12'
opk_subject = 'OPK'
slots = [(d, h) for d in days for h in lessons]
opk_slot_bools = []
for d, h in slots:
    bool_var = model2.NewBoolVar(f"opk_slot_{d}_{h}")
    opk_slot_bools.append(bool_var)
    for c in range(6, 10):
        model2.Add(Timetable[c, opk_subject, opk_room, d, h] == 1).OnlyEnforceIf(bool_var)
        for r in rooms:
            if r != opk_room:
                model2.Add(Timetable[c, opk_subject, r, d, h] == 0).OnlyEnforceIf(bool_var)
        for d2, h2 in slots:
            if (d2, h2) != (d, h):
                for r in rooms:
                    model2.Add(Timetable[c, opk_subject, r, d2, h2] == 0).OnlyEnforceIf(bool_var)
model2.Add(sum(opk_slot_bools) == 1)

# Ограничение: один учитель ≤ 1 урок в слот (кроме совместных OPK)
for t in teachers:
    for d in days:
        for h in lessons:
            normal_lessons = []
            for c in classes:
                for s in subjects:
                    if teacher_of.get((c, s)) == t:
                        if not (s == 'OPK' and 6 <= c <= 9):  # OPK общий
                            for r in rooms:
                                normal_lessons.append(Timetable[c, s, r, d, h])
            model2.Add(sum(normal_lessons) <= 1)

# Objective: минимизируем расхождения с Curriculum (подстраховка)
penalties = []
for c in classes:
    for s in subjects:
        hrs = Curriculum.get((c, s), 0)
        if hrs > 0:
            actual = sum(Timetable[c, s, r, d, h] for r in rooms for d in days for h in lessons)
            diff = model2.NewIntVar(-hrs, hrs, f"diff_{c}_{s}")
            abs_diff = model2.NewIntVar(0, hrs, f"abs_diff_{c}_{s}")
            model2.Add(diff == actual - hrs)
            model2.AddAbsEquality(abs_diff, diff)
            penalties.append(abs_diff)
model2.Minimize(sum(penalties))

# Решение Phase 2
solver2 = cp_model.CpSolver()
solver2.parameters.max_time_in_seconds = 180
status2 = solver2.Solve(model2)

# ------------------------
# VISUALIZATION
# ------------------------
def show_timetable(Timetable, classes, subjects, rooms, days, lessons, solver, teacher_of):
    n = len(classes)
    fig, axes = plt.subplots(n // 3 + 1, 3, figsize=(12, 2*n))
    axes = axes.flatten()

    for idx, c in enumerate(classes):
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
                        if solver.Value(Timetable[c, s, r, d, h]):
                            subj = s
                            room = r
                            teacher = teacher_of.get((c, s))
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

if status2 in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("✅ Feasible timetable found")
    show_timetable(Timetable, classes, subjects, rooms, days, lessons, solver2, teacher_of)
else:
    print("❌ No feasible timetable")
