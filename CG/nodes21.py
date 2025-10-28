import matplotlib.pyplot as plt
import numpy as np

# Настройки
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.axis('off')

# Параметры
inner_radius = 1.5
outer_radius = 2.0
nodes_per_circle = 10

# Генерация позиций нод
angles = np.linspace(0, 2*np.pi, nodes_per_circle, endpoint=False)

# Внутренняя окружность
inner_nodes = np.array([[inner_radius * np.cos(a), inner_radius * np.sin(a)] for a in angles])

# Внешняя окружность (со смещением на половину угла для интересного узора)
outer_angles = angles + np.pi/nodes_per_circle
outer_nodes = np.array([[outer_radius * np.cos(a), outer_radius * np.sin(a)] for a in outer_angles])

# Центральная нода
center = np.array([0, 0])

# Рисуем связи
# 1. От центра к внутренним нодам
for node in inner_nodes:
    ax.plot([center[0], node[0]], [center[1], node[1]], 'black', linewidth=1.5, alpha=0.6)

# 2. От внутренних к внешним (каждая внутренняя к трём ближайшим внешним)
for i, inner in enumerate(inner_nodes):
    # К предыдущей внешней
    prev_i = (i - 1) % nodes_per_circle
    ax.plot([inner[0], outer_nodes[prev_i][0]], [inner[1], outer_nodes[prev_i][1]], 'black', linewidth=1.5, alpha=0.6)
    # К соответствующей внешней
    ax.plot([inner[0], outer_nodes[i][0]], [inner[1], outer_nodes[i][1]], 'black', linewidth=1.5, alpha=0.6)
    # К следующей внешней
    # next_i = (i + 1) % nodes_per_circle
    # ax.plot([inner[0], outer_nodes[next_i][0]], [inner[1], outer_nodes[next_i][1]], 'g-', linewidth=1.5, alpha=0.6)

# 3. Соединяем соседние ноды на внешней окружности
for i in range(nodes_per_circle):
    next_i = (i + 1) % nodes_per_circle
    ax.plot([outer_nodes[i][0], outer_nodes[next_i][0]], 
            [outer_nodes[i][1], outer_nodes[next_i][1]], 'black', linewidth=1.5, alpha=0.6)

# 4. Соединяем соседние ноды на внутренней окружности
for i in range(nodes_per_circle):
    next_i = (i + 1) % nodes_per_circle
    ax.plot([inner_nodes[i][0], inner_nodes[next_i][0]], 
            [inner_nodes[i][1], inner_nodes[next_i][1]], 'black', linewidth=1.5, alpha=0.6)

# Рисуем ноды
ax.scatter(*center, s=200, c='black', zorder=10, edgecolors='black', linewidths=2)
ax.scatter(inner_nodes[:, 0], inner_nodes[:, 1], s=150, c='black', zorder=10, edgecolors='black', linewidths=2)
ax.scatter(outer_nodes[:, 0], outer_nodes[:, 1], s=150, c='black', zorder=10, edgecolors='black', linewidths=2)

# Установка пределов
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)

# Сохранение в SVG
plt.savefig('network_pattern.svg', format='svg', bbox_inches='tight', dpi=300)
plt.show()

print("SVG сохранен как 'network_pattern.svg'")