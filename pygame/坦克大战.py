import warnings
import pygame
import time
import random

warnings.filterwarnings("ignore")
_display = pygame.display
color_black = pygame.Color(0,0,0)
color_red = pygame.Color(255,0,0)
version = 'v1.07'
class MainGame():
    window = None
    screen_width=800
    screen_height=500
    #创建我方坦克
    TANK_PI = None
    #存储所有敌方坦克
    EnemyTank_list = []
    #创建敌方坦克的数量
    EnemyTank_count = 4
    def __init__(self):
        pass
    #开始游戏方法
    def startGame(self):
        _display.init()
        #创建窗口加载窗口（借鉴官方文档）
        MainGame.window = _display.set_mode([MainGame.screen_width,MainGame.screen_height])
        #创建我方坦克
        MainGame.TANK_PI = Tank(250,300)
        self.creatEnemyTank()
        #设置一下游戏标题
        _display.set_caption("坦克大战"+version)
        #让窗口持续刷新操作
        while True:
            #给窗口完成一个填充颜色
            MainGame.window.fill(color_black)
            #在循环中持续完成事件的获取
            self.getEvent()
            #将绘制文字得到的小画布，粘贴到窗口中
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆"%len(MainGame.EnemyTank_list)),(5,5))
            #将我方坦克加入到窗口中
            MainGame.TANK_PI.displayTank()  
            #循环展示敌方坦克
            self.blitEnemyTank() 
            #根据坦克开关调用坦克的移动方法
            if MainGame.TANK_PI and not MainGame.TANK_PI.stop:
                MainGame.TANK_PI.move()
            time.sleep(0.02)
            #窗口的刷新
            _display.update()
    #创建敌方坦克
    def creatEnemyTank(self):
        
        top = 100
        speed = random.randint(3,6)
        for i in range(MainGame.EnemyTank_count):
            #每次都随机生成一个left值
            left = random.randint(1,5)
            eTank = EnemyTank(left*100,top,speed)
            MainGame.EnemyTank_list.append(eTank)
    #将坦克加入到窗口中
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            eTank.displayTank()
            #敌方移动的方法
            eTank.randMove()

    #获取程序期间所有事件（鼠标事件，键盘事件）
    def getEvent(self):
        #1、获取所有事件
        eventList = pygame.event.get()
        #2、对事件进行判断处理（1点击关闭按钮 2按下键盘上某个按键）
        for event in eventList:
            #判断event.type 是否QUIT，如果是退出的话，直接调用程序结束方法
            if event.type == pygame.QUIT:
                self.endGame()
            #判断事件类型是否为按键按下，如果是，继续判断按键是哪一个，来进行对应处理
            if event.type == pygame.KEYDOWN:
                #具体是哪一个按键的处理
                if event.key == pygame.K_LEFT:
                    print("坦克向左调头，移动")
                    #修改坦克方向,完成移动操作
                    MainGame.TANK_PI.direction = 'L'
                    #MainGame.TANK_PI.move()
                    MainGame.TANK_PI.stop = False
                elif event.key == pygame.K_RIGHT:
                    print("坦克向右调头，移动")
                    MainGame.TANK_PI.direction = 'R'
                    #MainGame.TANK_PI.move()
                    MainGame.TANK_PI.stop = False
                elif event.key == pygame.K_UP:
                    print("坦克向上调头，移动")
                    MainGame.TANK_PI.direction = 'U'
                    #MainGame.TANK_PI.move()
                    MainGame.TANK_PI.stop = False
                elif event.key == pygame.K_DOWN:
                    print("坦克向下调头，移动")
                    MainGame.TANK_PI.direction = 'D'
                    #MainGame.TANK_PI.move()
                    MainGame.TANK_PI.stop = False
                elif event.key == pygame.K_SPACE:   #空格键是SPACE
                    print("发射子弹")
            if event.type == pygame.KEYUP:
                #松开的如果是方向键，才更改移动开关状态
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    #修改坦克的状态
                    MainGame.TANK_PI.stop = True
    #左上角文字检测的功能
    def getTextSurface(self,text):
        #初始化字体模块
        pygame.font.init()
        #选中一个合适的字体
        font = pygame.font.SysFont('kaiti',10)
        #使用对应的字符完成相关内容的绘制
        textSurface = font.render(text,True,color_red)
        return textSurface
    #结束游戏方法
    def endGame(self):
        print("谢谢使用！")
        #结束python解释器
        exit()
class Tank():
    def __init__(self,left,top):
        self.iamges = {
            'U':pygame.image.load('D:\\Python\\练习\\pygame\\imagetank\\tankup.png'),
            'D':pygame.image.load('D:\\Python\\练习\\pygame\\imagetank\\tankdown.png'),
            'L':pygame.image.load('D:\\Python\\练习\\pygame\\imagetank\\tankleft.png'),
            'R':pygame.image.load('D:\\Python\\练习\\pygame\\imagetank\\tankright.png'),
        }
        self.direction = 'U'
        self.iamge = self.iamges[self.direction]
        #坦克所在的区域
        self.rect = self.iamge.get_rect()
        #指定坦克初始化位置分别距x,y轴的位置
        self.rect.left = left
        self.rect.top = top
        #新增速度属性
        self.speed = 3
        #新增属性：坦克的移动开关
        self.stop = True
    #坦克的移动方法
    def move(self):
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < MainGame.screen_width:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.screen_height:
                self.rect.top += self.speed
    #射击方法
    def shot(self):
        pass
    #展示坦克（将坦克这个surface绘制到窗口中）
    def displayTank(self):
        #1 重新设置坦克的图片
        self.iamge = self.iamges[self.direction]
        #2 将坦克加入到窗口中
        MainGame.window.blit(self.iamge,self.rect)
class MyTank(Tank):
    def __init__(self):
        pass
class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        #图片集\图片、方向、位置、速度、是否活着
        self.iamges = {
            'U':pygame.image.load('D:\\Python\\练习\\pygame\\imagetank\\dftankU.jpg'),
            'D':pygame.image.load('D:\\Python\\练习\\pygame\\imagetank\\dftankD.jpg'),
            'L':pygame.image.load('D:\\Python\\练习\\pygame\\imagetank\\dftankL.jpg'),
            'R':pygame.image.load('D:\\Python\\练习\\pygame\\imagetank\\dftankR.jpg')
        }
        self.direction = self.randDirection()
        self.iamge = self.iamges[self.direction]
        #坦克所在的区域
        self.rect = self.iamge.get_rect()
        #指定坦克初始化位置分别距x,y轴的位置
        self.rect.left = left
        self.rect.top = top
        #新增速度属性
        self.speed = speed
        self.stop = True
        #新增步数属性，用来控制敌方坦克随机移动
        self.step = 50
    def randDirection(self):
        num = random.randint(1,4)
        if num ==1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'
    #随机移动
    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1 

    #def displayEnemtTank(self):
        #super().displayTank()
class Bullet():
    def __init__(self):
        pass
    #子弹的移动方法
    def move(self):
        pass
    #展示子弹的方法
    def displayBullet(self):
        pass
class Explode():
    def __init__(self):
        pass
    #展示爆炸效果
    def displayExplode(self):
        pass
class Wall():
    def __init__(self):
        pass
    #展示墙壁的方法
    def displayWall(self):
        pass
class Music():
    def __init__(self):
        pass
    #开始播放音乐
    def play(self):
        pass
MainGame().startGame()

