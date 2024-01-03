# -*- coding:utf-8 -*-

import pygame
import sys
import time

from SceneManager import SceneManager
from Settings import *
from Player import Player

def run_game():
    pygame.init()

    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    pygame.display.set_caption(WindowSettings.name)

    scene = SceneManager(window)

    # 创建角色 和 NPC 精灵
    player = Player(WindowSettings.width // 2, WindowSettings.height // 2)
    clock = pygame.time.Clock()
    
    tot=5 #控制攻速的一个变量
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_r]:
            scene.begin_game()

        if scene.game_active():
            player.update(keys, scene)   # 主要是角色移动

            scene.update(player)
             # 主要是场景中对象的动画更新，暂时不涉及player的部分

            tot+=1
            if keys[pygame.K_SPACE]:     #按空格键开火            
                           
                if tot> player.get_playerAttackspeed(): #5是攻速
                    scene.fire(player.get_posx(),player.get_posy())
                    tot=0   

            # talking 的render 必须要在scene render以后，不然会被背景盖掉
                    
            scene.render(player) 
            scene.timing()               
            player.draw(window)

            #scene.check_event_talking(player, keys)
            #scene.check_event_battle(player, keys)
            pygame.display.flip()

if __name__ == "__main__":
    run_game()
