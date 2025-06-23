# План урока: Создание игры на Python Tkinter Canvas
*Для детей 11-15 лет | Продолжительность: 60-90 минут*

## 🎯 Цели урока
- Познакомиться с библиотекой Tkinter и виджетом Canvas
- Научиться рисовать простые фигуры на холсте
- Создать интерактивную игру "Лови мяч"
- Понять основы событийного программирования

## 📋 Необходимые знания
- Базовые знания Python (переменные, функции, циклы)
- Установленный Python с Tkinter

---

## 🚀 Структура урока

### 1. Введение и мотивация (10 минут)
**Демонстрация готовой игры**
- Показать финальную версию игры "Лови мяч"
- Объяснить, что мы будем создавать сегодня
- Обсудить, где используется графическое программирование

**Что такое Tkinter?**
- Встроенная библиотека Python для создания графических интерфейсов
- Canvas - "холст" для рисования

### 2. Основы Canvas (15 минут)
**Создание окна и холста**
```python
import tkinter as tk

# Создаем главное окно
root = tk.Tk()
root.title("Моя первая игра")

# Создаем холст
canvas = tk.Canvas(root, width=800, height=600, bg='lightblue')
canvas.pack()

root.mainloop()
```

**Практическое задание 1:**
Ученики создают свое первое окно с холстом, экспериментируют с цветами фона.

**Рисование простых фигур**
```python
# Рисуем круг
canvas.create_oval(100, 100, 150, 150, fill='red')

# Рисуем прямоугольник  
canvas.create_rectangle(200, 200, 300, 250, fill='blue')

# Рисуем линию
canvas.create_line(0, 0, 100, 100, width=5)
```

**Практическое задание 2:**
Создать простой рисунок из нескольких фигур (дом, солнце, дерево).

### 3. Создание игры "Лови мяч" - Часть 1 (20 минут)

**Создание игрового поля и мяча**
```python
import tkinter as tk
import random

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Лови мяч!")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='lightgreen')
        self.canvas.pack()
        
        # Создаем мяч
        self.ball_x = 400
        self.ball_y = 50
        self.ball_speed_x = random.choice([-3, -2, 2, 3])
        self.ball_speed_y = 2
        
        self.ball = self.canvas.create_oval(
            self.ball_x-20, self.ball_y-20,
            self.ball_x+20, self.ball_y+20,
            fill='red'
        )
        
    def start_game(self):
        self.root.mainloop()

# Запускаем игру
game = Game()
game.start_game()
```

**Объяснение концепций:**
- Класс для организации кода
- Координаты на холсте
- Переменные для позиции и скорости мяча

### 4. Анимация мяча (15 минут)

**Добавляем движение**
```python
def move_ball(self):
    # Двигаем мяч
    self.ball_x += self.ball_speed_x
    self.ball_y += self.ball_speed_y
    
    # Отскок от стен
    if self.ball_x <= 20 or self.ball_x >= 780:
        self.ball_speed_x = -self.ball_speed_x
    if self.ball_y <= 20:
        self.ball_speed_y = -self.ball_speed_y
    
    # Обновляем позицию на холсте
    self.canvas.coords(self.ball,
                      self.ball_x-20, self.ball_y-20,
                      self.ball_x+20, self.ball_y+20)
    
    # Повторяем через 20 миллисекунд
    self.root.after(20, self.move_ball)
```

**Практическое задание 3:**
Добавить движение мяча, протестировать отскок от стен.

### 5. Создание игры - Часть 2 (15 минут)

**Добавляем платформу и управление**
```python
def __init__(self):
    # ... предыдущий код ...
    
    # Создаем платформу
    self.paddle_x = 350
    self.paddle_y = 550
    self.paddle = self.canvas.create_rectangle(
        self.paddle_x, self.paddle_y,
        self.paddle_x + 100, self.paddle_y + 20,
        fill='blue'
    )
    
    # Привязываем управление
    self.canvas.bind('<Motion>', self.move_paddle)
    self.canvas.focus_set()

def move_paddle(self, event):
    self.paddle_x = event.x - 50
    if self.paddle_x < 0:
        self.paddle_x = 0
    if self.paddle_x > 700:
        self.paddle_x = 700
        
    self.canvas.coords(self.paddle,
                      self.paddle_x, self.paddle_y,
                      self.paddle_x + 100, self.paddle_y + 20)
```

**Объяснение:**
- События мыши
- Ограничения движения платформы

### 6. Завершение игры (10 минут)

**Добавляем столкновения и счет**
```python
def check_collision(self):
    # Проверяем столкновение с платформой
    if (self.ball_y + 20 >= self.paddle_y and
        self.ball_x >= self.paddle_x and
        self.ball_x <= self.paddle_x + 100):
        self.ball_speed_y = -abs(self.ball_speed_y)
        self.score += 1
        
    # Проверяем падение мяча
    if self.ball_y > 600:
        self.game_over()

def game_over(self):
    self.canvas.create_text(400, 300, text=f"Игра окончена! Счет: {self.score}",
                           font=('Arial', 24), fill='red')
```

### 7. Демонстрация и обсуждение (5 минут)
- Ученики показывают свои игры
- Обсуждение возможных улучшений
- Идеи для домашнего задания

---

## 🎮 Полный код игры
```python
import tkinter as tk
import random

class BallCatcherGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Лови мяч!")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='lightgreen')
        self.canvas.pack()
        
        # Игровые переменные
        self.score = 0
        self.game_running = True
        
        # Создаем мяч
        self.ball_x = 400
        self.ball_y = 50
        self.ball_speed_x = random.choice([-3, -2, 2, 3])
        self.ball_speed_y = 2
        
        self.ball = self.canvas.create_oval(
            self.ball_x-20, self.ball_y-20,
            self.ball_x+20, self.ball_y+20,
            fill='red', outline='darkred', width=2
        )
        
        # Создаем платформу
        self.paddle_x = 350
        self.paddle_y = 550
        self.paddle = self.canvas.create_rectangle(
            self.paddle_x, self.paddle_y,
            self.paddle_x + 100, self.paddle_y + 20,
            fill='blue', outline='darkblue', width=2
        )
        
        # Счет
        self.score_text = self.canvas.create_text(
            50, 30, text=f"Счет: {self.score}",
            font=('Arial', 16), fill='black'
        )
        
        # Управление
        self.canvas.bind('<Motion>', self.move_paddle)
        self.canvas.focus_set()
        
        # Запускаем игру
        self.move_ball()
        
    def move_paddle(self, event):
        if not self.game_running:
            return
            
        self.paddle_x = event.x - 50
        if self.paddle_x < 0:
            self.paddle_x = 0
        if self.paddle_x > 700:
            self.paddle_x = 700
            
        self.canvas.coords(self.paddle,
                          self.paddle_x, self.paddle_y,
                          self.paddle_x + 100, self.paddle_y + 20)
    
    def move_ball(self):
        if not self.game_running:
            return
            
        # Двигаем мяч
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y
        
        # Отскок от стен
        if self.ball_x <= 20 or self.ball_x >= 780:
            self.ball_speed_x = -self.ball_speed_x
        if self.ball_y <= 20:
            self.ball_speed_y = -self.ball_speed_y
        
        # Проверка столкновения с платформой
        if (self.ball_y + 20 >= self.paddle_y and
            self.ball_y + 20 <= self.paddle_y + 20 and
            self.ball_x >= self.paddle_x and
            self.ball_x <= self.paddle_x + 100):
            self.ball_speed_y = -abs(self.ball_speed_y)
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Счет: {self.score}")
        
        # Проверка падения мяча
        if self.ball_y > 600:
            self.game_over()
            return
        
        # Обновляем позицию мяча
        self.canvas.coords(self.ball,
                          self.ball_x-20, self.ball_y-20,
                          self.ball_x+20, self.ball_y+20)
        
        # Повторяем через 20 миллисекунд
        self.root.after(20, self.move_ball)
    
    def game_over(self):
        self.game_running = False
        self.canvas.create_text(400, 300, 
                               text=f"Игра окончена!\nВаш счет: {self.score}",
                               font=('Arial', 24), fill='red',
                               justify='center')
    
    def start_game(self):
        self.root.mainloop()

# Запускаем игру
if __name__ == "__main__":
    game = BallCatcherGame()
    game.start_game()
```

---

## 🏠 Домашнее задание
1. Добавить звуковые эффекты при отскоке мяча
2. Создать уровни сложности (изменение скорости мяча)
3. Добавить препятствия на игровом поле
4. Сделать мяч разноцветным или добавить несколько мячей

## 📚 Дополнительные ресурсы
- Документация Python Tkinter
- Примеры других простых игр на Tkinter
- Идеи для следующих проектов

## ✅ Критерии успеха урока
- Ученик может создать окно с Canvas
- Умеет рисовать простые фигуры
- Понимает принцип анимации через after()
- Создал работающую версию игры
- Может объяснить основные концепции