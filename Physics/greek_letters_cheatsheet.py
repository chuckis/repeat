from PIL import Image, ImageDraw, ImageFont

# Create an image with white background
width, height = 1200, 1000
img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)

# Prepare text content
text = """Greek Letters in Physics

α — альфа (al-fa) — угол; температурное расширение
β — бета (be-ta) — β-излучение; коэффициенты
γ — гамма (gam-ma) — γ-излучение; отношение теплоёмкостей
δ — дельта (del-ta) — малое изменение величины (δx)
ε — эпсилон (ep-si-lon) — диэлектрическая проницаемость; ЭДС
ζ — зета (ze-ta) — коэффициент затухания
η — эта (e-ta) — КПД; вязкость
θ — тета (the-ta) — угол
κ — каппа (kap-pa) — теплопроводность; коэффициенты
λ — лямбда (lam-bda) — длина волны
μ — мю (myu) — магнитный момент; коэффициент трения
ν — ню (nyu) — частота
ξ — кси (ksi) — затухание; переменные
π — пи (pi) — число π; импульс
ρ — ро (ro) — плотность; заряд
σ — сигма (sig-ma) — проводимость; поверхностная плотность
τ — тау (tau) — постоянная времени; момент силы
φ — фи (fi) — магнитный поток; потенциал
χ — хи (khi) — магнитная восприимчивость
ψ — пси (psi) — волновая функция (КМ)
ω — омега (o-me-ga) — циклическая частота
"""

# Select a default font
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 28)
except:
    font = ImageFont.load_default()

# Draw text
draw.text((40, 40), text, fill="black", font=font)

# Save image
file_path = "./greek_letters_physics.png"
img.save(file_path)

file_path
