import tkinter as tk
from tkinter import ttk

def decode_csv_like_format(input_str):
    """Декодирует CSV-like строку в массив строк 16x16"""
    if not input_str.strip():
        return ['0' * 16 for _ in range(16)]
    
    # Разбиваем входную строку на строки по разделителю ;
    rows = input_str.split(';')
    
    # Здесь будем хранить результат - массив 16 строк
    result = []
    
    for row in rows:
        if not row.strip():
            result.append('0' * 16)
            continue
            
        row_data = row.split(',')  # Разбиваем строку на отдельные элементы
        decoded_row = ""  # Строка для хранения результата декодирования строки
        
        try:
            for i in range(0, len(row_data), 2):
                if i + 1 < len(row_data):
                    color = row_data[i]       # Берем цвет (1 или 0)
                    count = int(row_data[i+1])  # Берем количество повторений
                    
                    decoded_row += color * count  # Повторяем цвет необходимое число раз
        except (ValueError, IndexError):
            # В случае ошибки декодирования заполняем нулями
            decoded_row = '0' * 16
        
        # Если строка короче 16 символов, заполняем оставшееся место нулями
        decoded_row = decoded_row.ljust(16, '0')
        
        # Добавляем результат в итоговый список, ограничив длину строки до 16 символов
        result.append(decoded_row[:16])
    
    # Если строк меньше 16, заполняем оставшиеся нулями
    while len(result) < 16:
        result.append('0' * 16)
    
    # Оставляем только первые 16 строк
    return result[:16]

class ASCIIArtDecoder:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Decoder")
        self.root.geometry("600x500")
        
        # Создаем основной фрейм
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Поле ввода
        ttk.Label(main_frame, text="Введите CSV-like строку:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_var = tk.StringVar()
        self.input_var.trace('w', self.on_input_change)
        
        self.input_entry = ttk.Entry(main_frame, textvariable=self.input_var, width=60)
        self.input_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Фрейм для отображения ASCII-картинки
        self.canvas_frame = ttk.LabelFrame(main_frame, text="ASCII Art (16x16)", padding="10")
        self.canvas_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Создаем canvas для отображения картинки
        self.canvas = tk.Canvas(self.canvas_frame, width=320, height=320, bg='white')
        self.canvas.pack()
        
        # Текстовое отображение для проверки
        ttk.Label(main_frame, text="Текстовое представление:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        self.text_display = tk.Text(main_frame, width=20, height=16, font=("Courier", 8))
        self.text_display.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Пример для демонстрации
        example = "1,5,0,3,1,8;0,16;1,7,0,9"
        self.input_var.set(example)
        
        # Настраиваем растягивание
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def on_input_change(self, *args):
        """Обновляет отображение при изменении входной строки"""
        input_str = self.input_var.get()
        decoded_data = decode_csv_like_format(input_str)
        
        # Обновляем графическое отображение
        self.update_canvas(decoded_data)
        
        # Обновляем текстовое отображение
        self.update_text_display(decoded_data)
    
    def update_canvas(self, data):
        """Обновляет графическое отображение на canvas"""
        self.canvas.delete("all")
        
        cell_size = 20  # Размер каждой ячейки в пикселях
        
        for row_idx, row in enumerate(data):
            for col_idx, cell in enumerate(row):
                x1 = col_idx * cell_size
                y1 = row_idx * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                if cell == '1':
                    # Черный квадрат для единицы
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='gray')
                else:
                    # Белый квадрат для нуля
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='gray')
    
    def update_text_display(self, data):
        """Обновляет текстовое отображение"""
        self.text_display.delete(1.0, tk.END)
        
        text_representation = ""
        for row in data:
            text_row = ""
            for char in row:
                if char == '1':
                    text_row += "█"  # Черный квадрат
                else:
                    text_row += "·"  # Точка для пустого места
            text_representation += text_row + "\n"
        
        self.text_display.insert(1.0, text_representation)

def main():
    root = tk.Tk()
    app = ASCIIArtDecoder(root)
    root.mainloop()

if __name__ == "__main__":
    main()