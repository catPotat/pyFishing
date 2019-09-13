# -*- coding: utf-8 -*-
'''
This script is written by Long Nguyen
It is also my first game ever so no critism please :P
'''
import pygame
import pygame.gfxdraw
import random
from time import sleep
import threading
from sys import exit
from GIF import GIFImage

# Kích cỡ 
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
LAND = 200

# Màu 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
OceanBLUE = (0, 119, 190)
GREY150 = (150, 150, 150)
abcdefBlue = (171, 205, 239)
TranOCEAN = (0, 119, 190, 175)

GLOBAL_LIST = [0] # we have score, volume, boss mode stored here

def intro():
    print "*****************************************"
    print "*WELCOME TO PYFISHING 1.1 by LONG NGUYEN*"
    print "*****************************************"
    done = False
    while not done:
        print "Choose an option:"
        print "[P]: Play game [M]: Play muted [X]: Exit"
        do = raw_input().lower()
        if do == "p":
            GLOBAL_LIST.append(False)
            done = True
        if do == "m":
            GLOBAL_LIST.append(True)
            done = True
        if do == "x":
            exit("kemcoi")

class Underwater:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.tuyp = True
                        
def make_fish():
    fish = Underwater()
    fish.x = random.choice([-50, SCREEN_WIDTH+200])
    fish.y = random.randrange(LAND+60, SCREEN_HEIGHT-50)
    fish.tuyp = True
    if random.randrange(0, 10) == 1:
        fish.tuyp = not fish.tuyp
    fish.change_y = random.randrange(-3, 3) # hướng bơi 
    if fish.x < 0:
        if fish.tuyp == True:
            fish.change_x = random.randrange(1, 5) # tốc độ
        else:
            fish.change_x = 10
    else:
        if fish.tuyp == True:
            fish.change_x = random.randrange(-5, -1)
        else:
            fish.change_x = -10
    return fish
    
def make_bubble():
    bubble = Underwater()
    bubble.x = random.randrange(0, SCREEN_WIDTH)
    bubble.y = SCREEN_HEIGHT-5
    bubble.change_y = random.randrange(-5, -1) # tốc độ
    return bubble
        
def make_obstacle():
    obstacle = Underwater()
    obstacle.tuyp = random.choice([True, False])
    #print "ob.type", obstacle.tuyp
    obstacle.x = random.choice([-200, SCREEN_WIDTH+200])
    obstacle.y = random.randrange(LAND+100, SCREEN_HEIGHT-50)
    obstacle.change_y = random.randrange(-2, 2) # hướng bơi 
    if obstacle.x < 0:
        obstacle.change_x = random.randrange(1, 4) # tốc độ
    else:
        obstacle.change_x = random.randrange(-4, -1)
    return obstacle
    
def make_crab():
    crab = Underwater()
    crab.tuyp = random.choice([True, False])
    crab.y = LAND
    if crab.tuyp == True:
        crab.x = -50
        crab.change_x = random.randrange(1, 5) # tốc độ
    else:
        crab.x = SCREEN_WIDTH+50
        crab.change_x = random.randrange(-5, -1)
    return crab

def fish_flee(obstacleY, hook):
    flee = Underwater()
    flee.y = obstacleY +50
    flee.x = SCREEN_WIDTH/2
    flee.change_x = random.choice([-15, 15])
    if hook == 1:
        flee.tuyp = True
    else:
        flee.tuyp = False
    return flee

def make_boss(phase, kieu):
    boss = Underwater()
    if kieu == False:
        number = 1
    else:
        number = 2
    if phase == 1:
        boss.y = SCREEN_HEIGHT*number/3
        if number == 1:
            boss.x = SCREEN_WIDTH
            boss.change_x = -3
        else:
            boss.x = -320
            boss.change_x = 3
    elif phase == 2:
        boss.x = -400
        boss.y = (SCREEN_HEIGHT-LAND)/2 +LAND
        boss.change_x = 2
    elif phase == 3:
        boss.x = SCREEN_WIDTH
        boss.y = (SCREEN_HEIGHT-LAND)/2 +LAND
        boss.change_x = -1
    elif phase == 4:
        boss.x = SCREEN_WIDTH/2
        boss.y = (SCREEN_HEIGHT-LAND)/2 +LAND
        if kieu == False:
            boss.change_x = 18
        else:
            boss.change_x = -18
    return boss
            
#--------HERE LIES THE MAIN FUNCTION--------
def main():
    intro()
    
    def background_fx():
        t = threading.currentThread()
        bubbles = pygame.mixer.Sound('assets/bubbles.wav')
        waves = pygame.mixer.Sound('assets/wave.wav')
        bubbles.play()
        while getattr(t, "do_run", True):
            sleep(random.randrange(10, 20))
            if random.choice([True, False]):
                bubbles.play()
            else:
                waves.play()
        
    def spawn_bubble():
        t = threading.currentThread()
        while getattr(t, "do_run", True):
			bubble = make_bubble()
			bubble_list.append(bubble)
			sleep(random.randrange(0, 2))
			sleep(0.01)
			
    def spawn_fish():
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            fish = make_fish()
            fish_list.append(fish)
            #print "fish", fish
            sleep(random.randrange(10, 40)/10)

    def spawn_obstacle():
        t = threading.currentThread()
        while True:
            sleep(5)
            while getattr(t, "do_run", True):
                #print "doing obs"
                score = GLOBAL_LIST[0]
                if score < 8:
                    choose = -1
                    sleep(3)
                elif score < 25:
                    choose = 1
                else:
                    choose = random.randrange(0, 3)
	                
                if choose > 0:
                    obstacle = make_obstacle()
                    obstacle_list.append(obstacle)
                    #print "obstacle", obstacle
                elif choose == 0:
                    crab = make_crab()
                    crab_list.append(crab)
                    #print "crab_", crab
                if score > 54:
                    score=54
                sleep(random.uniform(1, 10-score/6))

    def boss_fight():
        b = threading.currentThread()
        while True:
            sleep(7)
            while getattr(b, "bossmode", False):
                #~ print "made boss"
                gold = GLOBAL_LIST[3]
                sleep(1)
                boss = make_boss(1, False)
                boss_list.append(boss)
                if gold:
                    boss = make_boss(1, True)
                    boss_list.append(boss)
                sleep(10)
                boss = make_boss(2, 0)
                boss_list.append(boss)
                sleep(10)
                if gold:
                    sleep(7)
                    boss = make_boss(3, 0)
                    boss_list.append(boss)
                    sleep(15)
                GLOBAL_LIST[2] = False
                sleep(5)
    	        #print "stop boss"

    pygame.init()
    
    # Cài màn hình 
    pygame.display.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("PyCâuCá v1.1")

    #----ẢNH---- 
    r_fish = GIFImage("assets/fish.gif")
    r_fish.boomerang()
    l_fish = GIFImage("assets/fish.gif")
    l_fish.boomerang()
    l_fish.transform(True)
    
    r_rarefish = GIFImage("assets/rarefish.gif")
    r_rarefish.boomerang()
    l_rarefish = GIFImage("assets/rarefish.gif")
    l_rarefish.boomerang()
    l_rarefish.transform(True)
    
    vert_fish = GIFImage("assets/fish_hooked.gif")
    vert_fish.boomerang()
    vert_rarefish = GIFImage("assets/rarefish_dramatic.gif")
    
    bait = pygame.image.load("assets/worm.png").convert()
    bait.set_colorkey(BLACK)
    nobait = pygame.image.load("assets/noworm.png").convert()
    nobait.set_colorkey(BLACK)
    pole = pygame.image.load("assets/fishing_pole.png").convert()
    pole.set_colorkey(BLACK)
    pikachu = pygame.image.load("assets/Pikachu.png").convert()
    pikachu.set_colorkey(BLACK)
    worms = pygame.image.load("assets/CanOfWorms.png").convert()
    worms.set_colorkey(BLACK)
    
    weed = GIFImage("assets/seaweed.gif")
    
    bicycle = GIFImage("assets/bicycle.gif")
    bicycle.boomerang()
    shoe = GIFImage("assets/shoe.gif")
    shoe.boomerang()
    
    lcrab = pygame.image.load("assets/crab.png").convert()
    lcrab.set_colorkey(BLACK)
    rcrab = pygame.transform.flip(lcrab, True, False)
    
    hung = pygame.image.load("assets/hung.jpg").convert()
    hung_over = pygame.transform.rotate(hung, 90)
    
    magikarp = pygame.image.load("assets/Magikarp.png").convert()
    magikarp.set_colorkey(BLACK)
    vert_magikarp = pygame.transform.rotate(magikarp, 90)
    far_magikarp = pygame.transform.scale(pygame.transform.flip(magikarp, True, False), (185, 200))
    
    shinymagikarp = pygame.image.load("assets/ShinyMagikarp.png").convert()
    shinymagikarp.set_colorkey(BLACK)
    vert_shinymagikarp = pygame.transform.rotate(shinymagikarp, 90*3)
    far_shinymagikarp = pygame.transform.scale(pygame.transform.flip(shinymagikarp, True, False), (300, 320))
    
    reeled_background = pygame.image.load("assets/reeled_background.jpg").convert()
    reeled_big = pygame.image.load("assets/reeled_big.png").convert()
    reeled_big.set_colorkey(BLACK)
    reeled_gold = pygame.image.load("assets/reeled_gold.png").convert()
    reeled_gold.set_colorkey(BLACK)
    
    strandedred = pygame.image.load("assets/stranded_magikarp.png").convert()
    #~ strandedred.set_colorkey(BLACK)
    strandedgold = pygame.image.load("assets/stranded_shiny_magikarp.png").convert()
    strandedgold.set_colorkey(BLACK)
    
    scoref = pygame.font.Font("assets/Georgia.ttf", 100)

    #----ÂM THANH----
    if GLOBAL_LIST[1] == False:
        pygame.mixer.music.load('assets/DrSchroeder-GoodPeople.128.mp3') # nhạc nền
        pygame.mixer.music.play(-1)
        hooked_fx = pygame.mixer.Sound('assets/hooked.wav')
        flee_fx = pygame.mixer.Sound('assets/splash.wav')
        scored_fx = pygame.mixer.Sound('assets/pop.wav')
        cut_fx = pygame.mixer.Sound('assets/click.wav')
        chomp_fx = pygame.mixer.Sound('assets/chomp.wav')
        bigsplash = pygame.mixer.Sound('assets/bigsplash.wav')
    else:
        hooked_fx = pygame.mixer.Sound('')
        flee_fx = pygame.mixer.Sound('')
        scored_fx = pygame.mixer.Sound('')
        cut_fx = pygame.mixer.Sound('')
        chomp_fx = pygame.mixer.Sound('')
        bigsplash = pygame.mixer.Sound('')
        
    # các thứ
    clock = pygame.time.Clock()
    snow_white = False
    hookStatus = 0
    life = 3
    score = 1
    scoreleap = 0
    GLOBAL_LIST.append(False) #[2] bossmode
    GLOBAL_LIST.append(False) #[3] bossmodemode
    bosscounter = 0
    redbossreeled = False
    goldbossreeled = False
    howmanyweed = 15
    weed_spawn_y = []
    for i in xrange(howmanyweed):
        weed_spawn_y.append(random.randrange(0, SCREEN_WIDTH, 30))
    hole = (SCREEN_WIDTH/2 -100, LAND/2 +30)
    
    fish_list = []
    bubble_list = []
    obstacle_list = []
    crab_list = []
    boss_list = []

    obsthread = threading.Thread(target=spawn_obstacle)
    obsthread.start()
    obsthread.do_run = True
    bossthread = threading.Thread(target=boss_fight)
    bossthread.start()
    bossthread.bossmode = False
    
    nonstop = threading.Thread(target=spawn_fish)
    nonstop.start()
    nonstop = threading.Thread(target=spawn_bubble)
    nonstop.start()
    nonstop = threading.Thread(target=background_fx)
    if GLOBAL_LIST[1] == False:
	    nonstop.start()

    done = False
    
    #--------MAIN LOOP--------
    while not done:
        #--------Event Processing--------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = pygame.mouse.get_pos()
                if mouseY < LAND:
                    if mouseY < 25:
                        mouseY = 25
                    if hookStatus == 5:
                        mouseY = LAND+1
                    elif hookStatus == 6:
                        mouseY = LAND+1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                downX, downY = pygame.mouse.get_pos()
                if downY < LAND/2:
                    if 0 < hookStatus < 3 or 4<hookStatus<7:
                        if hookStatus == 1:
                            scoreleap = 1
                        elif hookStatus == 2:
                            scoreleap = 10
                        elif hookStatus == 5:
                            redbossreeled = True
                            hookStatus = 7
                            scoreleap = -25
                        elif hookStatus == 6:
                            goldbossreeled = True
                            hookStatus = 8
                            scoreleap = -55
                        if hookStatus <6:
                            scored_fx.play()
                            hookStatus = 0
                elif life > 0:
                    if 5 > hookStatus > 2 and SCREEN_WIDTH*3/4 < downX < SCREEN_WIDTH-30 and LAND/3 < downY < LAND:
	                    scored_fx.play()
	                    hookStatus = 0
	                    life -=1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    easteregg = 1
                elif event.key == pygame.K_e and easteregg == 1:
                    easteregg = 2
                elif event.key == pygame.K_m and easteregg == 2:
                    easteregg = 3
                elif event.key == pygame.K_c and easteregg == 3:
                    easteregg = 4
                elif event.key == pygame.K_o and easteregg == 4:
                    easteregg = 5
                elif event.key == pygame.K_i and easteregg == 5:
                    snow_white = not snow_white
                else:
                    easteregg = 0
                                        
        #--------LOGIC--------
        GLOBAL_LIST[0] = score
        
        if scoreleap > 0:
            score += 1
            scoreleap -= 1
        elif scoreleap < 0:
            score += 1
            scoreleap += 1
        
        # Kiểm tra có boss chưa
        if score%50 == 0:
            if score<>0 and score/50 == bosscounter and scoreleap>=0:
                #print "start boss"
                bossthread.bossmode = True
                obsthread.do_run = False
                GLOBAL_LIST[2] = True
                if bosscounter%2 ==0:
                    GLOBAL_LIST[3] = True #bossmodemode
                else:
                    GLOBAL_LIST[3] = False
                bosscounter +=1
        if obsthread.do_run == False:
            if GLOBAL_LIST[2] == False:
	            #print "stoped boss"
	            bossthread.bossmode = False
	            obsthread.do_run = True
                
        # Cá bơi
        for fish in fish_list:
            fish.x += fish.change_x
            fish.y += fish.change_y
            if fish.y < LAND+40 or fish.y > SCREEN_HEIGHT-10:
                fish.change_y *= -1
            if fish.x > SCREEN_WIDTH+200 or fish.x < -250: 
                fish_list.remove(fish)
            if abs(fish.x - SCREEN_WIDTH/2) < 35 and abs(fish.y - mouseY) < 40:
                if hookStatus == 0:
                    hooked_fx.play()
                    fish_list.remove(fish)
                    if fish.tuyp == True:
                        hookStatus = 1
                    else:
                        hookStatus = 2
        
        # Bong bóng 
        for bubble in bubble_list:
            bubble.y += bubble.change_y
            if bubble.y < LAND:
                bubble_list.remove(bubble)

        # Chướng ngại vật
        for obstacle in obstacle_list:
            obstacle.x += obstacle.change_x
            obstacle.y += obstacle.change_y
            if obstacle.tuyp == True:
                obtop = LAND+220/2
                obbottom = SCREEN_HEIGHT-50
                obwide = 250/2
                obhigh = 200/2
            else:
                obtop = LAND+75/2
                obbottom = SCREEN_HEIGHT-10
                obwide = 110/2
                obhigh = 75/2
            if obstacle.y < obtop or obstacle.y > obbottom:
                obstacle.change_y *= -1
            if obstacle.x > SCREEN_WIDTH+500 or obstacle.x < -500:
                obstacle_list.remove(obstacle)
            if abs(obstacle.x - SCREEN_WIDTH/2) < obwide and abs(obstacle.y - mouseY) < obhigh:
                if 0 < hookStatus < 3:
                    flee_fx.play()
                    flee = fish_flee(mouseY, hookStatus)
                    fish_list.append(flee)
                    hookStatus = 3
                    #print "fleeee", flee
            if hookStatus ==5:
                if abs(obstacle.x - SCREEN_WIDTH/2) < obwide+100 and abs(obstacle.y - mouseY) < obhigh+180:
                    flee_fx.play()
                    flee = make_boss(4, False)
                    boss_list.append(flee)
                    hookStatus = 3
            if hookStatus ==6:
                if abs(obstacle.x - SCREEN_WIDTH/2) < obwide+180 and abs(obstacle.y - (mouseY+275)) < obhigh+250:
                    flee_fx.play()
                    flee = make_boss(4, True)
                    boss_list.append(flee)
                    hookStatus = 3
                    
        for crab in crab_list:
            crab.x += crab.change_x
            if abs(crab.x - SCREEN_WIDTH/2) < 5:
                if mouseY > LAND:
                    cut_fx.play()
                    if 0 < hookStatus < 3:
                        flee = fish_flee(mouseY, hookStatus)
                        fish_list.append(flee)
                    if hookStatus ==5:
                        flee = flee = make_boss(4, False)
                        boss_list.append(flee)
                    if hookStatus ==6:
                        flee = flee = make_boss(4, True)
                        boss_list.append(flee)
                    hookStatus = 4
            if crab.tuyp == True:
                if crab.x < -50:
                    crab_list.remove(crab)
                elif crab.x > SCREEN_WIDTH/2:
                    crab.change_x *= -1
            else:
                if crab.x > SCREEN_WIDTH + 50:
                    crab_list.remove(crab)
                elif crab.x < SCREEN_WIDTH/2:
                    crab.change_x *= -1

        for boss in boss_list:
            boss.x += boss.change_x
            if boss.x > SCREEN_WIDTH+600 or boss.x < -800: 
                boss_list.remove(boss)
            if abs(boss.x - SCREEN_WIDTH/2) < 25 and abs(boss.y - (mouseY+100)) < 100 and boss.y == (SCREEN_HEIGHT-LAND)/2 +LAND:
                if 0<hookStatus<3 and boss.change_x > 0:
                    chomp_fx.play()
                    boss_list.remove(boss)
                    hookStatus = 5
                elif hookStatus == 5 and snow_white == True:
                    chomp_fx.play()
                    hookStatus = 6
                    boss_list.remove(boss)
            
        #--------LÀM MÀU--------
        screen.fill(OceanBLUE)
        
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, LAND))
        pygame.draw.ellipse(screen, GREY150, (hole[0], hole[1]+1, 200, 20+10)) # vẽ lỗ 
        pygame.draw.ellipse(screen, OceanBLUE, (hole[0], hole[1]+10, 200, 20))
        
        score_display = scoref.render(str(score), True, BLACK) # vẽ score 
        screen.blit(score_display, [300, -18])
        
        pygame.draw.rect(screen, GREY150, (0, hole[1]+50, SCREEN_WIDTH, 20))
        screen.blit(pikachu, [SCREEN_WIDTH/2 +170, -10])
        screen.blit(pole, [SCREEN_WIDTH/2, 10])
        
        if redbossreeled:
            screen.blit(strandedred, [-50, 25])
        if goldbossreeled:
            screen.blit(strandedgold, [55, -45])
        
        for bubble in bubble_list:
            pygame.draw.circle(screen, abcdefBlue, [bubble.x, bubble.y], 10)
        
        where_worm_x = 830
        for i in xrange(life):
            screen.blit(worms, [where_worm_x + i*50, 70])
            
        for boss in boss_list: #vẽ boss 
            #pygame.draw.circle(screen, BLACK, [boss.x, boss.y], 50)
            if boss.y <> (SCREEN_HEIGHT-LAND)/2 +LAND:
                if boss.y == SCREEN_HEIGHT*1/3:
                    screen.blit(far_magikarp, [boss.x, boss.y])
                else:
                    screen.blit(far_shinymagikarp, [boss.x, boss.y])
                #~ pygame.draw.rect(screen, TranOCEAN, (boss.x, boss.y, 320, 320))
                pygame.gfxdraw.box(screen, (boss.x, boss.y, 320, 320), TranOCEAN)
            else:
                if boss.change_x > 0:
                    screen.blit(magikarp, [boss.x-320, boss.y-180])
                else:
                    screen.blit(shinymagikarp, [boss.x+20, boss.y-275])
        
        if hookStatus == 0: #vẽ mồi
            screen.blit(bait, [SCREEN_WIDTH/2-25, mouseY])
        if hookStatus == 1:
            vert_fish.render(screen, (SCREEN_WIDTH/2-135/2, mouseY-2))
        elif hookStatus == 2:
            vert_rarefish.render(screen, (SCREEN_WIDTH/2-115/2, mouseY-50))
        elif hookStatus == 3:
            screen.blit(nobait, [SCREEN_WIDTH/2-25, mouseY])
        elif hookStatus == 5:
            screen.blit(vert_magikarp, [SCREEN_WIDTH/2-180, mouseY-10])
        elif hookStatus == 6:
            screen.blit(vert_shinymagikarp, [SCREEN_WIDTH/2-275, mouseY-15])
        
        # vẽ cảnh câu đc boss 
        elif hookStatus >6:
            bigsplash.play()
            reeled = True
            backgroundY = -25
            foregroundY = 50
            while reeled:
                screen.blit(reeled_background, [-320, backgroundY])
                if hookStatus == 7:
                    screen.blit(reeled_big, [-25, foregroundY])
                else:
                    screen.blit(reeled_gold, [-125, foregroundY-55])
                backgroundY -=1
                foregroundY -=2
                clock.tick(20) # Framerate
                pygame.display.flip()
                if foregroundY < -100:
                    reeled = False
                    hookStatus = 0
        
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH/2, 10), (SCREEN_WIDTH/2, mouseY), 2) # vẽ dây
                
        for fish in fish_list: # vẽ cá
            #pygame.draw.circle(screen, WHITE, [fish.x, fish.y], 20)
            if fish.change_x < 0:
                if fish.tuyp == True:
                    r_fish.render(screen, (fish.x, fish.y-130/2))
                else:
                    r_rarefish.render(screen, (fish.x, fish.y-130/2))
            else:
                if fish.tuyp == True:
                    l_fish.render(screen, (fish.x-220, fish.y-130/2))
                else:
                    l_rarefish.render(screen, (fish.x-220, fish.y-130/2))

        for obstacle in obstacle_list:
            #pygame.draw.circle(screen, BLACK, [obstacle.x, obstacle.y], 30)
            if obstacle.tuyp == True:
                bicycle.render(screen, (obstacle.x-280/2, obstacle.y-240/2))
            else:
                shoe.render(screen, (obstacle.x-140/2, obstacle.y-84/2))
                        
        for crab in crab_list:
            #pygame.draw.circle(screen, BLACK, [crab.x, crab.y], 20)
            if crab.tuyp == True:
                screen.blit(lcrab, [crab.x-150, crab.y])
            else:
                screen.blit(rcrab, [crab.x-20, crab.y])
                        
        if snow_white == True:
            for boss in boss_list:
                if boss.y == (SCREEN_HEIGHT-LAND)/2 +LAND:
                    if boss.change_x > 0:
                        screen.blit(hung, [boss.x-75, boss.y-35])
            for fish in fish_list:
                if fish.change_x < 0:
                    screen.blit(hung, [fish.x, fish.y-50])
                else:
                    screen.blit(hung, [fish.x-100, fish.y-50])
            if 0<hookStatus<3 or hookStatus==5:
                screen.blit(hung_over, [SCREEN_WIDTH/2-50, mouseY+25])
                
        for i in xrange(howmanyweed):
            #screen.blit(weed, [weed_spawn_y[i], SCREEN_HEIGHT-174])
            weed.render(screen, (weed_spawn_y[i], SCREEN_HEIGHT-130))
                                
        pygame.draw.rect(screen, WHITE, (hole[0], hole[1]+29, 200, 21))
        pygame.draw.rect(screen, GREY150, (0, hole[1]+50, SCREEN_WIDTH, 20))

        if life == 0 and hookStatus > 2:
            game = pygame.font.Font(None, 300)
            over = game.render("GAME OVER", True, BLACK)
            screen.blit(over, [SCREEN_HEIGHT/3, SCREEN_WIDTH/4])
            
        #--------Wrap-up--------
        clock.tick(60) # Framerate
        pygame.display.flip()
    
    ##--------EXIT--------
    #nonstop.do_run = False
    #nonstop.join()
        
if __name__ == "__main__":
    main()
    exit("Goodbye")
