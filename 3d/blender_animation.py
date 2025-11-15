import bpy
import math

# Очистка сцены
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Параметры анимации
frame_start = 1
frame_end = 250
cube_travel_distance = 50  # Расстояние движения куба по Y
cube_rotations = -2  # Количество оборотов куба (отрицательное = против часовой)
spiral_radius = 3  # Радиус спирали
spiral_turns = 3  # Количество витков спирали
spiral_points = 200  # Точек в спирали

# ==================== СОЗДАНИЕ КУБА ====================
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "Cube"

# Анимация движения куба
cube.location = (0, 0, 0)
cube.keyframe_insert(data_path="location", frame=frame_start)
cube.location = (0, cube_travel_distance, 0)
cube.keyframe_insert(data_path="location", frame=frame_end)

# Анимация вращения куба
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=frame_start)
cube.rotation_euler = (0, 0, math.radians(cube_rotations * 360))
cube.keyframe_insert(data_path="rotation_euler", frame=frame_end)

# Материал для куба (синий с излучением)
mat_cube = bpy.data.materials.new(name="CubeMaterial")
mat_cube.use_nodes = True
nodes = mat_cube.node_tree.nodes
nodes.clear()
node_emission = nodes.new(type='ShaderNodeEmission')
node_emission.inputs[0].default_value = (0.2, 0.4, 1.0, 1.0)  # Синий цвет
node_emission.inputs[1].default_value = 2.0  # Сила свечения
node_output = nodes.new(type='ShaderNodeOutputMaterial')
mat_cube.node_tree.links.new(node_emission.outputs[0], node_output.inputs[0])
cube.data.materials.append(mat_cube)

# ==================== СОЗДАНИЕ СПИРАЛЬНОЙ ТРАЕКТОРИИ ====================
curve_data = bpy.data.curves.new('SpiralCurve', type='CURVE')
curve_data.dimensions = '3D'
polyline = curve_data.splines.new('POLY')

# Генерация точек спирали (по часовой, противоположно вращению куба)
points_coords = []
for i in range(spiral_points):
    t = i / (spiral_points - 1)
    y = t * cube_travel_distance
    # Положительный угол = по часовой (противоположно вращению куба)
    angle = t * spiral_turns * 2 * math.pi
    x = spiral_radius * math.cos(angle)
    z = spiral_radius * math.sin(angle)
    points_coords.append((x, y, z))

polyline.points.add(len(points_coords) - 1)
for i, coord in enumerate(points_coords):
    polyline.points[i].co = coord + (1.0,)

curve_obj = bpy.data.objects.new('Spiral', curve_data)
bpy.context.collection.objects.link(curve_obj)
curve_data.bevel_depth = 0.02  # Толщина линии для визуализации
curve_data.bevel_resolution = 4

# Материал для спирали (слабое свечение)
mat_spiral = bpy.data.materials.new(name="SpiralMaterial")
mat_spiral.use_nodes = True
nodes_spiral = mat_spiral.node_tree.nodes
nodes_spiral.clear()
node_emission_spiral = nodes_spiral.new(type='ShaderNodeEmission')
node_emission_spiral.inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
node_emission_spiral.inputs[1].default_value = 0.5
node_output_spiral = nodes_spiral.new(type='ShaderNodeOutputMaterial')
mat_spiral.node_tree.links.new(node_emission_spiral.outputs[0], node_output_spiral.inputs[0])
curve_data.materials.append(mat_spiral)

# ==================== СОЗДАНИЕ ШАРА ====================
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
sphere = bpy.context.active_object
sphere.name = "Sphere"

# Материал для шара (красный с излучением)
mat_sphere = bpy.data.materials.new(name="SphereMaterial")
mat_sphere.use_nodes = True
nodes_sphere = mat_sphere.node_tree.nodes
nodes_sphere.clear()
node_emission_sphere = nodes_sphere.new(type='ShaderNodeEmission')
node_emission_sphere.inputs[0].default_value = (1.0, 0.3, 0.2, 1.0)  # Красный
node_emission_sphere.inputs[1].default_value = 3.0
node_output_sphere = nodes_sphere.new(type='ShaderNodeOutputMaterial')
mat_sphere.node_tree.links.new(node_emission_sphere.outputs[0], node_output_sphere.inputs[0])
sphere.data.materials.append(mat_sphere)

# Привязка шара к траектории через Follow Path constraint
constraint = sphere.constraints.new(type='FOLLOW_PATH')
constraint.target = curve_obj
constraint.use_fixed_location = False
constraint.forward_axis = 'FORWARD_Y'
constraint.up_axis = 'UP_Z'

# Анимация движения шара по траектории
constraint.offset_factor = 0.0
constraint.keyframe_insert(data_path="offset_factor", frame=frame_start)
constraint.offset_factor = 1.0
constraint.keyframe_insert(data_path="offset_factor", frame=frame_end)

# ==================== СОЗДАНИЕ ЗВЁЗД ====================
# Создаём множество маленьких светящихся сфер как звёзды
import random

random.seed(42)  # Для воспроизводимости
num_stars = 300
star_field_size = 100

for i in range(num_stars):
    x = random.uniform(-star_field_size, star_field_size)
    y = random.uniform(-20, cube_travel_distance + 20)
    z = random.uniform(-star_field_size, star_field_size)
    
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,
        radius=random.uniform(0.1, 0.3),
        location=(x, y, z)
    )
    star = bpy.context.active_object
    star.name = f"Star_{i}"
    
    # Материал звезды
    if i == 0:  # Создаём материал только один раз
        mat_star = bpy.data.materials.new(name="StarMaterial")
        mat_star.use_nodes = True
        nodes_star = mat_star.node_tree.nodes
        nodes_star.clear()
        node_emission_star = nodes_star.new(type='ShaderNodeEmission')
        node_emission_star.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
        node_emission_star.inputs[1].default_value = random.uniform(1.0, 3.0)
        node_output_star = nodes_star.new(type='ShaderNodeOutputMaterial')
        mat_star.node_tree.links.new(node_emission_star.outputs[0], node_output_star.inputs[0])
    
    star.data.materials.append(mat_star)

# ==================== НАСТРОЙКА КАМЕРЫ ====================
# Создаём камеру
bpy.ops.object.camera_add(location=(0, -15, 8))
camera = bpy.context.active_object
camera.name = "Camera"

# Родительская привязка камеры к кубу
camera.parent = cube
camera.matrix_parent_inverse = cube.matrix_world.inverted()

# Настройка камеры чтобы смотрела на куб
constraint_camera = camera.constraints.new(type='TRACK_TO')
constraint_camera.target = cube
constraint_camera.track_axis = 'TRACK_NEGATIVE_Z'
constraint_camera.up_axis = 'UP_Y'

# Устанавливаем эту камеру как активную
bpy.context.scene.camera = camera

# ==================== НАСТРОЙКА ОСВЕЩЕНИЯ ====================
bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
sun = bpy.context.active_object
sun.data.energy = 2.0

# ==================== НАСТРОЙКА СЦЕНЫ ====================
scene = bpy.context.scene
scene.frame_start = frame_start
scene.frame_end = frame_end
scene.frame_current = frame_start

# Настройка фона (чёрный космос)
world = bpy.data.worlds.get("World")
if world is None:
    world = bpy.data.worlds.new("World")
    scene.world = world

world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)  # Чёрный цвет
    bg_node.inputs[1].default_value = 0.0  # Без свечения

# Настройка рендера
scene.render.engine = 'BLENDER_EEVEE'  # Используем Eevee для быстрого рендера
scene.eevee.use_bloom = True  # Эффект свечения
scene.eevee.bloom_intensity = 0.5

# Настройка разрешения
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 24

# Установка линейной интерполяции для плавного движения
for obj in [cube, sphere]:
    if obj.animation_data:
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'LINEAR'

# Линейная интерполяция для constraint
if sphere.animation_data:
    for fcurve in sphere.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'

print("✓ Сцена создана успешно!")
print(f"✓ Анимация: {frame_start}-{frame_end} кадров")
print(f"✓ Создано объектов: Куб, Шар, {num_stars} звёзд, Камера")
print("✓ Нажмите Space для воспроизведения анимации")