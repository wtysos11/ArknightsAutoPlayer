import pyautogui
from PIL import Image
import time
import pyscreeze

class arknightsAutoPlayer:
    def auxiliaryFight(self):
        '''
        使用辅助战斗模块完成
        实现思路：
            点击开始按钮
            重复循环等待结束
            结束时点击重新进入开始

        可能出现的情况：
            1.失误：没办法，总不能我自己下场吧
            2.升级：需要多点一下
            3.延迟卡顿，可能还是要多点几下
        '''
        pyautogui.PAUSE = 2
        while not self.checkBattleAvailable():
            time.sleep(1)
        pyautogui.click(1620,932)
        while not self.CheckGameReady():
            time.sleep(1)
        pyautogui.click(1570,713)
        while not self.checkBattleEnd():
            time.sleep(1)
            if self.CheckLevelUp():
                pyautogui.click(1548,460)
        pyautogui.click(1548,460)
        pyautogui.click(1548,460)
        pyautogui.click(1548,460)

    def findInImage(self,aimImage,originImage,confidence = 0.9):
        ''' 
        在aimImage中查找originImage（两者都是Image对象）
        置信度confidence表示允许的误差像素的占比
        如果找到了，则返回首个像素；不然，返回None
        不支持缩放查找        
        实现思路：
        首先进行逐像素比对，计算允许的误差像素个数，并对当前搜索环境中的误差像素个数进行累计，如果累计超过，则不可能匹配，直接跳出
        '''
        try:
            location = pyautogui.locate(aimImage,originImage,confidence = confidence)
        except:
            return None
        return location
        '''
        alInterval = 5
        allowCount = int(originImage.size[0] * originImage.size[1] *confidence)
        for y in range(aimImage.size[1]):
            for x in range(aimImage.size[0]):
                wrongCount = 0
                if x+originImage.width>aimImage.width or y+originImage.height>aimImage.height:
                    break

                for xx in range(originImage.size[0]):
                    for yy in range(originImage.size[1]):
                        oc = originImage.getpixel((xx,yy))
                        ac = aimImage.getpixel((x+xx,y+yy))
                        if x+xx >= aimImage.size[0] or y+yy >= aimImage.size[1]:
                            break
                        if abs(oc[0]-ac[0])>alInterval or abs(oc[1]-ac[1])>alInterval or abs(oc[2]-ac[2])>alInterval:
                            wrongCount += 1
                    if wrongCount >=allowCount:
                        break
                
                if wrongCount < allowCount:
                    return (x,y)
        
        return None
        '''


    def checkBattleAvailable(self):
        '''
        检查开始战斗是否可用
        '''
        originXL = 1584
        originYU = 899
        originXR = 1774
        originYD = 972
        compareImage = Image.open('gameStart.png')
        shootImage = pyautogui.screenshot(region = (originXL,originYU,originXR-originXL,originYD-originYU))
        try:
            location = pyautogui.locate(compareImage,shootImage,confidence = 0.9)
        except pyscreeze.ImageNotFoundException:
            return False
        return True


    def checkBattleEnd(self):
        '''
        检查开始战斗是否结束
        '''
        originXL = 1269
        originYU = 678
        originXR = 1470
        originYD = 730
        compareImage = Image.open('gameOver.png')
        shootImage = pyautogui.screenshot(region = (originXL,originYU,originXR-originXL,originYD-originYU))
        try:
            location = pyautogui.locate(compareImage,shootImage,confidence = 0.9)
        except pyscreeze.ImageNotFoundException:
            return False
        return True

    def CheckLevelUp(self):
        '''
        检查是否升级
        '''
        originXL = 940
        originYU = 455
        originXR = 1198
        originYD = 564
        compareImage = Image.open('LevelUp.png')
        shootImage = pyautogui.screenshot(region = (originXL,originYU,originXR-originXL,originYD-originYU))
        try:
            location = pyautogui.locate(compareImage,shootImage,confidence = 0.9)
        except pyscreeze.ImageNotFoundException:
            return False
        return True


    def CheckGameReady(self):
        '''
        检查是否进入到开始行动界面
        '''
        originXL = 1457
        originYU = 520
        originXR = 1712
        originYD = 948
        compareImage = Image.open('gameReady.png')
        shootImage = pyautogui.screenshot(region = (originXL,originYU,originXR-originXL,originYD-originYU))
        try:
            location = pyautogui.locate(compareImage,shootImage,confidence = 0.9)
        except pyscreeze.ImageNotFoundException:
            return False
        return True
