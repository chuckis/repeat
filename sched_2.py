"""
Упрощенный генератор расписания для диагностики проблем
Без мягких ограничений - только основные
"""
from ortools.sat.python import cp_model
import time

def create_simple_timetable():
    print("=== УПРОЩЕННЫЙ ГЕНЕРАТОР РАСПИСАНИЯ ===")
    
    # Простейшие данные
    DAYS = ["Пон", "Вто", "Сре", "Чет", "Пят"] 
    PERIODS_PER_DAY = 6
    CLASSES = ["5А", "5Б"]
    SUBJECTS = ["Математика", "Русский", "Физика", "Физкультура", "ИЗО"]
    
    # Учителя - один на предмет
    TEACHER_OF = {
        "Математика": "Учитель1",
        "Русский": "Учитель2", 
        "Физика": "Учитель3",
        "Физкультура": "Учитель4",
        "ИЗО": "Учитель5"
    }
    
    # Часы в неделю
    REQUIRED_HOURS = {
        "5А": {"Математика": 7, "Русский": 7, "Физика": 6, "Физкультура": 5, "ИЗО": 5},
        "5Б": {"Математика": 7, "Русский": 7, "Физика": 6, "Физкультура": 5, "ИЗО": 5}
    }
    
    TOTAL_SLOTS = len(DAYS) * PERIODS_PER_DAY
    SLOTS = list(range(TOTAL_SLOTS))
    
    print(f"Дни: {DAYS}")
    print(f"Уроков в день: {PERIODS_PER_DAY}")
    print(f"Всего слотов на класс: {TOTAL_SLOTS}")
    
    # Проверка данных
    for cls in CLASSES:
        total = sum(REQUIRED_HOURS[cls].values())
        print(f"Класс {cls}: требуется {total} часов")
        if total != TOTAL_SLOTS:
            print(f"ОШИБКА: {cls} нужно {total}, а слотов {TOTAL_SLOTS}")
            return False
    
    print("✓ Данные корректны")
    
    # Создание модели
    print("\nСоздание модели...")
    model = cp_model.CpModel()
    
    # Переменные: x[класс, предмет, слот]
    x = {}
    for c in CLASSES:
        for s in SUBJECTS:
            for slot in SLOTS:
                x[(c, s, slot)] = model.NewBoolVar(f"x_{c}_{s}_{slot}")
    
    print(f"Создано переменных: {len(x)}")
    
    # Ограничение 1: в каждом слоте класс изучает ровно 1 предмет
    constraint_count = 0
    for c in CLASSES:
        for slot in SLOTS:
            model.Add(sum(x[(c, s, slot)] for s in SUBJECTS) == 1)
            constraint_count += 1
    print(f"Ограничений 'один предмет в слот': {constraint_count}")
    
    # Ограничение 2: недельная норма часов
    for c in CLASSES:
        for s in SUBJECTS:
            model.Add(sum(x[(c, s, slot)] for slot in SLOTS) == REQUIRED_HOURS[c][s])
            constraint_count += 1
    print(f"Всего ограничений норма часов: {constraint_count}")
    
    # Ограничение 3: учитель не может быть в двух местах одновременно
    teachers = set(TEACHER_OF.values())
    for teacher in teachers:
        for slot in SLOTS:
            # Найти все предметы этого учителя
            teacher_subjects = [s for s in SUBJECTS if TEACHER_OF[s] == teacher]
            # В каждом слоте учитель может вести максимум 1 урок
            model.Add(sum(x[(c, s, slot)] for c in CLASSES for s in teacher_subjects) <= 1)
            constraint_count += 1
    
    print(f"Всего ограничений: {constraint_count}")
    print(f"Учителей: {len(teachers)}")
    
    # БЕЗ целевой функции - просто найти любое допустимое решение
    
    # Решение
    print("\n=== РЕШЕНИЕ ===")
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5.0
    solver.parameters.log_search_progress = True
    
    start_time = time.time()
    result = solver.Solve(model)
    solve_time = time.time() - start_time
    
    print(f"Время решения: {solve_time:.2f} сек")
    
    if result == cp_model.OPTIMAL:
        print("✓ Найдено ОПТИМАЛЬНОЕ решение")
    elif result == cp_model.FEASIBLE:
        print("✓ Найдено ДОПУСТИМОЕ решение") 
    elif result == cp_model.INFEASIBLE:
        print("✗ Задача НЕРЕШАЕМА")
        return False
    else:
        print(f"✗ Неизвестный статус: {result}")
        return False
    
    # Вывод расписания
    print("\n=== РАСПИСАНИЕ ===")
    
    def slot_to_day_period(slot):
        return slot // PERIODS_PER_DAY, slot % PERIODS_PER_DAY
    
    for c in CLASSES:
        print(f"\n--- Класс {c} ---")
        
        # Создать сетку расписания
        schedule = {}
        for slot in SLOTS:
            for s in SUBJECTS:
                if solver.Value(x[(c, s, slot)]) == 1:
                    day, period = slot_to_day_period(slot)
                    schedule[(day, period)] = s
                    break
        
        # Вывести красиво
        print("     ", end="")
        for p in range(PERIODS_PER_DAY):
            print(f"Урок{p+1:2}", end="  ")
        print()
        
        for d, day_name in enumerate(DAYS):
            print(f"{day_name:4} ", end="")
            for p in range(PERIODS_PER_DAY):
                subject = schedule.get((d, p), "---")
                print(f"{subject[:7]:7}", end="  ")
            print()
    
    # Проверка решения
    print("\n=== ПРОВЕРКА ===")
    for c in CLASSES:
        print(f"\nКласс {c}:")
        for s in SUBJECTS:
            actual_hours = sum(solver.Value(x[(c, s, slot)]) for slot in SLOTS)
            required = REQUIRED_HOURS[c][s]
            status = "✓" if actual_hours == required else "✗"
            print(f"  {s}: {actual_hours}/{required} {status}")
    
    return True

if __name__ == "__main__":
    try:
        success = create_simple_timetable()
        if success:
            print("\n🎉 Программа завершена успешно!")
        else:
            print("\n❌ Программа завершена с ошибками")
    except ImportError:
        print("❌ Не установлен OR-Tools. Установите: pip install ortools")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()