from machine import Pin
from neopixel import NeoPixel

from time import sleep
from random import randint
from sys import exit

from lib.colors import *
from lib.index_converting import coords_to_linear, linear_to_coords, convert_index
from lib.transitions import transition
from lib.letters_on_mx import show


# the mx
mx = NeoPixel(Pin(0), 256)


# W, A, S, D buttons

w_button = Pin(9, Pin.IN, Pin.PULL_UP)
a_button = Pin(8, Pin.IN, Pin.PULL_UP)
s_button = Pin(7, Pin.IN, Pin.PULL_UP)
d_button = Pin(6, Pin.IN, Pin.PULL_UP)


class Snake:

    def __init__(self, mx, snake_color, time, mx_width=8, delay=.25):
        # mx attribues
        self.mx = mx
        self.mx_width = mx_width
        self.mx_height = self.mx.n//self.mx_width
        # about direction
        self.direction = "forward"
        self.direction_dict = {"forward":(1, 0),
                               "backward":(-1, 0),
                               "left":(0, 1),
                               "right":(0, -1)
                               }
        # snake attributes
        self.snake_color = snake_color
        self.snake_lenght = 10
        self.snake_tail = [(i, 0) for i in range(self.snake_lenght)]
        # technical stuff
        self.delay = delay
        self.time = time
        # apples
        self.apple_color = RED
        self.apple_spawn_chances = 1, 20
        self.apples = list()
        # score
        self.score = 0
        # all time hight score
        with open("best_score_for_snake.txt", "r") as f:
            self.best_score = int(f.read())


    def game_over(self):
        # checking to see if there is a new high score
        if self.score > self.best_score:
            self.best_score = self.score
            # if there is, remember it in a file
            with open("best_score_for_snake.txt", "w") as f:
                f.write(str(self.score))

        # clear the mx
        mx.fill(BLACK)
        mx.write()

        sleep(2)

        # show the score and the best score
        for intensity in transition(self.mx, BLACK, DARK_RED):
            show(mx, "You died!", intensity)
            sleep(.05)
        for intensity in transition(self.mx, DARK_RED, BLACK):
            show(mx, "You died!", intensity)
            sleep(.05)

        for intensity in transition(self.mx, BLACK, DARK_RED):
            show(mx, "Score "+str(self.score), intensity)
            sleep(.05)
        for intensity in transition(self.mx, DARK_RED, BLACK):
            show(mx, "Score "+str(self.score), intensity)
            sleep(.05)

        for intensity in transition(self.mx, BLACK, DARK_RED):
            show(mx, "Best: "+str(self.best_score), intensity)
            sleep(.01)
        for intensity in transition(self.mx, DARK_RED, BLACK):
            show(mx, "Best: "+str(self.best_score), intensity)
            sleep(.01)

        # end the programm
        exit()

    # run the game
    def run(self):

        off_w_button_value = w_button.value()
        w_button_pressed = False

        off_a_button_value = w_button.value()
        a_button_pressed = False

        off_s_button_value = w_button.value()
        s_button_pressed = False

        off_d_button_value = w_button.value()
        d_button_pressed = False

        old_direction = self.direction


        # run the game until the timer runs out or you died
        while self.time > 0:

            # W button
            if off_w_button_value != w_button.value() and w_button_pressed is False:
                w_button_pressed = True
                self.direction = "forward" if self.direction != "backward" else self.direction
            if off_w_button_value == w_button.value():
                w_button_pressed = False
            # A button
            if off_a_button_value != a_button.value() and a_button_pressed is False:
                a_button_pressed = True
                self.direction = "right" if self.direction != "left" else self.direction
            if off_a_button_value == a_button.value():
                a_button_pressed = False

            # S button
            if off_s_button_value != s_button.value() and s_button_pressed is False:
                s_button_pressed = True
                self.direction = "backward" if self.direction != "forward" else self.direction
            if off_s_button_value == s_button.value():
                s_button_pressed = False

            # D button
            if off_d_button_value != d_button.value() and d_button_pressed is False:
                d_button_pressed = True
                self.direction = "left" if self.direction != "right" else self.direction
            if off_d_button_value == d_button.value():
                d_button_pressed = False


            # direction
            if self.direction != old_direction:
                old_direction = self.direction


            # calculating the next position of the snake's coords
            self.x = self.snake_tail[-1][0]
            self.y = self.snake_tail[-1][1]

            if self.x+self.direction_dict[self.direction][0] < 0:
                self.x = self.mx_height-1
            elif self.x+self.direction_dict[self.direction][0] > self.mx_height-1:
                self.x = 0
            else:
                self.x += self.direction_dict[self.direction][0]


            if self.y+self.direction_dict[self.direction][1] < 0:
                self.y = self.mx_width-1
            elif self.y+self.direction_dict[self.direction][1] > self.mx_width-1:
                self.y = 0
            else:
                self.y += self.direction_dict[self.direction][1]
            

            # "moving" the snake
            mx[convert_index(coords_to_linear(self.snake_tail[-1]))] = self.snake_color 
            mx[convert_index(coords_to_linear(self.snake_tail[0]))] = (0, 0, 0)

            self.snake_tail.pop(0)


            # checking to see if the snake touched itself
            if (self.x, self.y) not in self.snake_tail:
                self.snake_tail.append((self.x, self.y))
            
            else:
                mx.write()

                sleep(2)

                self.game_over()


            # spawning the apple
            if randint(self.apple_spawn_chances[0], self.apple_spawn_chances[1]) == 1:
                self.apple_coords = randint(0, mx.n-1)

                if self.apple_coords in self.apples:
                    while self.apple_coords in self.apples:
                        self.apple_coords = randint(0, mx.n)

                self.apple_coords = linear_to_coords(self.apple_coords)
                self.apples.append(self.apple_coords)

                mx[coords_to_linear(self.apple_coords)] = self.apple_color


            # increasing the game speed if the snake tail is longer that 25 pixels
            if self.snake_lenght > 25:
                self.delay = .1


            # checking to see if the snake ate an apple
            if self.snake_tail[-1] in self.apples:
                self.score += 1
                self.apples.remove(self.snake_tail[-1])

                self.x = self.snake_tail[0][0]
                self.y = self.snake_tail[0][1]

                if self.x-self.direction_dict[self.direction][0] < 0:
                    self.x = self.mx_height-1
                elif self.x-self.direction_dict[self.direction][0] > self.mx_height-1:
                    self.x = 0
                else:
                    self.x -= self.direction_dict[self.direction][0]

                self.snake_tail.insert(0, (self.x, self.y))
                self.snake_lenght = len(self.snake_tail)

            # rendering the snake
            for coords in self.snake_tail:
                mx[convert_index(coords_to_linear(coords))] = self.snake_color


            # rendering the matrix
            mx.write()


            # post-rendering the matrix
            sleep(self.delay)
            self.time -= self.delay



Snake(mx, GREEN, 5000).run()

