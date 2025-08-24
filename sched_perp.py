import random
import math

# --------------------Pseudocode----------------
# Инициализация
# Создать начальное расписание S (обеспечить отсутствие конфликтов)

# # Функция оценки качества расписания
# Функция Оценить(S):
#     score = 0
#     Для каждого учителя t:
#         score += Вес_окон * Число_пустых_промежутков(t, S)
#         score += Вес_поездок * Кол-во_лишних_поездок(t, S)
#     score += Штраф_за_конфликты(S)
#     Вернуть score

# # Генерация соседних расписаний
# Функция СгенерироватьСоседей(S):
#     Список соседей = []
#     Для нескольких изменений в S:
#         изменить время или аудиторию урока, не нарушая строгих ограничений
#         добавить получившееся расписание в соседей
#     Вернуть соседей

# # Основной цикл (имитация отжига)
# Текущий = S
# Лучший = S
# Лучший_балл = Оценить(S)
# Температура = начальное_значение

# Пока Температура > минимальное_значение:
#     соседи = СгенерироватьСоседей(Текущий)
#     Выбрать S_new из соседей случайно
#     delta = Оценить(S_new) - Оценить(Текущий)

#     Если delta < 0 (улучшение):
#         Текущий = S_new
#         Если Оценить(S_new) < Лучший_балл:
#             Лучший = S_new
#             Лучший_балл = Оценить(S_new)
#     Иначе:
#         С вероятностью exp(-delta / Температура):
#             Текущий = S_new

#     Температура = Температура * коэффициент_охлаждения

# Вернуть Лучший
# ----------------------------------------------

# Пример данных: учителя и их уроки
teachers = {
    "TeacherA": ["Math", "Physics"],
    "TeacherB": ["English", "History"],
}

# Временные слоты (например, 5 уроков в день)
time_slots = [1, 2, 3, 4, 5, 6, 7]

# Расписание: словарь {учитель: {урок: время}}
def create_initial_schedule():
    schedule = {}
    for t, subjects in teachers.items():
        schedule[t] = {}
        available_slots = time_slots[:]
        random.shuffle(available_slots)
        for i, subject in enumerate(subjects):
            schedule[t][subject] = available_slots[i % len(available_slots)]
    return schedule

# Оценка качества расписания
def evaluate(schedule):
    score = 0
    for t, lessons in schedule.items():
        times = sorted(lessons.values())
        # Считаем пустые промежутки между уроками у учителя
        gaps = sum(times[i+1] - times[i] - 1 for i in range(len(times)-1))
        score += gaps
        # Можно добавить дополнительные штрафы за конфликты и т.п.
    return score

# Генерация соседа (случайные изменения в расписании)
def generate_neighbor(schedule):
    new_schedule = {t: lessons.copy() for t, lessons in schedule.items()}
    t = random.choice(list(new_schedule.keys()))
    subject = random.choice(list(new_schedule[t].keys()))
    new_slot = random.choice(time_slots)
    new_schedule[t][subject] = new_slot
    return new_schedule

# Имитация отжига
def simulated_annealing():
    current = create_initial_schedule()
    best = current
    current_score = evaluate(current)
    best_score = current_score
    temperature = 100.0
    cooling_rate = 0.95

    while temperature > 1:
        neighbor = generate_neighbor(current)
        neighbor_score = evaluate(neighbor)
        delta = neighbor_score - current_score
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = neighbor
            current_score = neighbor_score
            if current_score < best_score:
                best = current
                best_score = current_score
        temperature *= cooling_rate

    return best, best_score

# Запуск
final_schedule, final_score = simulated_annealing()
print("Оптимальное расписание:", final_schedule)
print("Качество расписания (чем меньше, тем лучше):", final_score)
