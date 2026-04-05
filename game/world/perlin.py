import numpy as np

def noise(x, y, seed=0):
    # создание матрицы для шума и генерация случайного seed
    np.random.seed(seed)
    ptable = np.arange(256, dtype=int)
    np.random.shuffle(ptable)
    ptable = np.stack([ptable, ptable]).flatten()

    # координаты сетки
    xi, yi = x.astype(int), y.astype(int)
    xg, yg = x - xi, y - yi
    xf, yf = fade(xg), fade(yg)

    # вычисляем градиенты (vectorized)
    n00 = gradient_vectorized(ptable[ptable[xi] + yi], xg, yg)
    n01 = gradient_vectorized(ptable[ptable[xi] + yi + 1], xg, yg - 1)
    n11 = gradient_vectorized(ptable[ptable[xi + 1] + yi + 1], xg - 1, yg - 1)
    n10 = gradient_vectorized(ptable[ptable[xi + 1] + yi], xg - 1, yg)

    # линейная интерполяция
    x1 = lerp(n00, n10, xf)
    x2 = lerp(n01, n11, xf)
    return lerp(x1, x2, yf)


def lerp(a, b, t):
    return a + t * (b - a)


def fade(f):
    return 6*f**5 - 15*f**4 + 10*f**3


def gradient_vectorized(c, x, y):
    """
    Vectorized gradient: c, x, y могут быть массивами одинаковой формы
    """
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    # если массив
    if np.ndim(c) > 0:
        result = np.empty_like(c, dtype=float)
        it = np.nditer(c, flags=['multi_index'])
        while not it.finished:
            idx = it.multi_index
            grad = vectors[c[idx] % 4]
            result[idx] = grad[0]*x[idx] + grad[1]*y[idx]
            it.iternext()
        return result
    else:
        grad = vectors[c % 4]
        return grad[0]*x + grad[1]*y