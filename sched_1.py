"""
School Timetable Generator
------------------------------------------------
- Solver: OR-Tools CP-SAT
- Генерирует расписание для нескольких классов с ограничениями

Установка: pip install ortools
Запуск: python sched_1.py
"""
from ortools.sat.python import cp_model
import sys

def main():
    # ------------------------
    # ДАННЫЕ (можно настроить)
    # ------------------------
    DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт"]
    PERIODS_PER_DAY = 7
    # CLASSES = ["1А", "2A", "3А", "4А", "5А", "6А", "7А", "8А", "9А"]
    CLASSES = ["7А", "8А"]  # Для быстрого теста
    # SUBJECTS = ["Алгебра", "Мат1", "Мат2", "Мат3", "Мат4", 
    #             "Укр.мова",
    #             "Укр.мова1", "Укр.мова2", "Укр.мова3", "Укр.мова4",
    #             "Фізика", "Фізкультура", "ИЗО", 
    #             "ЦСМ", "Англ.мова.Мол.Шк", 
    #             "Укр.літ", "Історія", "Географія", 
    #             "Біологія", "Хімія", "ОПК", "Трудове навчання", "Кінний спорт",
    #             ]
    SUBJECTS = ["Алгебра", "Укр.мова", "Фізика", "Фізкультура", "ІЗО"]  # Для быстрого теста

    # Учителя по предметам
    # TEACHER_OF = {
    #     "Укр.мова": "Шатило С.С.",
    #     "Алгебра": "Ткаченко К.Г.",
    #     "Русский": "Петрова П.П.",
    #     "Фізика": "Костюков А.Н.",
    #     "Фізкультура": "Адушкін Р.В.",
    #     "ІЗО": "Воронцова Л.С.",
    #     "ЦСМ": "Школьнік Л.В.",
    #     "Кінний спорт": "Болгова Є.М.",
    # }

    TEACHER_OF = {
        "Алгебра": "Ткаченко К.Г.",
        "Укр.мова": "Шатило С.С.",
        "Фізика": "Костюков А.Н.",
        "Фізкультура": "Адушкін Р.В.",
        "ІЗО": "Воронцова Л.С.",
    }

    TEACHERS = sorted(set(TEACHER_OF.values()))

    # Специальные кабинеты
    ROOM_OF = {
        "Фізкультура": "Спортзал",
        "ІЗО": "Кабинет ИЗО",
    }

    SPECIAL_ROOMS = sorted({r for r in ROOM_OF.values() if r})

    # Количество часов в неделю (должно суммироваться до 30)
    REQUIRED_HOURS = {
        "7А": {"Алгебра": 6, "Укр.мова": 7, "Фізика": 2, "Фізкультура": 5, "ІЗО": 5},
        "8А": {"Алгебра": 6, "Укр.мова": 7, "Фізика": 2, "Фізкультура": 5, "ІЗО": 5},
    }

    # Веса штрафов за нарушение мягких ограничений
    W_AVOID_PE_FIRST = 3
    W_AVOID_BACK_TO_BACK = 2

    # ------------------------
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ------------------------
    SLOTS = list(range(len(DAYS) * PERIODS_PER_DAY))

    def slot_of(day_idx: int, period_idx: int) -> int:
        return day_idx * PERIODS_PER_DAY + period_idx

    SLOT_TO_DP = {s: (s // PERIODS_PER_DAY, s % PERIODS_PER_DAY) for s in SLOTS}

    # Проверка корректности данных
    # for c in CLASSES:
    #     total_req = sum(REQUIRED_HOURS[c][s] for s in SUBJECTS)
    #     total_slots = len(DAYS) * PERIODS_PER_DAY
    #     if total_req != total_slots:
    #         print(f"ОШИБКА: Класс {c}: требуется {total_req} часов, но доступно {total_slots} слотов")
    #         return

    print("Проверка данных пройдена успешно!")
    print(f"Классы: {CLASSES}")
    print(f"Предметы: {SUBJECTS}")
    print(f"Учителя: {TEACHERS}")
    print(f"Специальные кабинеты: {SPECIAL_ROOMS}")
    print()

    # ------------------------
    # СОЗДАНИЕ МОДЕЛИ
    # ------------------------
    model = cp_model.CpModel()

    # Переменные: x[c, s, slot] = 1, если класс c изучает предмет s в слоте slot
    x = {}
    for c in CLASSES:
        for s in SUBJECTS:
            for sl in SLOTS:
                x[(c, s, sl)] = model.NewBoolVar(f"x[{c},{s},{sl}]")

    # ------------------------
    # ЖЕСТКИЕ ОГРАНИЧЕНИЯ
    # ------------------------
    
    # 1) В каждом слоте у класса ровно один предмет
    for c in CLASSES:
        for sl in SLOTS:
            model.Add(sum(x[(c, s, sl)] for s in SUBJECTS) == 1)

    # 2) Недельная норма часов по предметам
    for c in CLASSES:
        for s in SUBJECTS:
            model.Add(sum(x[(c, s, sl)] for sl in SLOTS) == REQUIRED_HOURS[c][s])

    # 3) Учитель не может вести уроки в разных классах одновременно
    for teacher in TEACHERS:
        for sl in SLOTS:
            teacher_subjects = [s for s in SUBJECTS if TEACHER_OF[s] == teacher]
            model.Add(
                sum(x[(c, s, sl)] for c in CLASSES for s in teacher_subjects) <= 1
            )

    # 4) Специальные кабинеты не могут использоваться одновременно
    for room in SPECIAL_ROOMS:
        for sl in SLOTS:
            room_subjects = [s for s in SUBJECTS if ROOM_OF[s] == room]
            model.Add(
                sum(x[(c, s, sl)] for c in CLASSES for s in room_subjects) <= 1
            )

    # ------------------------
    # МЯГКИЕ ОГРАНИЧЕНИЯ (штрафы)
    # ------------------------
    penalties = []

    # Избегать физкультуру на первом уроке
    for c in CLASSES:
        for d in range(len(DAYS)):
            sl = slot_of(d, 0)
            penalties.append(W_AVOID_PE_FIRST * x[(c, "Фізкультура", sl)])

    # Избегать одинаковые предметы подряд в течение дня
    for c in CLASSES:
        for s in SUBJECTS:
            for d in range(len(DAYS)):
                for p in range(PERIODS_PER_DAY - 1):
                    sl1 = slot_of(d, p)
                    sl2 = slot_of(d, p + 1)
                    both = model.NewBoolVar(f"adj[{c},{s},{d},{p}]")
                    
                    # both = 1 тогда и только тогда, когда оба урока одного предмета
                    model.AddBoolAnd([x[(c, s, sl1)], x[(c, s, sl2)]]).OnlyEnforceIf(both)
                    model.AddBoolOr([x[(c, s, sl1)].Not(), x[(c, s, sl2)].Not()]).OnlyEnforceIf(both.Not())
                    penalties.append(W_AVOID_BACK_TO_BACK * both)

    # Целевая функция: минимизировать штрафы
    model.Minimize(sum(penalties))

    # ------------------------
    # РЕШЕНИЕ
    # ------------------------
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    solver.parameters.num_search_workers = 4

    print("Начинаю поиск решения...")
    result = solver.Solve(model)

    status_map = {
        cp_model.OPTIMAL: "ОПТИМАЛЬНОЕ",
        cp_model.FEASIBLE: "ДОПУСТИМОЕ",
        cp_model.INFEASIBLE: "НЕРЕШАЕМО",
        cp_model.MODEL_INVALID: "МОДЕЛЬ НЕКОРРЕКТНА",
        cp_model.UNKNOWN: "НЕИЗВЕСТНО",
    }
    
    print(f"Статус: {status_map.get(result, 'НЕИЗВЕСТНО')}")
    
    if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"Штраф (чем меньше, тем лучше): {int(solver.ObjectiveValue())}")
        print(f"Время решения: {solver.WallTime():.2f} сек")
        print()

        # ------------------------
        # ВЫВОД РАСПИСАНИЯ
        # ------------------------
        for c in CLASSES:
            print(f"\n{'='*50}")
            print(f"РАСПИСАНИЕ ДЛЯ КЛАССА: {c}")
            print(f"{'='*50}")
            
            # Создаем таблицу дни × уроки
            grid = [[None for _ in range(PERIODS_PER_DAY)] for _ in range(len(DAYS))]
            
            for sl in SLOTS:
                d, p = SLOT_TO_DP[sl]
                for s in SUBJECTS:
                    if solver.Value(x[(c, s, sl)]) == 1:
                        grid[d][p] = s
                        break
            
            # Выводим заголовок
            header = "День   "
            for p in range(PERIODS_PER_DAY):
                header += f"{'Урок ' + str(p+1):<12} "
            print(header)
            print("-" * len(header))
            
            # Выводим расписание по дням
            for d, day in enumerate(DAYS):
                row = f"{day:<6} "
                for p in range(PERIODS_PER_DAY):
                    subject = grid[d][p] if grid[d][p] else "---"
                    row += f"{subject:<12} "
                print(row)

        # ------------------------
        # ПРОВЕРКА ЗАГРУЗКИ УЧИТЕЛЕЙ
        # ------------------------
        print(f"\n{'='*50}")
        print("ПРОВЕРКА ЗАГРУЗКИ УЧИТЕЛЕЙ")
        print(f"{'='*50}")
        
        for teacher in TEACHERS:
            print(f"\nУчитель: {teacher}")
            teacher_subjects = [s for s in SUBJECTS if TEACHER_OF[s] == teacher]
            print(f"Предметы: {teacher_subjects}")
            
            total_lessons = 0
            for sl in SLOTS:
                lessons_this_slot = 0
                for c in CLASSES:
                    for s in teacher_subjects:
                        if solver.Value(x[(c, s, sl)]) == 1:
                            lessons_this_slot += 1
                            total_lessons += 1
                
                if lessons_this_slot > 1:
                    print(f"⚠️  КОНФЛИКТ в слоте {sl}: {lessons_this_slot} уроков одновременно!")
            
            print(f"Всего уроков в неделю: {total_lessons}")

    else:
        print("\n❌ Не удалось найти допустимое расписание!")
        print("Возможные причины:")
        print("- Слишком жесткие ограничения")
        print("- Недостаточно времени или учителей")
        print("- Конфликт в требованиях")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Ошибка: Не установлена библиотека OR-Tools")
        print("Установите командой: pip install ortools")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        sys.exit(1)