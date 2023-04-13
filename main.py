
# importing libraries
import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (100, 110, 5)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        # the image of the apple
        self.image = pygame.image.load("apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


# determines the apple appear (random)
# miltiply by size so that both the apple and the snake are on the same scales on both axis
    def move(self):
        self.x = random.randint(1, 6) * SIZE
        self.y = random.randint(1, 12) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        # one pixel of the snake
        self.image = pygame.image.load("block.jpg").convert()
        # the direction the snake moves when it starts
        self.direction = "right"

        self.length = 1
        self.x = [SIZE]
        self.y = [SIZE]

# defining keystrokes (making functions for each of them)

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

# update body after every change

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]


# update how the snake looks like after evrey key is pressed
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

            pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        # game caption found on the top of the screen
        pygame.display.set_caption("The Snake Game")

        pygame.mixer.init()
        self.play_background_music()
        # the size of the screen
        self.surface = pygame.display.set_mode((600, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        # background music file
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        # sound played when crashing
        if sound_name == "crash":
            sound = pygame.mixer.Sound("crash.mp3")

# sound played when eating an apple
        elif sound_name == "ding":
            sound = pygame.mixer.Sound("ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + SIZE:
            if y1 >= y2 and y1 <= y2 + SIZE:
                return True
        return False

# set the background to the background image

    def render_background(self):
        bg = pygame.image.load("background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x,
                             self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

# snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0],
                                 self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision Occurred"


# snake crashing on the boundaries
#if self.snake != pygame.display.set_mode (600,800):
#self.play_sound("crash")
#raise "Collision Occurred"
    def display_score(self):
        # setting the font and the size of the font
        font = pygame.font.SysFont("arial", 30)

        # keeps track of the score
        score = font.render(f"Score: {self.snake.length}", True,
                            (200, 200, 200))
        self.surface.blit(score, (10, 10))

    def show_game_over(self):
        self.render_background()

        # setting the font and the size of the font
        font = pygame.font.SysFont("arial", 25)

        # the location of the first line "Game over! Your score is: [score]"
        line1 = font.render(f"You Died! Your score: {self.snake.length}", True,
                            (255, 255, 255))

        self.surface.blit(line1, (100, 200))

        # the locations of the second line "To play again press enter. To exit press escape."
        line2 = font.render("To play again press Enter. To exit press Escape.",
                            True, (255, 255, 255))

        self.surface.blit(line2, (25, 300))

        # stop the music and change to end screen when the game is over
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        # keys
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)

if __name__ == "__main__":
    game = Game()
    game.run()