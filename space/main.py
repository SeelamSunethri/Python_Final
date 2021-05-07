import pygame
import os
import time
import sys
import math
import random

class Hero:

    def __init__(self, game, x_loc, y_loc, player_icon = None):

        self.game = game
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.player_icon = player_icon

    def draw(self):
        self.game.screen.blit(self.player_icon, (self.x_loc,self.y_loc))

class Astroid:

    def __init__(self, game):
        self.game = game
        self.x1 = 70
        self.x2 = 260
        self.x3 = 480
        self.x4 = 650
        self.y1 = 550
        self.y2 = 510
        self.y3 = 540
        self.y4 = 560
        self.all_loc = [(self.x1, self.y1), (self.x2, self.y2),(self.x3, self.y3),(self.x4, self.y4)]
        script_path = os.getcwd()
        images_path = f"{script_path}\images"
        images = []
        images.append(pygame.image.load(f"{images_path}\\aa.png"))
        images.append(pygame.image.load(f"{images_path}\\aa1.png"))
        images.append(pygame.image.load(f"{images_path}\\aa2.png"))
        images.append(pygame.image.load(f"{images_path}\\aa3.png"))
        self.game.screen.blit(images[0], (self.x1, self.y1))
        self.game.screen.blit(images[1], (self.x2, self.y2))
        self.game.screen.blit(images[2], (self.x3, self.y3))
        self.game.screen.blit(images[3], (self.x4, self.y4))


class Alien:

    def __init__(self, game, x_loc, y_loc, dead_alien = None):

        self.game = game
        self.co_ordinates = {}
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.dead_alien = [] if dead_alien is None else dead_alien

        script_path = os.getcwd()
        images_path = f"{script_path}\images"
        self.images = []

        self.images.append(pygame.image.load(f"{images_path}\\alien.png"))
        self.images.append(pygame.image.load(f"{images_path}\\alien_2.png"))
        self.images.append(pygame.image.load(f"{images_path}\\alien_3.png"))
        self.images.append(pygame.image.load(f"{images_path}\\alien_4.png"))
        self.images.append(pygame.image.load(f"{images_path}\\alien_4.png"))

    def draw_aliens(self):
        if self.y_loc == 80:
            self.game.screen.blit(self.images[0], (self.x_loc, self.y_loc))
        elif self.y_loc == 140:
            self.game.screen.blit(self.images[1], (self.x_loc, self.y_loc))
        elif self.y_loc == 200:
            self.game.screen.blit(self.images[2], (self.x_loc, self.y_loc))
        else:
            self.game.screen.blit(self.images[3], (self.x_loc, self.y_loc))


class Rocket:
    def __init__(self, game, x, y, height):
        self.x = x
        self.y = y
        self.x_attack = 100
        self.y_attack = 100
        self.game = game
        self.height = height


    def fire(self):
        if self.y-2 >= 0:
            pygame.draw.rect(self.game.screen,
                         (255, 255, 255),
                         pygame.Rect(self.x+24, self.y, 2, 20))
            self.y -= 4

    def defetect_collision(self, aliens):
        dead_alien = False
        if aliens == -1:
            return [], -1
        for alien in aliens:
            if (15.622776601683796 <= math.dist(((alien.x_loc, alien.y_loc)), (self.x, self.y)) <= 27.568542494923804):
                dead_alien = True
                aliens.remove(alien)
                if len(aliens) == 0:
                    return -1, -1
                break
        return aliens, dead_alien

    def detect_hero_collision(self, player_x, player_y):
        dead = False
        if (15.622776601683796 <= math.dist(((player_x, player_y)), (self.x, self.y)) <= 27.568542494923804):
            dead = True
        return dead

    def detect_astroid_collision(self, astroids):
        blast = False
        for x, y in astroids.all_loc:
            if (30.622776601683796 <= math.dist(((x, y)), (self.x, self.y)) <= 50.568542494923804):
                blast = True
        return blast

    def alien_attack(self):
        if self.y <= self.height:
            pygame.draw.rect(self.game.screen,
                         (255, 0, 0),
                         pygame.Rect(self.x, self.y, 2, 20))
            self.y += 2

class SpaceInvader:

    screen = None
    aliens = []
    rockets = []
    background = None
    script_path = os.getcwd()
    images_path = f"{script_path}\images"

    def game_settings(self):

        # GAME SPEED
        self.game_speed = 40

        # IMAGES
        self.background = pygame.image.load(f"{self.images_path}\\bg.jpg")
        self.player_image = pygame.image.load(f"{self.images_path}\\player.png")
        self.player_lives = pygame.image.load(f"{self.images_path}\\life.png")

        # GAME SIZE
        self.width = 900
        self.height = 700

    def generate_aliens(self, total_rows):

        row = 0
        total_rows =  3 + total_rows
        for y_loc in range(80, int(self.height / 2), 60):
            self.co_ordinates[str(row)] = []
            for x_loc in range(self.x_loc_start, self.x_loc_end, 71):
                self.co_ordinates[str(row)].append((x_loc, y_loc))
                self.aliens.append(Alien(self, x_loc, y_loc))
            if row == total_rows:
                break
            else:
                row = row + 1
                continue

        self.create_aliens = True

    def restart_game(self):
        self.game_state = "Running"
        self.player_score = 0
        self.player_life_count = 3
        self.aliens = []
        self.attacks = []
        self.bullets_fired = False
        self.create_aliens = False

    def __init__(self):

        pygame.init()
        pygame.font.init()

        # FETCH GAME SETTINGS
        self.game_settings()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.game_over_font = pygame.font.SysFont('Comic Sans MS', 70)

        # Game Status
        self.game_status = "running"

        # player start co-ordinates
        player_x_loc = self.width / 2
        player_y_loc = self.height - 50
        self.rockets = []
        self.bullets_fired = False
        self.create_aliens = False
        self.x_loc_start = 50
        self.x_loc_end = self.width - 100
        self.alien_direction = "Forward"
        self.player_life_count = 3
        self.player_score = 0
        self.dead_aliens = []
        self.all_aliens = []
        self.attacks = []
        self.move = 80
        self.confirm_dead = []
        self.move_end = 60
        self.game_level = 0
        self.co_ordinates = {}
        self.game_state = "Running"
        self.astroids = None

        delay = 0

        while self.game_status == "running":

            self.screen.fill((0, 0, 0))

            # BACKGROUND IMAGE
            self.screen.blit(self.background, (0, 0))

            # GAME INFO
            player_lifes = self.font.render('Lives: ', False, (255, 255, 255))
            player_score = self.font.render(f'Score: {self.player_score}', False, (255, 255,255))
            self.screen.blit(player_lifes, (600, 5))
            self.screen.blit(player_score, (20, 5))

            if self.player_life_count == 1:
                self.screen.blit(self.player_lives, (700, 10))
            if self.player_life_count == 2:
                self.screen.blit(self.player_lives, (700, 10))
                self.screen.blit(self.player_lives, (750, 10))
            if self.player_life_count == 3:
                self.screen.blit(self.player_lives, (700, 10))
                self.screen.blit(self.player_lives, (750, 10))
                self.screen.blit(self.player_lives, (800, 10))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.game_status = "completed"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bullets_fired = True
                    self.rockets.append(Rocket(self, player_x_loc, player_y_loc, self.height))

            for rockets in self.rockets:
                rockets.fire()

            pressed = pygame.key.get_pressed()

            if self.game_state == "WON":
                game_state_won = self.game_over_font.render('Aliens Destroyed', False, (255, 255, 255))
                restart = self.game_over_font.render(f'LEVEL {self.game_level+1} ', False, (255, 255, 255))
                continue_game = self.game_over_font.render('press space to continue ', False, (255, 255, 255))
                alien_attack_speed = self.game_over_font.render(f'Alien attack speed: {100-self.game_speed} ', False, (255, 255, 255))
                self.screen.blit(game_state_won, (170, self.height/2 - 50))
                self.screen.blit(restart, (350, self.height/2 + 20 ))
                self.screen.blit(continue_game, (90, self.height/2 + 80 ))
                self.screen.blit(alien_attack_speed, (90, self.height / 2 + 130))
                time.sleep(0.01)
                pygame.display.update()

                if pressed[pygame.K_SPACE]:
                    self.game_level += 1
                    previous_lvl_score = self.player_score
                    previous_lvl_lives = self.player_lives
                    self.restart_game()
                    self.player_score = previous_lvl_score
                    self.player_lives = previous_lvl_lives
                    self.game_speed -= 5
                continue
                #self.restart_game()

            if self.game_state == "Running":

                if pressed[pygame.K_LEFT]:
                    player_x_loc -= 8 if player_x_loc > 0 else 0

                elif pressed[pygame.K_RIGHT]:
                    player_x_loc += 8 if player_x_loc < self.width - 50 else 0

            else:

                game_state = self.game_over_font.render('GAME OVER', False, (255, 255, 255))
                restart = self.game_over_font.render('Press R to Restart', False, (255, 255, 255))
                self.screen.blit(game_state, (250, self.height/2 - 50))
                self.screen.blit(restart, (160, self.height/2 + 20 ))
                self.game_state = "GAME OVER"

                if pressed[pygame.K_r]:
                    self.restart_game()

            hero = Hero(self, player_x_loc, player_y_loc, player_icon=self.player_image)
            hero.draw()

            if self.create_aliens == False:
                self.generate_aliens(self.game_level)

            self.astroids= Astroid(self)

            if (self.aliens) == 0:
                continue

            for alien in self.aliens:
                alien.draw_aliens()

            else:

                for alien in self.aliens:
                    if (self.alien_direction == "Forward") & (alien.x_loc <= self.width - 100):
                        alien.x_loc += 0.5
                    else:
                        self.alien_direction = "Backward"
                    if (self.alien_direction == "Backward") & (alien.x_loc >= 51):
                        alien.x_loc -= 0.5
                    else:
                        self.alien_direction = "Forward"

            for alien in self.aliens:
                alien.draw_aliens()


            if (self.aliens) != 0:
                self.random_alien_attack = random.randint(2, self.game_speed)
                if self.random_alien_attack == 6:
                    try:
                        self.random_alien_attack = random.randint(1, len(self.aliens))
                        attacking_alien = self.aliens[self.random_alien_attack]
                        self.attacks.append(Rocket(self, attacking_alien.x_loc + 10, attacking_alien.y_loc + 40, self.height))
                    except Exception as e:
                        pass # Attacking alien dead
            else:
                continue

            if (self.aliens) == 0:
                continue
            for attack in self.attacks:
                attack.alien_attack()
                dead = attack.detect_hero_collision(player_x_loc, player_y_loc)
                astroid_collision = attack.detect_astroid_collision(self.astroids)

                if astroid_collision:
                    self.attacks.remove(attack)

                if dead:
                    self.player_life_count -= 1
                    player_x_loc = self.width / 2
                    player_y_loc = self.height - 50

                if self.player_life_count == 0:
                    self.game_state = "GAME OVER"

            if (self.aliens) == 0:
                continue
            if self.bullets_fired:
                for rocket in self.rockets:
                    self.aliens,dead = rocket.defetect_collision(self.aliens)
                    astroid_collision = rocket.detect_astroid_collision(self.astroids)

                    if dead == -1:
                        self.game_state = "WON"
                        continue
                    if dead == True:
                        self.aliens = self.aliens[0:8]
                        self.rockets.remove(rocket)
                        self.player_score += 10

                    if astroid_collision:
                        self.rockets.remove(rocket)
            time.sleep(0.01)
            pygame.display.update()

if __name__ == '__main__':
    space_invader = SpaceInvader()

