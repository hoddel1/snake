import pygame
import random
import sys

pygame.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Изгиб Питона')
clock = pygame.time.Clock()


class GameObject:

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        pass


class Apple(GameObject):

    def __init__(self):
        super().__init__(body_color=RED)
        self.randomize_position()

    def randomize_position(self):
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Snake(GameObject):
    def __init__(self):
        super().__init__(body_color=GREEN)
        self.reset()

    def reset(self):
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE

        self.positions = [(start_x, start_y)]
        self.direction = (CELL_SIZE, 0)  # Движение вправо
        self.next_direction = None
        self.length = 1

    def update_direction(self):
        if self.next_direction:
            opposite_x = self.direction[0] * -1
            opposite_y = self.direction[1] * -1

            if not (self.next_direction[0] == opposite_x and
                    self.next_direction[1] == opposite_y):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction

        new_x = head_x + dir_x
        new_y = head_y + dir_y

        if new_x < 0:
            new_x = (GRID_WIDTH - 1) * CELL_SIZE
        elif new_x >= WINDOW_WIDTH:
            new_x = 0
        elif new_y < 0:
            new_y = (GRID_HEIGHT - 1) * CELL_SIZE
        elif new_y >= WINDOW_HEIGHT:
            new_y = 0

        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

            if i == 0:
                dir_x, dir_y = self.direction
                eye_size = CELL_SIZE // 5

                if dir_x != 0:
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
                else:
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
        return self.positions[0]

    def grow(self):
        self.length += 1


def handle_keys(snake):
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
    snake = Snake()
    apple = Apple()

    running = True

    while running:
        running = handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        head_pos = snake.get_head_position()
        if head_pos in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        screen.fill(BLACK)

        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(
                screen, (20, 20, 20), (x, 0), (x, WINDOW_HEIGHT)
            )
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(
                screen, (20, 20, 20), (0, y), (WINDOW_WIDTH, y)
            )

        apple.draw(screen)
        snake.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(
            f'Счет: {snake.length - 1}', True, (255, 255, 255)
        )
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main())
