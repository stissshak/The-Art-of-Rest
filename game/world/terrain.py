import numpy as np
import pygame

from config import Config
from . import perlin as pr


class Terrain:
    COLORKEY = (255, 0, 255)
    DIRT = (110, 70, 40)
    GRASS = (90, 170, 80)
    CRATER_RIM = (70, 45, 25)
    GRASS_THICKNESS = 6

    def __init__(self, width: int = None, height: int = None, seed: int = 42):
        self.width = width if width is not None else Config.SCREEN_WIDTH
        self.height = height if height is not None else Config.SCREEN_HEIGHT
        self.seed = seed

        self.mask = self._generate_mask()
        self.surface = self._build_surface()

    def _generate_mask(self) -> np.ndarray:
        w, h = self.width, self.height

        ground_level = self._heightmap()
        ys = np.arange(h)[:, None]
        mask = ys >= ground_level[None, :]

        self._add_islands(mask)

        mask[int(h * 0.92):, :] = True   # bedrock floor
        return mask

    def _heightmap(self) -> np.ndarray:
        # Sum several octaves (fBm): low freq = big hills, high freq = fine bumps.
        w, h = self.width, self.height
        line = np.zeros(w)
        amp, total = 1.0, 0.0
        for octave in range(3):
            freq = 2 ** octave
            xs = np.linspace(0, 7 * freq, w)
            line += amp * pr.noise(xs, np.zeros_like(xs), seed=self.seed + octave)
            total += amp
            amp *= 0.5
        line = _normalize(line / total)
        return np.clip((line * (h * 0.30) + h * 0.44).astype(int), 0, h - 1)

    def _add_islands(self, mask: np.ndarray):
        # Detached noisy ellipses floating above the worms' starting ground.
        w, h = self.width, self.height
        rng = np.random.default_rng(self.seed + 99)
        for i in range(int(rng.integers(3, 6))):
            cx = int(rng.integers(int(w * 0.10), int(w * 0.90)))
            cy = int(rng.integers(int(h * 0.12), int(h * 0.30)))
            rx = int(rng.integers(60, 160))
            ry = int(rng.integers(25, 50))

            x0, x1 = max(0, cx - rx), min(w, cx + rx + 1)
            y0, y1 = max(0, cy - ry), min(h, cy + ry + 1)
            yy, xx = np.ogrid[y0:y1, x0:x1]
            nx, ny = np.meshgrid(np.linspace(0, 4, x1 - x0), np.linspace(0, 3, y1 - y0))
            wobble = pr.noise(nx, ny, seed=self.seed + i)

            ell = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0 + 0.3 * wobble
            mask[y0:y1, x0:x1] |= ell

    def _build_surface(self) -> pygame.Surface:
        w, h = self.width, self.height
        solid = self.mask.T

        rgb = np.empty((w, h, 3), dtype=np.uint8)
        rgb[:, :] = self.COLORKEY
        rgb[solid] = self.DIRT

        above = np.zeros_like(solid)
        above[:, self.GRASS_THICKNESS:] = solid[:, :-self.GRASS_THICKNESS]
        rgb[solid & ~above] = self.GRASS

        surface = pygame.surfarray.make_surface(rgb)
        surface.set_colorkey(self.COLORKEY)
        return surface

    def is_solid(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return bool(self.mask[int(y), int(x)])
        return False

    def rect_collides(self, rect: pygame.Rect) -> bool:
        x0 = max(0, int(rect.left))
        x1 = min(self.width, int(rect.right))
        y0 = max(0, int(rect.top))
        y1 = min(self.height, int(rect.bottom))
        if x0 >= x1 or y0 >= y1:
            return False
        return bool(self.mask[y0:y1, x0:x1].any())

    def destroy_circle(self, cx: int, cy: int, radius: int):
        cx, cy, radius = int(cx), int(cy), int(radius)
        x0 = max(0, cx - radius)
        x1 = min(self.width, cx + radius + 1)
        y0 = max(0, cy - radius)
        y1 = min(self.height, cy + radius + 1)
        if x0 >= x1 or y0 >= y1:
            return

        ys, xs = np.ogrid[y0:y1, x0:x1]
        disk = (xs - cx) ** 2 + (ys - cy) ** 2 <= radius ** 2
        self.mask[y0:y1, x0:x1][disk] = False

        pygame.draw.circle(self.surface, self.COLORKEY, (cx, cy), radius)
        pygame.draw.circle(self.surface, self.CRATER_RIM, (cx, cy), radius, width=3)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, (0, 0))


def _normalize(a: np.ndarray) -> np.ndarray:
    span = a.max() - a.min()
    if span == 0:
        return np.zeros_like(a)
    return (a - a.min()) / span
