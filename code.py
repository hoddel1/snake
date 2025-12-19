import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Размеры окна и ячейки
CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Изгиб Питона')
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для игровых объектов.
    
    Атрибуты:
        position (tuple): Координаты объекта на игровом поле (x, y)
        body_color (tuple): Цвет объекта в формате RGB
    """
    
    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """
        Инициализация игрового объекта.
        
        Args:
            position (tuple): Начальные координаты объекта
            body_color (tuple): Цвет объекта
        """
        self.position = position
        self.body_color = body_color
    
    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта.
        
        Args:
            surface: Поверхность Pygame для отрисовки
        """
        pass


class Apple(GameObject):
    """
    Класс для представления яблока в игре.
    
    Наследуется от GameObject.
    """
    
    def __init__(self):
        """Инициализация яблока с красным цветом и случайной позицией."""
        super().__init__(body_color=RED)
        self.randomize_position()
    
    def randomize_position(self):
        """Устанавливает случайную позицию для яблока в пределах игрового поля."""
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)
    
    def draw(self, surface):
        """
        Отрисовывает яблоко на игровом поле.
        
        Args:
            surface: Поверхность Pygame для отрисовки
        """
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Snake(GameObject):
    """
    Класс для представления змейки в игре.
    
    Наследуется от GameObject.
    
    Атрибуты:
        positions (list): Список координат сегментов змейки
        direction (tuple): Текущее направление движения
        next_direction (tuple): Следующее направление движения
        length (int): Текущая длина змейки
    """
    
    def __init__(self):
        """Инициализация змейки с зелёным цветом и начальной позицией."""
        super().__init__(body_color=GREEN)
        self.reset()
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        # Начальная позиция - центр экрана
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        
        self.positions = [(start_x, start_y)]
        self.direction = (CELL_SIZE, 0)  # Движение вправо
        self.next_direction = None
        self.length = 1
    
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Проверка, чтобы змейка не могла двигаться в противоположном направлении
            opposite_x = self.direction[0] * -1
            opposite_y = self.direction[1] * -1
            
            if not (self.next_direction[0] == opposite_x and
                    self.next_direction[1] == opposite_y):
                self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        """Перемещает змейку на одну ячейку в текущем направлении."""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        
        # Вычисляем новую позицию головы
        new_x = head_x + dir_x
        new_y = head_y + dir_y
        
        # Проверка выхода за границы поля (телепортация)
        if new_x < 0:
            new_x = (GRID_WIDTH - 1) * CELL_SIZE
        elif new_x >= WINDOW_WIDTH:
            new_x = 0
        elif new_y < 0:
            new_y = (GRID_HEIGHT - 1) * CELL_SIZE
        elif new_y >= WINDOW_HEIGHT:
            new_y = 0
        
        # Добавляем новую голову
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        
        # Удаляем хвост, если длина змейки не увеличилась
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def draw(self, surface):
        """
        Отрисовывает змейку на игровом поле.
        
        Args:
            surface: Поверхность Pygame для отрисовки
        """
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
            
            # Рисуем глаза у головы
            if i == 0:
                # Определяем направление для правильного размещения глаз
                dir_x, dir_y = self.direction
                eye_size = CELL_SIZE // 5
                
                # Горизонтальное движение
                if dir_x != 0:
                    # Глаза сверху и снизу
                    pygame.draw.rect(
                        surface,
                        BLACK,
                        pygame.Rect(
                            pos[0] + CELL_SIZE // 3,
                            pos[1] + CELL_SIZE // 4,
                            eye_size,
                            eye_size
                        )
                    )
                    pygame.draw.rect(
                        surface,
                        BLACK,
                        pygame.Rect(
                            pos[0] + CELL_SIZE // 3,
                            pos[1] + 3 * CELL_SIZE // 4 - eye_size,
                            eye_size,
                            eye_size
                        )
                    )
                # Вертикальное движение
                else:
                    # Глаза слева и справа
                    pygame.draw.rect(
                        surface,
                        BLACK,
                        pygame.Rect(
                            pos[0] + CELL_SIZE // 4,
                            pos[1] + CELL_SIZE // 3,
                            eye_size,
                            eye_size
                        )
                    )
                    pygame.draw.rect(
                        surface,
                        BLACK,
                        pygame.Rect(
                            pos[0] + 3 * CELL_SIZE // 4 - eye_size,
                            pos[1] + CELL_SIZE // 3,
                            eye_size,
                            eye_size
                        )
                    )
    
    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        
        Returns:
            tuple: Координаты головы змейки (x, y)
        """
        return self.positions[0]
    
    def grow(self):
        """Увеличивает длину змейки на 1."""
        self.length += 1


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для управления змейкой.
    
    Args:
        snake (Snake): Объект змейки для управления
    
    Returns:
        bool: False если игра должна быть завершена, иначе True
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (CELL_SIZE, 0)
    return True


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    # Создание объектов игры
    snake = Snake()
    apple = Apple()
    
    running = True
    
    # Главный игровой цикл
    while running:
        # Обработка событий
        running = handle_keys(snake)
        
        # Обновление направления движения змейки
        snake.update_direction()
        
        # Перемещение змейки
        snake.move()
        
        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            
            # Убедимся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # Проверка столкновения змейки с самой собой
        head_pos = snake.get_head_position()
        if head_pos in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
        
        # Отрисовка
        screen.fill(BLACK)
        
        # Отрисовка сетки (опционально)
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (20, 20, 20), (0, y), (WINDOW_WIDTH, y))
        
        # Отрисовка игровых объектов
        apple.draw(screen)
        snake.draw(screen)
        
        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Счет: {snake.length - 1}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Обновление экрана
        pygame.display.update()
        
        # Контроль скорости игры
        clock.tick(10)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
