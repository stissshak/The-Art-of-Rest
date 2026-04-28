import numpy as np
import perlin as pr
import matplotlib.pyplot as plot
from config import Config 

class Terrain:
    def _create_terrain():

# размеры карты
width = Config.SCREEN_WIDTH
height = Config.SCREEN_HEIGHT

# 1D координаты для heightmap
x = np.linspace(0, 10, width)

# генерация 1D перлин шума
noise_1d = pr.noise(x, np.zeros_like(x), seed=420)

# нормализация в [0, 1]
noise_1d = (noise_1d - noise_1d.min()) / (noise_1d.max() - noise_1d.min())

# масштабируем в высоту
ground_level = (noise_1d * 300 + 400).astype(int)

# создаём пустую карту
terrain = np.zeros((height, width), dtype=np.uint8)

# заполняем землю
for ix in range(width):
    terrain[ground_level[ix]:, ix] = 1

# создаём 2D координатную сетку для деталей/пещер
x_grid = np.linspace(0, 10, width)
y_grid = np.linspace(0, 10, height)
x_grid, y_grid = np.meshgrid(x_grid, y_grid)

# 2D перлин шум для пещер
noise2d = pr.noise(x_grid, y_grid, seed=3)

# применяем порог и объединяем с основной землёй
terrain = np.logical_and(terrain, noise2d > -0.2).astype(np.uint8)

# вывод и сохранение
plot.imshow(terrain, origin='upper', cmap='gray')
plot.savefig("perlin.png")
