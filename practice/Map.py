# -*- coding:utf-8 -*-
from Settings import *
import pygame
from random import random,randint

class Block(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


def gen_city_map():
    images = [pygame.image.load(tile) for tile in GamePath.cityTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tot = randint(0, 100)
            if tot < 1:
                imagenumber = randint(len(images) - 4, len(images) - 1)
            else:
                imagenumber = randint(0, len(images) - 5)
            tmp.append(images[imagenumber])
        mapObj.append(tmp)
    
    return mapObj

def gen_wild_map():
    images = [pygame.image.load(tile) for tile in GamePath.groundTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tot = randint(0, 100)
            if tot < 1:
                imagenumber = randint(len(images) - 4, len(images) - 1)
            else:
                imagenumber = randint(0, len(images) - 5)
            tmp.append(images[imagenumber])

        mapObj.append(tmp)
    
    return mapObj

def gen_win_map():
    images = [pygame.image.load(tile) for tile in GamePath.winmapTiles]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            tot = randint(0, 200)
            if tot < 1:
                imagenumber = randint(len(images) - 4, len(images) - 1)
            else:
                imagenumber = randint(0, len(images) - 5)
            tmp.append(images[imagenumber])

        mapObj.append(tmp)
    
    return mapObj

def gen_obstacles():
    images = [pygame.image.load(obstacles) for obstacles in GamePath.obstacles]

    obstacles = pygame.sprite.Group()
    # 左上没生成障碍，因为没做npc和障碍的碰撞
    midx = SceneSettings.tileXnum//2
    midy = SceneSettings.tileYnum//2
    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            # 防止在出生点生成obstacle
            if random() < SceneSettings.obstacleDensity and not(i < midx and j < midy) and (i not in range(midx-3, midx+3)) and (j not in range(midy-3, midy+3)):
                obstacles.add(Block(images[randint(0, len(images) - 1)], SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    return obstacles

