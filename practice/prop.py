# -*- coding:utf-8 -*-
from Settings import *
import random

class prop:
    def __init__(self):
        self.addCoins = 0
        self.addHP = 0
        self.addAttack = 0
        self.wave = 0
        self.list = []
        self.cs = copperstoneSettings()
        self.ss = silverstoneSettings()
        self.gs = goldenstoneSettings()
        self.cm = coppermedicineSettings()
        self.sm = silvermedicineSettings()
        self.gm = goldenmedicineSettings()
        self.cshoes = coppershoesSettings()
        self.sshoes = silvershoesSettings()
        self.ct = cartridgeSettings()
        self.msk = maskSettings()
        for _ in range(PropSettings.copper):
            self.list.append(self.cs)
            self.list.append(self.cm)
            
        for _ in range(PropSettings.silver):
            self.list.append(self.ss)
            self.list.append(self.sm)
            self.list.append(self.cshoes)
            self.list.append(self.ct)
        for _ in range(PropSettings.gold):
            self.list.append(self.gs)
            self.list.append(self.gm)
            self.list.append(self.msk)
            self.list.append(self.sshoes)

    def get_prop(self,wave):
        l = random.choice(self.list)
        addCoins = int(l.addCoins * pow(PropSettings.growthrate,wave))
        text = f"{l.text},价格{-addCoins}金币"
        return (addCoins,l.addHP,l.addAttack,l.addSpeed,l.addAttackspeed,text)

class copperstoneSettings:
    addCoins = - 20
    addHP = 0
    addAttack = 1
    addSpeed = 0
    addAttackspeed = 0
    text = f"粗糙的磨刀石，攻击力+1"

class silverstoneSettings:
    addCoins = - 50
    addHP = 0
    addAttack = 2
    addSpeed = 0
    addAttackspeed = 0
    text = f"普通的磨刀石，攻击力+2"

class goldenstoneSettings:
    addCoins = - 80
    addHP = 0
    addAttack = 3
    addSpeed = 0
    addAttackspeed = 0
    text = f"精良的磨刀石，攻击力+3"

class coppermedicineSettings:
    addCoins = - 5
    addHP = 5
    addAttack = 0
    addSpeed = 0
    addAttackspeed = 0
    text = f"廉价的生命药水，生命值+5"

class silvermedicineSettings:
    addCoins = - 10
    addHP = 10
    addAttack = 0
    addSpeed = 0
    addAttackspeed = 0
    text = f"普通的生命药水，生命值+10"

class goldenmedicineSettings:
    addCoins = - 25
    addHP = 25
    addAttack = 0
    addSpeed = 0
    addAttackspeed = 0
    text = f"优质的生命药水，生命值+25"

class coppershoesSettings:
    addCoins = -30
    addHP = 0
    addAttack = 0
    addSpeed = 1
    addAttackspeed = 0
    text = f"神速之靴，速度+1"

class silvershoesSettings:
    addCoins = -65
    addHP = 0
    addAttack = 0
    addSpeed = 2
    addAttackspeed = 0
    text = f"疾步之靴，速度+2"

class cartridgeSettings:
    addCoins = -100
    addHP = 0
    addAttack = 0
    addSpeed = 0
    addAttackspeed = -1
    text = f"快速弹夹，攻速+1"

class maskSettings:
    addCoins = -180
    addHP = 10
    addAttack = 2
    addSpeed = 1
    addAttackspeed = 0
    text = f"小丑面具，生命值+30,速度+1,攻击+2"