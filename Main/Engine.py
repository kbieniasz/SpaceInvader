import sys
import pygame
import random
from Main.vector import Vector
from Main.Player import Player
from Main.enemy import Enemy
from Main.star import Star
from Main.missile_wrapper import MissileWrapper


class Engine:
    def __init__(self, screen):
        self.screen = screen
        self.stars = [Star(screen) for x in range(200)]

    def player_prefab(self):
        return Player(pygame.Rect(0, 0, 30, 30), 9, (0, 255, 0))

    def enemy_prefab(self, pos):
        return Enemy(pygame.Rect(pos[0], pos[1], 30, 30))

    def run_single(self):
        player1 = self.player_prefab()
        buff = list(player1.controls)
        buff[4] = -1
        player1.controls = tuple(buff)
        enemies = [self.enemy_prefab((random.randrange(0, self.screen.get_width(), 1), -30))]
        timer = 0

        missile_wrapper = MissileWrapper()

        while True:
            d_time = pygame.time.Clock().tick(60)
            if len(enemies) < 8:
                timer += d_time
                if timer > 1500:
                    enemies.append(self.enemy_prefab((random.randrange(0, self.screen.get_width(), 1), -30)))
                    timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            self.screen.fill((0, 0, 0))
            missile_wrapper.add_from_player(player1.shoot())
            player1.update_mouse(pygame.mouse.get_pos(), d_time)
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)

            missile_wrapper.update(self.screen)

            for e in enemies:
                missile_wrapper.add_from_enemy(e.update(player1.center, d_time))
                e.draw(self.screen)

            enemies = [e for e in enemies if not missile_wrapper.enemy_hit(e)]
            missile_wrapper.player_hit(player1)
            missile_wrapper.draw(self.screen)
            player1.draw(self.screen)

            pygame.display.flip()

    def run_multi(self):
        player1 = self.player_prefab()
        player2 = self.player_prefab()
        player2.controls = (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_TAB)
        player2.color = (0, 155, 155)
        enemies = [self.enemy_prefab((random.randrange(0, self.screen.get_width(), 1), -30))]
        timer = 0

        missile_wrapper = MissileWrapper()

        while True:
            d_time = pygame.time.Clock().tick(60)
            if len(enemies) < 8:
                timer += d_time
                if timer > 1500:
                    enemies.append(self.enemy_prefab((random.randrange(0, self.screen.get_width(), 1), -30)))
                    timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)

            self.screen.fill((0, 0, 0))
            missile_wrapper.add_from_player(player1.shoot())
            missile_wrapper.add_from_player(player2.shoot())
            player1.update_keyboard(d_time, self.screen)
            player2.update_keyboard(d_time, self.screen)
            for s in self.stars:
                s.update(self.screen)
                s.draw(self.screen)

            missile_wrapper.update(self.screen)

            for e in enemies:
                dp1 = Vector(player1.center[0] - e.center[0], player1.center[1] - e.center[1])
                dp2 = Vector(player2.center[0] - e.center[0], player2.center[1] - e.center[1])
                if dp1.magnitude() > dp2.magnitude():
                    missile_wrapper.add_from_enemy(e.update(player2.center, d_time))
                else:
                    missile_wrapper.add_from_enemy(e.update(player1.center, d_time))
                e.draw(self.screen)

            enemies = [e for e in enemies if not missile_wrapper.enemy_hit(e)]
            missile_wrapper.player_hit(player1)
            missile_wrapper.player_hit(player2)
            missile_wrapper.draw(self.screen)
            player1.draw(self.screen)
            player2.draw(self.screen)
            pygame.display.flip()



