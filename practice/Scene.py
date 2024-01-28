import pygame
import Map
from Settings import *
from NPC import *
from Monster import *
from Bullet import *
from Portal import *

class Scene():
    def __init__(self, window):
        self.type = None

        self.cameraX = 0
        self.cameraY = 0
        self.map = None
        self.obstacles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

        self.window = window
        self.width = WindowSettings.width
        self.height = WindowSettings.height

    def get_width(self):
        return WindowSettings.width * WindowSettings.outdoorScale

    def get_height(self):
        return WindowSettings.height * WindowSettings.outdoorScale
    
    def get_camerax(self):
        return self.cameraX
    
    def get_cameray(self):
        return self.cameraY
    
    def update_camera(self,player,bullets, bossbullets, monsterbullets, monsters):
        if player.rect.x > WindowSettings.width / 4 * 3:
            self.cameraX += player.speed
            if self.cameraX < self.get_width() - WindowSettings.width:
                player.move(-player.speed, 0)
                for bullet in bullets:
                    bullet.move(-player.speed, 0)
                for bossbullet in bossbullets:
                    bossbullet.move(-player.speed, 0)
                for monsterbullet in monsterbullets:
                    monsterbullet.move(-player.speed, 0)
                for monster in monsters:
                    monster.move(-player.speed, 0)
                for obstacle in self.obstacles:
                    obstacle.rect.x -= player.speed
                
            else:
                self.cameraX = self.get_width() - WindowSettings.width
        elif player.rect.x < WindowSettings.width / 4:
            self.cameraX -= player.speed
            if self.cameraX > 0:
                player.move(player.speed, 0)
                for bullet in bullets:
                    bullet.move(player.speed, 0)
                for bossbullet in bossbullets:
                    bossbullet.move(player.speed, 0)
                for monsterbullet in monsterbullets:
                    monsterbullet.move(player.speed, 0)
                for monster in monsters:
                    monster.move(player.speed, 0)
                for obstacle in self.obstacles:
                    obstacle.rect.x += player.speed
            else:
                self.cameraX = 0
        if player.rect.y > WindowSettings.height / 4 * 3:
            self.cameraY += player.speed
            if self.cameraY < self.get_height() - WindowSettings.height:
                player.move(0, -player.speed)
                for bullet in bullets:
                    bullet.move(0, -player.speed)
                for bossbullet in bossbullets:
                    bossbullet.move(0, -player.speed)
                for monsterbullet in monsterbullets:
                    monsterbullet.move(0, -player.speed)
                for monster in monsters:
                    monster.move(0, -player.speed)
                for obstacle in self.obstacles:
                    obstacle.rect.y -= player.speed
            else:
                self.cameraY = self.get_height() - WindowSettings.height
        elif player.rect.y < WindowSettings.height / 4:
            self.cameraY -= player.speed
            if self.cameraY > 0:
                player.move(0, player.speed)
                for bullet in bullets:
                    bullet.move(0, player.speed)
                for bossbullet in bossbullets:
                    bossbullet.move(0, player.speed)
                for monsterbullet in monsterbullets:
                    monsterbullet.move(0, player.speed)
                for monster in monsters:
                    monster.move(0, player.speed)
                for obstacle in self.obstacles:
                    obstacle.rect.y += player.speed
            else:
                self.cameraY = 0

    def render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                                 (SceneSettings.tileWidth * i- self.cameraX, 
                                SceneSettings.tileHeight * j - self.cameraY))
                
        self.obstacles.draw(self.window)
        self.portals.draw(self.window)

        
        
class CityScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.CITY
        self.map = Map.gen_city_map()
        self.obstacles = Map.gen_obstacles()

        self.portals.add(Portal(self.width // 3 *2 , self.height // 3 * 2 ))


class WildScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.WILD
        self.map = Map.gen_wild_map()

class WinScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.WIN
        self.map = Map.gen_win_map()

class MainMenuScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.MAIN
        self.bg = pygame.image.load(GamePath.menu)
        self.bg = pygame.transform.scale(self.bg, 
                (WindowSettings.width, WindowSettings.height))
        
        self.font = pygame.font.Font(None, MenuSettings.textSize)
        self.font2 = pygame.font.Font("C:/Windows/Fonts/BRUSHSCI.TTF", MenuSettings.textSize * 3)
        self.text = self.font.render("Press ENTER to start",
                                True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2 , 
                                WindowSettings.height - 50))
        self.text2 = self.font2.render("Dungeon Breakers",
                                True, (255, 0, 0))
        self.text2Rect = self.text.get_rect(center=(WindowSettings.width // 2 -150, 
                                150))
        self.blinkTimer = 0
        
    def render(self):
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.text2, self.text2Rect)
        
        self.blinkTimer += 1
        if self.blinkTimer >= MenuSettings.blinkInterval:
            self.window.blit(self.text, self.textRect)
            if self.blinkTimer >= MenuSettings.blinkInterval * 2:
                self.blinkTimer = 0

class GameoverScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.OVER
        self.bg = pygame.image.load(GamePath.gameover)
        self.bg = pygame.transform.scale(self.bg, 
                (WindowSettings.width, WindowSettings.height))
        self.font = pygame.font.Font(None, MenuSettings.textSize)
        self.text = self.font.render("Press ENTER to restart",
                                True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 50))
        
    def render(self):
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.text, self.textRect)

class BadendingScene(GameoverScene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.BADENDING
        self.bg = pygame.image.load(GamePath.badending)
        self.bg = pygame.transform.scale(self.bg, 
                (WindowSettings.width, WindowSettings.height))

class GoodendingScene(GameoverScene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.GOODENDING
        self.bg = pygame.image.load(GamePath.goodending)
        self.bg = pygame.transform.scale(self.bg, 
                (WindowSettings.width, WindowSettings.height))