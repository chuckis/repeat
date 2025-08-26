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
            'T12','T13','T14', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21']
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

Curriculum[(3, 'ukrmol')] = 7
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
    ('T1','ukrmol'):1,
    ('T1','arithm'):1,
    ('T2', 'navch'):1,
    ('T2','ukrmol'):1,
    ('T2','arithm'):1,
    ('T3', 'ukrm'):1,
    ('T3','ukrmol'):1,
    ('T3','arithm'):1,
    ('T3', 'pravozn'):1,
    ('T4', 'music'):1,
    ('T4','arithm'):1,
    ('T4','ukrmol'):1,
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
    ('T21', 'ippoter'):1
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

print(Teaches)

Lessons = {t:model1.NewIntVar(0,30,f"Lessons[{t}]") for t in teachers}
# print(Lessons)

# First 4 teachers are fixed to first 4 classes (except english)
#  TODO: у нас еще есть музыка и укрм. and explain
# pairings = list(zip(teachers[:4], classes[:4]))
# for t,c in pairings:
#     for s in subjects:
#         if s != 'english' and Curriculum.get((c,s),0) > 0:
#             model1.Add(Teaches[t,c,s] == 1)
#     for c2 in classes:
#         if c2 != c:
#             for s in subjects:
#                 model1.Add(Teaches[t,c2,s] == 0)
#     hours = sum(Curriculum.get((c,s),0) for s in subjects if s != 'english')
#     model1.Add(Lessons[t] == hours)

# Other or maybe ALL(?) teachers by approbation
for t in teachers:
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
    model1.Add(Lessons[t] <= 25)
    # model1.Add(Lessons[t] >= 14)

# TODO: explain
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

print(teacher_of)

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
# for c in classes:
#     for d in days:
#         for h in lessons:
#             model2.Add(sum(Timetable[c,s,r,d,h] for s in subjects for r in rooms) <= 1)

# Ограничение: в понедельник на первом уроке все классы имеют мероприятие в одном кабинете
event_subject = 'event'
event_room = 'R1'
for c in classes:
    # Только мероприятие в нужной комнате
    model2.Add(Timetable[c, event_subject, event_room, 'Mo', 1] == 1)
    # Все остальные предметы и комнаты запрещены
    for s in subjects:
        for r in rooms:
            if s != event_subject or r != event_room:
                model2.Add(Timetable[c, s, r, 'Mo', 1] == 0)

# Ограничение: у 6-9 классов урок OPK одновременно и вместе
opk_room = 'R12'
opk_subject = 'OPK'

# Для каждого слота создаём булеву переменную, которая означает "OPK для всех классов в этом слоте"
opk_slot_bools = []
slots = [(d, h) for d in days for h in lessons]
for idx, (d, h) in enumerate(slots):
    bool_var = model2.NewBoolVar(f"opk_slot_{d}_{h}")
    opk_slot_bools.append(bool_var)
    # Если выбран этот слот, то OPK у всех классов 6-9 в этом кабинете
    for c in range(6, 10):
        model2.Add(Timetable[c, opk_subject, opk_room, d, h] == 1).OnlyEnforceIf(bool_var)
        # Запретить OPK в других кабинетах в этом слоте
        for r in rooms:
            if r != opk_room:
                model2.Add(Timetable[c, opk_subject, r, d, h] == 0).OnlyEnforceIf(bool_var)
        # Запретить OPK в других слотах
        for d2, h2 in slots:
            if (d2, h2) != (d, h):
                for r in rooms:
                    model2.Add(Timetable[c, opk_subject, r, d2, h2] == 0).OnlyEnforceIf(bool_var)

# Только один слот выбран для совместного OPK
model2.Add(sum(opk_slot_bools) == 1)

# # Если нужен конкретный день/урок, например, четверг, 3-й урок:
# for c in range(6, 10):
#     for r in rooms:
#         if r == opk_room:
#             model2.Add(Timetable[c, opk_subject, r, 'Th', 3] == 1)
#         else:
#             model2.Add(Timetable[c, opk_subject, r, 'Th', 3] == 0)
#     # Запретить OPK в другие слоты
#     for d in days:
#         for h in lessons:
#             if (d, h) != ('Th', 3):
#                 for r in rooms:
#                     model2.Add(Timetable[c, opk_subject, r, d, h] == 0)

# Each room ≤1 lesson per slot
# for r in rooms:
#     for d in days:
#         for h in lessons:
#             model2.Add(sum(Timetable[c,s,r,d,h] for c in classes for s in subjects) <= 1)


# Если предмет совместный (например, OPK), то допускается несколько классов одновременно.
# Для остальных предметов — не более одного урока.
for t in teachers:
    for d in days:
        for h in lessons:
            # Считаем количество обычных уроков
            normal_lessons = []
            for c in classes:
                for s in subjects:
                    if teacher_of.get((c,s)) == t:
                        # Если это не совместный OPK
                        if not (s == 'OPK' and 6 <= c <= 9):
                            for r in rooms:
                                normal_lessons.append(Timetable[c,s,r,d,h])
            model2.Add(sum(normal_lessons) <= 1)

# # Room-specific constraints
# for r in rooms:
#     if r != 'R14':
#         for d in days:
#             for h in lessons:
#                 model2.Add(sum(Timetable[c,'IT',r,d,h] for c in classes) == 0)
#     if r != 'R13':
#         for d in days:
#             for h in lessons:
#                 model2.Add(sum(Timetable[c,'chem',r,d,h] for c in classes) == 0)

# Objective: minimize later lessons
penalties = []
# for c in classes:
#     for s in subjects:
#         for r in rooms:
#             for d in days:
#                 for h in lessons:
#                     penalties.append(h * Timetable[c,s,r,d,h])
# model2.Minimize(sum(penalties))

for c in classes:
    for s in subjects:
        hrs = Curriculum.get((c,s),0)
        if hrs > 0:
            actual = sum(Timetable[c,s,r,d,h] for r in rooms for d in days for h in lessons)
            diff = model2.NewIntVar(-hrs, hrs, f"diff_{c}_{s}")
            abs_diff = model2.NewIntVar(0, hrs, f"abs_diff_{c}_{s}")
            model2.Add(diff == actual - hrs)
            model2.AddAbsEquality(abs_diff, diff)
            penalties.append(abs_diff)
# ...
model2.Minimize(sum(penalties))

solver2 = cp_model.CpSolver()
solver2.parameters.max_time_in_seconds = 180
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
