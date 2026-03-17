"""Простая игра 'Змейка' на Pygame."""

from random import randint
import pygame
from typing import Optional, List, Tuple

# --- Константы размеров поля и сетки ---
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# --- Направления движения ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Цвета ---
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# --- Скорость (FPS) ---
SPEED = 20


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position: Tuple[int, int] = (0, 0),
        body_color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """Инициализация базового игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:
        """Абстрактный метод отрисовки."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(
        self,
        position: Tuple[int, int] = (0, 0),
        body_color: Tuple[int, int, int] = APPLE_COLOR,
    ) -> None:
        """Создаёт яблоко в случайной позиции."""
        super().__init__(position, body_color)
        self.randomize_position([])

    def randomize_position(
        self, exclude_positions: Optional[List[Tuple[int, int]]] = None
    ) -> Tuple[int, int]:
        """Ставит яблоко в случайную свободную клетку."""
        if exclude_positions is None:
            exclude_positions = []

        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in exclude_positions:
                self.position = (x, y)
                return self.position

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(
        self,
        position: Tuple[int, int] = (0, 0),
        body_color: Tuple[int, int, int] = SNAKE_COLOR,
    ) -> None:
        """Создаёт змейку в центре поля."""
        super().__init__(position, body_color)
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.length = 1
        self.positions: List[Tuple[int, int]] = [(start_x, start_y)]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.last_removed: Optional[Tuple[int, int]] = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Передвигает змейку на одну клетку."""
        head_x, head_y = self.positions[0]
        new_x = (head_x // GRID_SIZE + self.direction[0]) % GRID_WIDTH
        new_y = (head_y // GRID_SIZE + self.direction[1]) % GRID_HEIGHT
        new_head = (new_x * GRID_SIZE, new_y * GRID_SIZE)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last_removed = self.positions.pop()
        else:
            self.last_removed = None

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку."""
        if self.last_removed:
            last_rect = pygame.Rect(self.last_removed, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        start_x = (GRID_WIDTH // 2) * GRID_SIZE
        start_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last_removed = None


# --- Инициализация pygame и глобальных объектов ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Змейка")


def handle_keys(game_object: Snake) -> None:
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
