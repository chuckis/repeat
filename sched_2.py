"""
Диагностика проблем с составлением расписания
Поэтапно проверяем каждое ограничение
"""
from ortools.sat.python import cp_model

def analyze_constraints():
    print("=== АНАЛИЗ ОГРАНИЧЕНИЙ ===\n")
    
    DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт"]
    PERIODS_PER_DAY = 6
    CLASSES = ["5А", "5Б"]
    SUBJECTS = ["Математика", "Русский", "Физика", "Физкультура", "ИЗО", "Англ"]
    
    TEACHER_OF = {
        "Математика": "Учитель1",
        "Русский": "Учитель2", 
        "Физика": "Учитель3",
        "Физкультура": "Учитель4",
        "ИЗО": "Учитель5",
        "Англ": "Учитель1"
    }
    
    REQUIRED_HOURS = {
        "5А": {"Математика": 7, "Русский": 7, "Физика": 6, "Физкультура": 5, "ИЗО": 5, "Англ": 3},
        "5Б": {"Математика": 7, "Русский": 7, "Физика": 6, "Физкультура": 5, "ИЗО": 5, "Англ": 3}
    }
    
    TOTAL_SLOTS = len(DAYS) * PERIODS_PER_DAY
    print(f"Всего временных слотов в неделю: {TOTAL_SLOTS}")
    print(f"Количество классов: {len(CLASSES)}")
    print(f"Количество предметов: {len(SUBJECTS)}")
    print(f"Количество учителей: {len(set(TEACHER_OF.values()))}")
    
    # Проверка 1: Баланс часов
    print("\n1. ПРОВЕРКА БАЛАНСА ЧАСОВ:")
    for cls in CLASSES:
        total_required = sum(REQUIRED_HOURS[cls].values())
        print(f"   Класс {cls}: требуется {total_required} часов, доступно {TOTAL_SLOTS}")
        if total_required != TOTAL_SLOTS:
            print(f"   ❌ ПРОБЛЕМА: несоответствие!")
            return False
    print("   ✓ Баланс часов корректен")
    
    # Проверка 2: Нагрузка учителей
    print("\n2. ПРОВЕРКА НАГРУЗКИ УЧИТЕЛЕЙ:")
    teacher_load = {}
    for subject, teacher in TEACHER_OF.items():
        if teacher not in teacher_load:
            teacher_load[teacher] = 0
        # Каждый учитель ведет предмет во ВСЕХ классах
        for cls in CLASSES:
            teacher_load[teacher] += REQUIRED_HOURS[cls][subject]
    
    for teacher, load in teacher_load.items():
        subjects = [s for s, t in TEACHER_OF.items() if t == teacher]
        print(f"   {teacher} (предметы: {subjects}): {load} часов в неделю")
        if load > TOTAL_SLOTS:
            print(f"   ❌ ПРОБЛЕМА: учитель перегружен! Максимум {TOTAL_SLOTS} часов")
            return False
    print("   ✓ Нагрузка учителей допустима")
    
    # Проверка 3: Конфликты учителей (основная причина!)
    print("\n3. ПРОВЕРКА КОНФЛИКТОВ УЧИТЕЛЕЙ:")
    print("   Анализируем: может ли учитель физически вести все свои уроки...")
    
    # Для каждого учителя считаем максимально возможные конфликты
    max_conflicts_per_slot = {}
    for teacher, load in teacher_load.items():
        subjects = [s for s, t in TEACHER_OF.items() if t == teacher]
        max_conflicts = len(CLASSES)  # учитель может конфликтовать максимум с количеством классов
        max_conflicts_per_slot[teacher] = max_conflicts
        
        print(f"   {teacher}:")
        print(f"     - Ведет предметы: {subjects}")
        print(f"     - Общая нагрузка: {load} часов") 
        print(f"     - Максимальные конфликты в слот: {max_conflicts} (количество классов)")
        
        # Если учитель должен вести один предмет в разных классах одновременно
        for subject in subjects:
            hours_per_class = {}
            for cls in CLASSES:
                hours_per_class[cls] = REQUIRED_HOURS[cls][subject]
            
            if len(set(hours_per_class.values())) == 1 and len(CLASSES) > 1:
                same_hours = list(hours_per_class.values())[0]
                if same_hours > 0:
                    print(f"     - ПОТЕНЦИАЛЬНАЯ ПРОБЛЕМА с предметом '{subject}':")
                    print(f"       Все {len(CLASSES)} класса нуждаются в {same_hours} часах")
                    print(f"       Но учитель может вести только 1 класс одновременно!")
    
    print("\n4. ТЕСТ ПРОСТЕЙШЕЙ МОДЕЛИ (только основные ограничения):")
    return test_basic_model(DAYS, PERIODS_PER_DAY, CLASSES, SUBJECTS, TEACHER_OF, REQUIRED_HOURS)

def test_basic_model(DAYS, PERIODS_PER_DAY, CLASSES, SUBJECTS, TEACHER_OF, REQUIRED_HOURS):
    SLOTS = list(range(len(DAYS) * PERIODS_PER_DAY))
    
    model = cp_model.CpModel()
    
    # Переменные
    x = {}
    for c in CLASSES:
        for s in SUBJECTS:
            for slot in SLOTS:
                x[(c, s, slot)] = model.NewBoolVar(f"x_{c}_{s}_{slot}")
    
    # Только самые базовые ограничения
    print("   Добавляю ограничения...")
    
    # 1. В каждом слоте у класса один предмет
    for c in CLASSES:
        for slot in SLOTS:
            model.Add(sum(x[(c, s, slot)] for s in SUBJECTS) == 1)
    
    # 2. Недельная норма часов  
    for c in CLASSES:
        for s in SUBJECTS:
            model.Add(sum(x[(c, s, slot)] for slot in SLOTS) == REQUIRED_HOURS[c][s])
    
    print("   Пробую решить БЕЗ ограничений на учителей...")
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 3.0
    result1 = solver.Solve(model)
    
    if result1 == cp_model.FEASIBLE or result1 == cp_model.OPTIMAL:
        print("   ✓ Базовая модель решаема")
    else:
        print("   ❌ Даже базовая модель нерешаема!")
        return False
    
    # Теперь добавим ограничения на учителей
    print("   Добавляю ограничения на учителей...")
    
    teachers = set(TEACHER_OF.values())
    for teacher in teachers:
        for slot in SLOTS:
            teacher_subjects = [s for s in SUBJECTS if TEACHER_OF[s] == teacher]
            model.Add(sum(x[(c, s, slot)] for c in CLASSES for s in teacher_subjects) <= 1)
    
    print("   Пробую решить С ограничениями на учителей...")
    
    result2 = solver.Solve(model)
    
    if result2 == cp_model.FEASIBLE or result2 == cp_model.OPTIMAL:
        print("   ✓ Полная модель решаема!")
        return True
    else:
        print("   ❌ Ограничения на учителей делают задачу нерешаемой!")
        print("\n=== ПРИЧИНА ПРОБЛЕМЫ ===")
        print("Скорее всего проблема в том, что:")
        print("1. Учителя должны вести одинаковые предметы в разных классах")
        print("2. Но они не могут быть в двух местах одновременно")
        print("3. При текущем расписании это создает неразрешимые конфликты")
        print("\nРЕШЕНИЯ:")
        print("- Уменьшить количество часов по некоторым предметам")
        print("- Добавить больше учителей (разные учителя для разных классов)")
        print("- Увеличить количество дней или уроков в день")
        return False

def suggest_fixes():
    print("\n=== ПРЕДЛАГАЕМЫЕ ИСПРАВЛЕНИЯ ===")
    print("\nВариант 1: Разные учителя для каждого класса")
    
    TEACHER_OF_FIXED = {
        ("5А", "Математика"): "Математик_5А",
        ("5А", "Русский"): "Русский_5А", 
        ("5А", "Физика"): "Физик_5А",
        ("5А", "Физкультура"): "Физрук_5А",
        ("5А", "ИЗО"): "ИЗО_5А",
        
        ("5Б", "Математика"): "Математик_5Б",
        ("5Б", "Русский"): "Русский_5Б",
        ("5Б", "Физика"): "Физик_5Б", 
        ("5Б", "Физкультура"): "Физрук_5Б",
        ("5Б", "ИЗО"): "ИЗО_5Б",
    }
    
    print("Код с разными учителями для каждого класса:")
    print("""
TEACHER_OF = {
    ("5А", "Математика"): "Математик_5А",
    ("5А", "Русский"): "Русский_5А", 
    ("5А", "Физика"): "Физик_5А",
    ("5А", "Физкультура"): "Физрук_5А",
    ("5А", "ИЗО"): "ИЗО_5А",
    
    ("5Б", "Математика"): "Математик_5Б",
    ("5Б", "Русский"): "Русский_5Б",
    ("5Б", "Физика"): "Физик_5Б", 
    ("5Б", "Физкультура"): "Физрук_5Б",
    ("5Б", "ИЗО"): "ИЗО_5Б",
}

# И изменить ограничение на:
for slot in SLOTS:
    for subject in SUBJECTS:
        # Каждый предмет может вестись только в одном классе за раз
        model.Add(sum(x[(c, subject, slot)] for c in CLASSES) <= 1)
    """)
    
    print("\nВариант 2: Уменьшить количество часов")
    print("""
REQUIRED_HOURS = {
    "5А": {"Математика": 6, "Русский": 6, "Физика": 6, "Физкультура": 3, "ИЗО": 3},  # = 24 часа
    "5Б": {"Математика": 6, "Русский": 6, "Физика": 6, "Физкультура": 3, "ИЗО": 3},  # = 24 часа
}
PERIODS_PER_DAY = 5  # вместо 6
    """)

if __name__ == "__main__":
    try:
        success = analyze_constraints()
        if not success:
            suggest_fixes()
    except ImportError:
        print("❌ Не установлен OR-Tools. Установите: pip install ortools")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()