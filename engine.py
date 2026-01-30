import numpy as np

class AeroCellEngine:
    def __init__(self, width=50, height=50, diffusion=0.1, decay=0.005):
        self.width = width
        self.height = height
        self.diffusion = diffusion
        self.decay = decay
        self.grid = np.zeros((width, height))
        self.obstacles = np.zeros((width, height))

    def add_obstacle(self, x1, y1, x2, y2):
        self.obstacles[x1:x2, y1:y2] = 1

    def emit(self, x, y, concentration=1.0):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x, y] = concentration

    def update(self):
        # Difusão usando deslocamento de matriz (Vizinhança de Von Neumann)
        # Calcula a média dos vizinhos usando pad para evitar wraparound nas bordas
        padded_grid = np.pad(self.grid, pad_width=1, mode='constant', constant_values=0)
        
        neighbor_sum = (
            padded_grid[1:-1, 2:  ] +  # Vizinho direita
            padded_grid[1:-1, 0:-2] +  # Vizinho esquerda
            padded_grid[2:  , 1:-1] +  # Vizinho baixo
            padded_grid[0:-2, 1:-1]    # Vizinho acima
        )
        
        # Nova grade baseada na difusão e no decaimento (perda de carga viral)
        new_grid = (self.grid * (1 - self.diffusion) + (neighbor_sum / 4) * self.diffusion)
        new_grid *= (1 - self.decay)
        
        # Bloqueia propagação onde há obstáculos
        new_grid[self.obstacles == 1] = 0
        self.grid = new_grid