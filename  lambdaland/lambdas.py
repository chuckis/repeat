zero  = lambda f: lambda x: x
one   = lambda f: lambda x: f(x)
two   = lambda f: lambda x: f(f(x))
three = lambda f: lambda x: f(f(f(x)))

print(type(two))  # <class 'function'>  

def add(m, n):
    return lambda f: lambda x: m(f)(n(f)(x))

def multiply(m, n):
    return lambda f: m(n(f))

six = multiply(two, three)

# Тестируем:
five = add(two, three)

add_star = lambda s: s + "*"
print(five(add_star)(""))  # должно быть "*****"
print(six(add_star)(""))   # должно быть "******"

# Булевы значения и условные выражения

true  = lambda x: lambda y: x
false = lambda x: lambda y: y

print(true("яблоко")("банан"))  # "яблоко"

def if_then_else(condition, then_value, else_value):
    return condition(then_value)(else_value)

# Тесты:
print(if_then_else(true, "yes", "no"))   # "yes"
print(if_then_else(false, "yes", "no"))  # "no"

# Рекурсия

# Наша "самоприменяющаяся" функция:
f = lambda self, n: 1 if n == 0 else n * self(self, n - 1)

# Вызываем её так:
result = f(f, 5)  # передаём функцию саму себе!
print(result)  # 120

# Y = λf.(λx.f(x x))(λx.f(x x))