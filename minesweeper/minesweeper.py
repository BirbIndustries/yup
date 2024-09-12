#todo
#square clearing (clears a square until it reaches one with a bomb in its 3*3 area. it labels that tile with its number):
#   - make the bomb counter run itself on squares with no bombs, and no clearsquare square on
#UI and sound effects:
#   - maybe a slider to pick bombs? click to tp the slider to mouse x position, a text on screen that tells you what it is (finds how may pixels across it is then rounds down to a multiple of 252 * how many pixels per incrment )

import pygame
import pgzrun
import random
import threading
from pgzero.actor import Actor

WIDTH = 540
HEIGHT = 473
numsqrs = [Actor("cleared square"),Actor("1"),Actor("2"),Actor("3"),Actor("4"),Actor("5"),Actor("6"),Actor("7"),Actor("8")]
bg = Actor("map")
flag = Actor("flag")
bombcurser = Actor("bomb")
flagcurser = Actor("flag")
deadface = Actor("deadface")
deadface.x = 269
deadface.y = 447
stoobid = Actor("stoobid")
stoobid.x = 270
stoobid.y = 235
bombs = []
flags = []
clearedsquares = []
screensquares = []
queue = []
curser = 0
# bombcount = 10
# while not(bombcount < 253 and bombcount > 0):
#   bombcount = int(input("How many Bombs per game? \n (Between 1 and 252): "))
bombcount = 30
flaglimit = bombcount
dead = False
seconds = 0

def timer():
    global run1
    global seconds
    run1 = threading.Timer(1,timer)
    run1.start()
    seconds = seconds + 1


def bombchecker(xoffset,yoffset):
    bombcounter = 0
    for i in bombs:
        if i.x == xoffset and i.y == yoffset:
            bombcounter += 1
    if bombcounter > 0:
        return 1
    else:
        return 0

def sqrchecker(x,y):
    global clearedsquares
    global screensquares
    bombcount = 0
    bombcount += bombchecker(x+0,y-1)
    bombcount += bombchecker(x+0,y+1)
    bombcount += bombchecker(x+1,y+1)
    bombcount += bombchecker(x+1,y-1)
    bombcount += bombchecker(x+1,y+0)
    bombcount += bombchecker(x-1,y+1)
    bombcount += bombchecker(x-1,y+0)
    bombcount += bombchecker(x-1,y-1)
    newclearsqr = Actor(numsqrs[bombcount].image)
    newclearsqr.x = x
    newclearsqr.y = y
    clearedsquares.append(newclearsqr)
    screensqr = newclearsqr
    screensqr.x = (x*30)+15
    screensqr.y = (y*30)+15
    screensquares.append(screensqr)
    for n in range(-2,2):
        for m in range(-2,2):
            if (x + n) >= 0 and (x + n)< 18 and (y + m) >= 0 and (y + m) < 14:
                if n != 0 and m != 0:
                    if not any(a.x == x+n and a.y == y+m for a in bombs):
                        if not any(b.x == x+n and b.y == y+m for b in flags):
                            if not any(c.x == x+n and c.y == y+m for c in clearedsquares):
                                if not any(d[0] == x+n and d[1] == y+m for d in queue):
                                    try:
                                        if not clearedsquares[x+n][y+m]:
                                            newsqr = [x+n,y+m]
                                            queue.append(newsqr)
                                    except IndexError:
                                        pass


def genbombs():
    for i in range(bombcount):
        newbomb = Actor("bomb")
        newbomb.x = random.randint(0,17)
        newbomb.y = random.randint(0,13)
        reroll = True
        while reroll == True:
            if not any(bomb.x == newbomb.x and bomb.y == newbomb.y for bomb in bombs):
                bombs.append(newbomb)
                reroll = False
            else:
                newbomb.x = random.randint(0,17)
                newbomb.y = random.randint(0,13)

def draw():
    global seconds
    global curser
    global dead
    screen.clear()
    bg.draw()
    flagcounter = str(flaglimit-len(flags))
    stringseconds = str(seconds)
    screen.draw.text(flagcounter, (20, 433), color="red",fontname="seven segment", fontsize=25)
    screen.draw.text(stringseconds, (483, 433), color="red",fontname="seven segment", fontsize=25)
    for i in bombs:
        screenbomb = Actor("bomb")
        screenbomb.x = (i.x*30)+15
        screenbomb.y = (i.y*30)+15
        screenbomb.draw()
    for i in flags:
        screenflag = Actor("flag")
        screenflag.x = (i.x*30)+15
        screenflag.y = (i.y*30)+15
        screenflag.draw()
    for i in screensquares:
        i.draw()
    if dead == False:
        if curser == 0:
            flagcurser.draw()
        else:
            bombcurser.draw()
    if dead == True:
        stoobid.draw()
        deadface.draw()

def update():
    bombcurser.pos = pygame.mouse.get_pos()
    flagcurser.pos = pygame.mouse.get_pos()
    if len(queue) > 0:
        sqrchecker(queue[0][0],queue[0][1])
        queue.remove(queue[0])
    print(queue)

def on_key_down(key):
    global curser
    if key == key.S:
        if curser == 1:
            curser = 0
        elif curser == 0:
            curser = 1

def on_mouse_down(pos, button):
    global clearedsquares
    global seconds
    global run1
    global dead
    global curser
    if button == mouse.LEFT:
        mousebox_x = pos[0]//30
        mousebox_y = pos[1]//30
        if mousebox_y < 14:
            attempt = 0
            if curser == 1 and dead == False:
                for i in bombs:
                    if i.x == mousebox_x and i.y == mousebox_y:
                        print("game over")
                        dead = True
                        run1.cancel()
                    elif (not any(i.x == mousebox_x and i.y == mousebox_y for i in bombs)and attempt == 0):
                        attempt += 1
                if attempt > 0:
                    flagcount = 0
                    for i in flags:
                        if i.x == mousebox_x and i.y == mousebox_y:
                            flagcount += 1
                    if flagcount == 0:
                        sqrchecker(mousebox_x,mousebox_y)
            if curser == 0 and dead == False:
                flagcount = 0
                for i in flags:
                    if i.x == mousebox_x and i.y == mousebox_y:
                        flags.remove(i)
                        flagcount += 1
                if flagcount == 0 and len(flags) < flaglimit:
                    clearsquarecheck = 0
                    for i in clearedsquares:
                        if i.x == ((pos[0]//30)*30)+15 and i.y == ((pos[1]//30)*30+15):
                            clearsquarecheck += 1
                    if clearsquarecheck == 0:
                        newflag = Actor("flag")
                        newflag.x = mousebox_x
                        newflag.y = mousebox_y
                        flags.append(newflag)
        if pos[0] > 255 and pos[0] < 280 and pos[1] > 432 and pos[1] < 457 and dead == True:
            dead = False
            bombs.clear()
            clearedsquares.clear()
            screensquares.clear()
            flags.clear()
            genbombs()
            seconds = 0
            timer()
timer()
genbombs()
pgzrun.go()
