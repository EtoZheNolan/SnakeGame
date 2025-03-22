import random
from threading import Thread
from time import sleep

from pynput import keyboard
from pynput.keyboard import Key

empty = '.'
snake = 'o'
food = '*'
score = 0
x, y = 20, 10

def game_over():
    print("Game over!")
    print("Your score: ", score)
    input("Press enter to continue...")
    exit()

def create_snake(head, tail_size):
    result = [head]

    for i in range(tail_size):
        result.append([result[-1][0] - 1, result[-1][1]])

    return result


def make_field(x, y):
    lines = [list(empty) * x for _ in range(y)]
    return lines


def place_snake(field, list_of_places):
    for place in list_of_places:
        field[place[1]][place[0]] = snake

    return field


def place_food(field, place):
    field[place[1]][place[0]] = food
    return field


def draw_field(field):
    for row in field:
        print(''.join(row))


def move_snake(snake_place, snake_direction):
    global food_place, snake_places, field, score

    new_head = []
    prev_head = snake_place[0]
    near_tail = snake_place[1]

    if snake_direction == Key.up:
        new_head = [prev_head[0], prev_head[1] - 1]

    if snake_direction == Key.down:
        new_head = [prev_head[0], prev_head[1] + 1]

    if snake_direction == Key.left:
        new_head = [prev_head[0] - 1, prev_head[1]]

    if snake_direction == Key.right:
        new_head = [prev_head[0] + 1, prev_head[1]]

    if new_head[0] == near_tail[0] and new_head[1] == near_tail[1]:
        return False

    if new_head[0] == x or new_head[1] == y or new_head[0] < 0 or new_head[1] < 0:
        game_over()

    if new_head[0] == food_place[0] and new_head[1] == food_place[1]:
        snake_places.append(new_head)
        print("\033[H")
        field, snake_places, food_place = build(20, 10, snake_places)
        draw_field(field)
        score += 1
        return False

    copy_places = snake_place.copy()

    for i in range(1, len(snake_place)):
        snake_place[i] = copy_places[i - 1]

    snake_place[0] = new_head
    return True


def build(x, y, snake_places_param=None, fool_place_param=None):
    field_local = make_field(x, y)

    tail_size = 3

    if fool_place_param is None:
        fool_place_param = [random.randint(0, x - 1), random.randint(0, y - 1)]

    place_food(field_local, fool_place_param)

    if snake_places_param is None:
        snake_head = [x // 2, y // 2]
        snake_places_param = create_snake(snake_head, tail_size)

    place_snake(field_local, snake_places_param)

    return field_local, snake_places_param, fool_place_param


field, snake_places, food_place = build(x, y)
draw_field(field)
last_direction = Key.right


def snake_move_itself():
    global field, snake_places, food_place, last_direction, score
    while True:

        result = move_snake(snake_places, last_direction)
        if result:
            print("\033[H")
            field, snake_places, food_place = build(x, y, snake_places, food_place)
            draw_field(field)
            sleep(0.5)



thread = Thread(target=snake_move_itself)
thread.start()

def on_key_release(key):
    global field, snake_places, food_place, last_direction

    key_pressed = None

    if key == Key.right:
        key_pressed = Key.right
    elif key == Key.left:
        key_pressed = Key.left
    elif key == Key.up:
        key_pressed = Key.up
    elif key == Key.down:
        key_pressed = Key.down
    elif key == Key.esc:
        exit()

    if key_pressed is not None:
        result = move_snake(snake_places, key_pressed)
        last_direction = key_pressed

        if result:
            print("\033[H")
            field, snake_places, food_place = build(x, y, snake_places, food_place)

            draw_field(field)



with keyboard.Listener(on_release=on_key_release) as listener:
    listener.join()
