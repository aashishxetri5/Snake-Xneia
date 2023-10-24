import pygame
import random

WIDTH, HEIGHT = 600, 600
SNAKE_SIZE = FOOD_SIZE = 10
SNAKE_SPEED = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class SnakeGame:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.snake = Snake(self)
        self.food = Food(self)
        self.score = 0

    def increase_speed(self):
        global SNAKE_SPEED
        SNAKE_SPEED += 1

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Xenia")

        clock = pygame.time.Clock()
        moving = True

        while moving:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    moving = False

            keys = pygame.key.get_pressed()
            self.snake.handle_keys(keys)

            self.snake.move()
            self.snake.check_collision_food(self.food)
            self.snake.check_boundaries()

            screen.fill(BLACK)
            self.snake.draw(screen)
            self.food.draw(screen)
            self.display_score(screen)

            pygame.display.update()
            clock.tick(SNAKE_SPEED)

        pygame.quit()

    def display_score(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))


class Snake:
    def __init__(self, game):
        self.game = game
        self.body = [
            (100, 50),
            (90, 50),
            (80, 50),
        ]  # Position of snake as [head, mid, tail]
        self.direction = "RIGHT"
        self.foods_eaten = 0

    def move(self):
        x, y = self.body[0]
        if self.direction == "RIGHT":
            new_head = (x + SNAKE_SIZE, y)
        if self.direction == "LEFT":
            new_head = (x - SNAKE_SIZE, y)
        if self.direction == "UP":
            new_head = (x, y - SNAKE_SIZE)
        if self.direction == "DOWN":
            new_head = (x, y + SNAKE_SIZE)

        self.body.insert(0, new_head)

        if self.check_collision_self():  # Check for self-collision
            pass

        if self.body[0] == self.game.food.position:
            self.game.score += 1
            self.game.food.randomize_position()
            self.foods_eaten += 1
            self.game.increase_speed()  # Call a new method to increase speed

        else:
            self.body.pop()

    # Checks if snake has collided with itself
    def check_collision_self(self):
        return self.body[0] in self.body[1:]

    def handle_keys(self, keys):
        if keys[pygame.K_RIGHT] and self.direction != "LEFT":
            self.direction = "RIGHT"
        if keys[pygame.K_LEFT] and self.direction != "RIGHT":
            self.direction = "LEFT"
        if keys[pygame.K_UP] and self.direction != "DOWN":
            self.direction = "UP"
        if keys[pygame.K_DOWN] and self.direction != "UP":
            self.direction = "DOWN"

    # Checks whether snake has eaten the food.
    def check_collision_food(self, food):
        if self.body[0] == food.position:
            food.randomize_position()

    def check_boundaries(self):
        head = self.body[0]
        if (
            head[0] >= self.game.width
            or head[0] < 0
            or head[1] >= self.game.height
            or head[1] < 0
        ):
            pygame.quit()
            exit()

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(
                screen, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE)
            )


class Food:
    def __init__(self, game):
        self.game = game
        self.position = (
            random.randrange(1, (game.width // FOOD_SIZE)) * FOOD_SIZE,
            random.randrange(1, (game.height // FOOD_SIZE)) * FOOD_SIZE,
        )

    def randomize_position(self):
        self.position = (
            random.randrange(1, (self.game.width // FOOD_SIZE)) * FOOD_SIZE,
            random.randrange(1, (self.game.height // FOOD_SIZE)) * FOOD_SIZE,
        )

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (*self.position, FOOD_SIZE, FOOD_SIZE))


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
