import pygame
from random import randint
import time

#khởi tạo game
pygame.init()

#khai báo màu
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (210, 210, 210)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

#tạo cửa sổ
WIDTH = 1000
HEIGHT = 500

cuaso = pygame.display.set_mode((WIDTH, HEIGHT)) #2 dấu ngoặc
pygame.display.set_caption('Background moving')

icon = pygame.image.load(r'D:\bt python 4\mk.png') #nếu không có r thì đổi thành dấu /
pygame.display.set_icon(icon)

fps = 90
clock = pygame.time.Clock()
global font


#tạo biến để lưu ảnh
bg = pygame.image.load(r'D:\bt python 4\images pygame\bg.png')
player_image = pygame.image.load(r'D:\bt python 4\images pygame\S5.png')



#-----------------------------------Class PLAYER----------------------------
class Player(pygame.sprite.Sprite):
    run_images = []
    jump_images = []
    slide_images = []

    #load ảnh và lưu vào các biến
    for i in range(1,8): #jump
        jump_images.append(pygame.image.load('images pygame/' + str(i) + '.png'))

    for i in range (2):
        jump_images.insert(3, pygame.image.load('images pygame/4.png'))

    for i in range(8,16): #run
        run_images.append(pygame.image.load('images pygame/' + str(i) + '.png'))

    for i in range(1,6): #slide
        slide_images.append(pygame.image.load('images pygame/' + 'S' + str(i) + '.png'))

    for i in range (2):
        slide_images.insert(1, pygame.image.load('images pygame/S2.png'))
    
  
    def __init__(self, x, y):
        super(Player,self).__init__()
        self.run_count = 0 #đếm số lần ảnh chạy
        self.jump_count = 0
        self.slide_count = 0
        self.surf = self.run_images[self.run_count] #cần lấy vị trí ảnh trong list
        self.rect = self.surf.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

        self.fall = False
        self.jump = False
        self.slide = False
        self.jump_down_speed = 0


    def activity(self, cs): #truyền thêm tham số cửa sổ phục vụ cho việc hiển thị text lúc ngã
        if self.fall:
            self.surf = pygame.image.load('images pygame/0.png')
            self.rect.y = (312 + 57) - self.surf.get_height()
            font = pygame.font.SysFont('arial', 40, 'bold')
            repeat_text = font.render('Press R to replay', True, RED, WHITE)
            cs.blit(repeat_text, (300,300))
            
            

        elif self.slide:
           
            self.surf = self.slide_images[self.slide_count//20]

            #chiều cao của ảnh
            cao = self.surf.get_height()  #57 đang là ảnh cao nhất
            self.rect.y = (312 + 57) - cao
            self.slide_count += 1
            
            if self.slide_count == len(self.slide_images) * 20:
                self.rect.y = 312
                self.slide_count = 0
                self.slide = False
        

        elif self.jump:
            self.surf = self.jump_images[self.jump_count//12]
            self.rect.y -= self.jump_down_speed 
            if self.jump_count <= 36:
                self.jump_down_speed = 3 - (self.jump_count//12)

            elif 36 < self.jump_count < 72:
                self.jump_down_speed = 0

            elif 72 <= self.jump_count < 108:
                self.jump_down_speed = -(len(self.jump_images) - (self.jump_count//12)) 

            self.jump_count +=1
        
            if self.jump_count == 108: #len(self.jump_images) * 12:
                self.jump_count = 0
                self.jump = False
                self.rect.y = 312
                
        else:
            self.surf = self.run_images[self.run_count//6]
            self.run_count += 1
            if self.run_count == len(self.run_images)*6:
                self.run_count = 0

 
'''elif self.jump:
            self.surf = self.jump_images[self.jump_count//12]
            self.rect.y - = self.jump_down_speed

            if self.jump_count <= (len(self.jump_images) - 6)*12: #jump_count <= 12 // load 1 ảnh 12 lần
                self.jump_down_speed = 3 - (self.jump_count//12)

            elif (len(self.jump_images) - 6) * 12 < self.jump_count < (len(self.jump_images) - 3)*12:
                self.jump_down_speed = 0
     
            elif self.jump_count < (len(self.jump_images) - 3) * 12 <= self.jump_count < len(self.jump_images) * 12:
                self.jump_down_speed = -(len(self.jump_images) - (self.jump_count//12))
            #print(self.jump_down_speed)
            print('độ dài của self.jump_count: ' + str(self.jump_count))

            self.jump_count += 1
'''
           
            

#=================Tạo chướng ngại vật======================
class Cua(pygame.sprite.Sprite):
    saw_images = []
    for i in range(0,4):
        saw_images.append(pygame.transform.scale(pygame.image.load('images pygame/SAW' + str(i) + '.png'), (64,64)))

    def __init__(self, y , dai, rong):
        super().__init__()
        self.x = 1000
        self.y = y
        self.dai = dai
        self.rong = rong
        self.saw_count = 0
        self.surf = pygame.Surface((dai, rong))
        self.rect = self.surf.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def show(self):
        self.surf = self.saw_images[self.saw_count]
        self.saw_count += 1

        if self.saw_count >= len(self.saw_images):
            self.saw_count = 0

        

class Cot(Cua):     #phương thức kế thừa hàm init
    cot = (pygame.image.load('images pygame/spike.png'))

    def show(self):
        self.surf = self.cot


#=========vật cản==========
list_vatcan = []
vatcan = pygame.sprite.Group()

def Vatcan():
    global list_vatcan, vatcan
    t = randint(0,1)

    if t == 0:
        vc = Cua(312,64,64)

    else:
        vc = Cot(0,48,320)

    vatcan.add(vc)
    
    list_vatcan.append(vc)
        
        
        

#=================Chương trình chính===================
pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
run = True
Vatcan()
player = Player(100, 312)
x_start = 0
x_stop = bg.get_width()

def load_sc():
    global x_start
    global x_stop
    cuaso.blit(bg, (x_start, 0))
    cuaso.blit(bg, (x_stop, 0))

    #khi ảnh chạy hết, gán lại giá trị ban đầu
    if x_stop == 0:
        x_start = 0
        x_stop = bg.get_width()

    x_start -= 2
    x_stop -= 2

def show_score():
    global score
    font = pygame.font.SysFont('arial', 30, 'bold')
    text_score = font.render('Score: ' + str(score), True, RED)
    cuaso.blit(text_score, (50, 20))

    

def show_highscore():
    global highscore
    global score
    font = pygame.font.SysFont('arial', 30, 'bold')
    text_highscore = font.render('Highscore: ' + str(highscore), False, RED)
    cuaso.blit(text_highscore, (50, 70))

#___________________Score______________
score = 0
highscore = 0

#xử lý highscore
f = open('highscore.txt', 'r', encoding = 'utf-8')
data = f.read()
f.close()
data1 = data.split('\n')

data2 = []
for i in data1:
    data2.append(i.split())         
del data2[-1]

data3 = []
for j in data2:
    data3.append(j[-1])

data4 = []
for k in data3:
    data4.append(int(k))
data4.sort()
                
if data4 == [] :
    highscore = 0
    
else:
    highscore = data4[-1]
    show_highscore()


print(data4)  

"""
def show_score():
    global score
    font = pygame.font.SysFont('arial', 30, 'bold')
    text_score = font.render('Score: ' + str(score), True, RED)
    cuaso.blit(text_score, (50, 20))

    

def show_highscore():
    global highscore
    global score
    font = pygame.font.SysFont('arial', 30, 'bold')
    text_highscore = font.render('Highscore: ' + str(highscore), False, RED)
    cuaso.blit(text_highscore, (50, 70))
"""
    
        
def breakstreak():
    text_highscore = font.render('Highscore: ' + str(score), False, RED)
    cuaso.blit(text_highscore, (50, 70))
    





#__________Hàm xử lý vật cản____________________
def Xuly_Vatcan():
    global list_vatcan, score, vatcan, player
    
    for i in vatcan:
        cuaso.blit(i.surf, i.rect)
        i.rect.x -= 2
        i.show()

        #khi chạy hết màn hình thì xóa đối tượng vật cản đi
        if i.rect.x < -64:
            i.kill()
            del list_vatcan[0]

        #xử lý tăng điểm
        if player.fall == False:
            if i.rect.x == 90:
                score += 1
            show_score()

    #kiểm tra vị trí của vật cản cuối để tạo ra vật cản mới
        if list_vatcan[-1].rect.x < 650:
            Vatcan()

def reset():
    global player, list_vatcan, vatcan, score, fps
    player = Player(100, 312)
    list_vatcan = []
    for i in vatcan:
        i.kill()

    Vatcan()
    score = 0
    fps = 90



#=======CHƯƠNG TRÌNH CHÍNH=============
while run:
    clock.tick(fps)
    #các sự kiện
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            run = False
 
        if event.type == pygame.USEREVENT + 1:
            fps += 10
            if fps >= 270:
                fps = 270
        
        if event.type == pygame.KEYDOWN:
            if player.jump or player.slide:
                pass
            
            elif event.key == pygame.K_UP:
                player.jump = True

            elif event.key == pygame.K_DOWN:
                player.slide = True

            if event.key == pygame.K_r:
                reset()

    if pygame.sprite.spritecollide(player, vatcan, False):
        font = pygame.font.SysFont('arial', 30, 'bold')
        player.fall = True
        if highscore <= score:
            text_highscore = font.render('Highscore: ' + str(score), False, RED)
            f = open('highscore.txt', "w")
            f.write(str(score))
            f.close()
        
            

    #cuaso.blit(bg, (0,0))
    load_sc()
    cuaso.blit(player.surf, player.rect)
    player.activity(cuaso)
    Xuly_Vatcan()
    show_score()
    show_highscore()

    '''cuaso.blit(saw.surf, saw.rect)
    saw.rect.x -= 2
    saw.show()

    cuaso.blit(cot.surf, cot.rect)
    cot.rect.x -= 2
    cot.show()'''
    



    pygame.display.update() #pygame.display.flip()
pygame.quit()







