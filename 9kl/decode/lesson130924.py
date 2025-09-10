def decode_csv_like_format(input_str):
    # Разбиваем входную строку на строки по разделителю ;
    rows = input_str.split(';')
    
    # Здесь будем хранить результат - массив 16 строк
    result = []
    
    for row in rows:
        row_data = row.split(',')  # Разбиваем строку на отдельные элементы
        decoded_row = ""  # Строка для хранения результата декодирования строки
        
        for i in range(0, len(row_data), 2):
            color = row_data[i]       # Берем цвет (1 или 0)
            count = int(row_data[i+1])  # Берем количество повторений
            
            decoded_row += color * count  # Повторяем цвет необходимое число раз
        
        # Если строка короче 16 символов, заполняем оставшееся место нулями
        decoded_row = decoded_row.ljust(16, '0')
        
        # Добавляем результат в итоговый список, ограничив длину строки до 16 символов
        result.append(decoded_row[:16])
    
    return result

# Пример использования
input_str = "1,5,0,3,1,8;0,16;1,7,0,9"
decoded = decode_csv_like_format(input_str)

# Вывод результата
for row in decoded:
    print(row)
