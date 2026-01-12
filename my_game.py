"""
------------------------------------------------------------
 Script Name:        My_Game.py

 Description:        This script implements a 2D arcade-style
                     car dodging game using the Pygame library.
                     The player controls a car on a vertical road
                     and must avoid incoming enemy vehicles while
                     surviving as long as possible.
                     The game includes the following features:
                     1. Player-controlled car movement using
                        keyboard arrow keys.
                     2. Randomly spawned enemy cars with increasing
                        speed difficulty over time.
                     3. Collision detection between player and
                        enemy vehicles.
                     4. A life system represented by hearts.
                     5. A timer and record system that tracks the
                        longest survival time.
                     6. Visual assets including background, cars,
                        and heart icons.

 Author:             Razmik Bazeyan
 Created On:         01.10.2025
 Last Modified:      09.10.2026

 Version:            1.0
 Python Version:     3.x

 Usage:
     python Road_Car_Dodge_Game.py

 Dependencies:
     - pygame
     - sys
     - random
     - time

 Assets Required:
     - road.png     (background image)
     - car.png      (player vehicle)
     - car1.png     (enemy vehicle 1)
     - car2.png     (enemy vehicle 2)
     - heart.png    (life indicator)

 Notes:
     - All image assets must be located in the same directory
       as the script unless absolute paths are specified.
     - The game difficulty increases automatically over time.
     - The record time is stored in memory for the session.
     - This project is intended for learning game development
       concepts such as collision detection and game loops.
------------------------------------------------------------
"""
import pygame
import sys
import random
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Road with Car")

clock = pygame.time.Clock()

background = pygame.image.load("road.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


CAR_WIDTH = 80
CAR_HEIGHT = 100

player_car = pygame.image.load("car.png").convert_alpha()
player_car = pygame.transform.scale(player_car, (CAR_WIDTH, CAR_HEIGHT))

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - CAR_HEIGHT - 40
player_speed = 5


ROAD_LEFT = 150
ROAD_RIGHT = 650

#
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 100

enemy_images = [
    pygame.transform.scale(pygame.image.load("car1.png").convert_alpha(), (ENEMY_WIDTH, ENEMY_HEIGHT)),
    pygame.transform.scale(pygame.image.load("car2.png").convert_alpha(), (ENEMY_WIDTH, ENEMY_HEIGHT))
]

enemy_cars = []

def spawn_enemy(img):
    while True:
        x = random.randint(ROAD_LEFT, ROAD_RIGHT - ENEMY_WIDTH)
        y = random.randint(-600, -100)
        speed = random.randint(3, 6)

        too_close = False
        for e in enemy_cars:
            if abs(x - e["x"]) < ENEMY_WIDTH + 30 and abs(y - e["y"]) < ENEMY_HEIGHT + 30:
                too_close = True
                break

        if not too_close:
            return {
                "image": img,
                "x": x,
                "y": y,
                "speed": speed
            }


for img in enemy_images:
    enemy_cars.append(spawn_enemy(img))

hearts = 3
game_over = False

font_big = pygame.font.SysFont(None, 80)
font_small = pygame.font.SysFont(None, 36)


start_time = time.time()
elapsed_time = 0

speed_multiplier = 1.0
SPEED_INTERVAL = 10
last_speed_increase = 0

top_time = 0

def update_top_time(current_time):
    global top_time
    if current_time > top_time:
        top_time = current_time


heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (40, 40))

def respawn_player():
    global player_x, player_y
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - CAR_HEIGHT - 40

def show_timer(seconds):
    text = font_small.render(f"Time: {int(seconds)}s", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 160, 10))

def show_top_time():
    text = font_small.render(f"Record: {top_time}s", True, (255, 215, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - 80, 10))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        elapsed_time = time.time() - start_time


        if elapsed_time - last_speed_increase >= SPEED_INTERVAL:
            speed_multiplier += 0.2
            last_speed_increase = elapsed_time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

    
    player_x = max(ROAD_LEFT, min(ROAD_RIGHT - CAR_WIDTH, player_x))
    player_y = max(0, min(SCREEN_HEIGHT - CAR_HEIGHT, player_y))

    player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH, CAR_HEIGHT)

   
    if not game_over:
        for enemy in enemy_cars:
            enemy["y"] += enemy["speed"] * speed_multiplier
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], ENEMY_WIDTH, ENEMY_HEIGHT)

            
            if player_rect.colliderect(enemy_rect):
                hearts -= 1
                respawn_player()
                enemy.update(spawn_enemy(enemy["image"]))

                if hearts <= 0:
                    update_top_time(int(elapsed_time))
                    game_over = True

            
            if enemy["y"] > SCREEN_HEIGHT + 150:
                enemy.update(spawn_enemy(enemy["image"]))

   
    screen.blit(background, (0, 0))

    for enemy in enemy_cars:
        screen.blit(enemy["image"], (enemy["x"], enemy["y"]))

    screen.blit(player_car, (player_x, player_y))

    
    for i in range(hearts):
        screen.blit(heart_img, (10 + i * 45, 10))

    show_timer(elapsed_time)
    show_top_time()

    if game_over:
        text = font_big.render("GAME OVER", True, (255, 0, 0))
        screen.blit(
            text,
            (SCREEN_WIDTH // 2 - text.get_width() // 2,
             SCREEN_HEIGHT // 2 - text.get_height() // 2)
        )

    pygame.display.flip()
    clock.tick(60)
