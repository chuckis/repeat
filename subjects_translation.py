
SUBJECTS_UKRAINIAN = {
    'arithm': 'Арифметика',
    'math': 'Математика', # 5 class
    'algebra': 'Алгебра', # 7 class
    'geometry': 'Геометрія',
    'ukrmol': 'Укр.мова мол',
    'ukrmollit': 'Укр.література мол',
    'ukrm': 'Українська мова',
    'ukrlit': 'Українська література',
    'english': 'Англ. мова',
    'engmol': 'Англ. мова мол',
    'IT': 'Інформатика',
    'biology': 'Біологія',
    'history': 'Всесвітня історія',
    'ukrhistory': 'Історія України',
    'arts': 'Образотворче мистецтво',
    'music': 'Музичне мистецтво',
    'crafts': 'Трудове навчання',
    'craftsboys': 'Технології (хлопці)',
    'sport': 'Фізична культура',
    'physics': 'Фізика',
    'geo': 'Географія',
    'pravozn': 'Правознавство',
    'chem': 'Хімія',
    'prirod': 'Природознавство',
    'ippoter': 'Іпотерапія',    
    'verhova': 'Верхова Їзда',    
    'navch': 'Навчання грамоті',
    'CSL': 'ЦСМ',          
    'OPK': 'ОПК',          
    'JS': 'ЖС',            
    'event': 'Молебен'         
}

# Функция для получения перевода предмета
def translate_subject(subject_key):
    """
    Получить украинский перевод предмета по ключу
    
    Args:
        subject_key (str): Ключ предмета (например, 'math', 'english')
    
    Returns:
        str: Украинское название предмета или исходный ключ, если перевод не найден
    
    Examples:
        >>> translate_subject('math')
        'Математика'  # если заполнен словарь
        
        >>> translate_subject('unknown_subject')
        'unknown_subject'  # если перевод не найден
    """
    return SUBJECTS_UKRAINIAN.get(subject_key, subject_key)

# Функция для перевода списка предметов
def translate_subjects_list(subjects_list):
    """
    Перевести список предметов
    
    Args:
        subjects_list (list): Список ключей предметов
    
    Returns:
        list: Список переведенных названий предметов
    
    Examples:
        >>> translate_subjects_list(['math', 'english', 'sport'])
        ['Математика', 'Англійська мова', 'Фізична культура']
    """
    return [translate_subject(subject) for subject in subjects_list]

# Функция для получения всех доступных предметов
def get_available_subjects():
    """
    Получить список всех доступных предметов (ключи)
    
    Returns:
        list: Список ключей предметов
    """
    return list(SUBJECTS_UKRAINIAN.keys())

# Функция для получения всех переводов
def get_all_translations():
    """
    Получить словарь всех переводов
    
    Returns:
        dict: Полный словарь переводов
    """
    return SUBJECTS_UKRAINIAN.copy()

# Функция для проверки существования предмета
def subject_exists(subject_key):
    """
    Проверить, есть ли предмет в словаре
    
    Args:
        subject_key (str): Ключ предмета
    
    Returns:
        bool: True если предмет существует в словаре
    """
    return subject_key in SUBJECTS_UKRAINIAN
