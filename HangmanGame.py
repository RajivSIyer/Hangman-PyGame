from typing_extensions import runtime
import pygame as p
import sys
import random
from pygame import key
from pygame.constants import KEYUP, K_ESCAPE, K_RETURN, MOUSEBUTTONUP 

#Initialize the game
p.init()

GAME_FONT_TITLE = p.font.SysFont(None, 100)
GAME_FONT_REG = p.font.SysFont(None, 30)
GAME_FONT_INGAME = p.font.SysFont(None, 50)
BLACK_COL = (0,0,0)
WHITE_COL = (255,255,255)
CRIMSON_COL = (220,20,60)
#create the screen
SCR_WIDTH = 1280
SCR_HEIGHT = 720
clock = p.time.Clock()
input_box = p.Rect(100, 100, 140, 32)
color_inactive = p.Color('lightskyblue3')
color_active = p.Color('dodgerblue2')
screen = p.display.set_mode((SCR_WIDTH, SCR_HEIGHT))

#Adding a Background
background = p.image.load('dungeon.jpg')
logo  = p.image.load('logoresize.png')
rope = p.image.load("hangmannoose.png")
prisoner = p.image.load("prisonerresized.png")
stool = p.image.load("stoolresize.png")

#Caption and Icon
p.display.set_caption("Hangman")

icon = p.image.load('D:\My Documents\Rajiv\Projects\Hangman PyGame\hangman-game.png')
p.display.set_icon(icon)

#Draw Text Utility function
def DrawText(text, drawsurface, fnt, x, y, fgcol, bgcol=None, align='left'):
    textobj = fnt.render(text, 1, fgcol, bgcol) # creates the text in memory (it's not on a surface yet).
    textrect = textobj.get_rect()
    #print('X: ', x,'Y: ', y)
    #print(textrect)
    if align == 'left':
        textrect.topleft = (x, y)
    if align == 'right':
        textrect.topright = (x,y)
    if align == 'center':
        textrect.midtop = (x,y)

    #print("Post alignment: ", textrect)
    screen.blit(textobj, textrect)
    p.display.update()

#Background Screen
def background_scr():
    screen.blit(background, (0,0))
    screen.blit(stool, ((20/100) * SCR_WIDTH, (70/100) * SCR_HEIGHT))
    screen.blit(prisoner, ((28/100) * SCR_WIDTH, (10/100)* SCR_HEIGHT))
    screen.blit(rope, ((31/100)* SCR_WIDTH, 0))
    DrawText("YOU'VE SINNED!", screen, GAME_FONT_REG, (SCR_WIDTH/2), SCR_HEIGHT/5.5, CRIMSON_COL, None, 'center')

#Terminate Program
def terminate():
    p.quit()
    sys.exit()

#Check for key press
def getnextkey():
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                return event.key
    #return False

def give_input():
    stringcat = ''
    while True:

        char = getnextkey()
        print(char)
        if char == K_RETURN:
            if stringcat != '':
                break
                
        elif chr(char) not in 'abcdefghijklmnopqrstuvwxyzABCDEFJHIJKLMNOPQRSTUVWXYZ':
            DrawText('Invalid character. Please try again!', screen, GAME_FONT_REG, 10, SCR_HEIGHT-40, CRIMSON_COL, None, 'left')
            continue
        else:
            stringcat += chr(char)

    return stringcat

#Game Logic Functions
def loadwords(filename, min_wordlen, max_wordlen=None):
    f = open(filename, 'rb')
    rawdata = f.read().decode('utf-8')
    listofwords = rawdata.split('\n')
    f.close()
    filtered_list = []
    for w in listofwords:
        if min_wordlen <= len(w) <= max_wordlen:
            filtered_list.append(w)
    return filtered_list

def give_word(word_list):
    #word_list = ['Mississippi','Entreupreneur', 'Abacus', 'Kangaroo', 'Flabergasted', 'abandon', 'abbreviation', 'badminton', 'becomingly', 'Behemoth', 'Capillaries']
    word = random.choice(word_list)
    word_list.remove(word)
    return word

def word_split(word):
    vowels = ['a','e','i','o','u']
    reduced_cons = []
    reduced_vowel = []
    for c in word:
        if c in vowels:
            reduced_vowel.append(c)
        else:
            reduced_cons.append(c)

    return (list(set(reduced_vowel)), list(set(reduced_cons)))

def Hint(vowels, consonants):
    if len(vowels):
        letter = random.choice(vowels)
        vowels.remove(letter)
    else:
        letter = random.choice(consonants)
        consonants.remove(letter)
    return letter

def Input_Box():

    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                terminate()
            if event.type == p.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = True
                else:
                    active = False

            if event.type == p.MOUSEBUTTONUP:
                # If the user released the click while being inside input_box rect.
                if input_box.collidepoint(event.pos):
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                else:
                    active = False

                
            if event.type == p.KEYDOWN:
                if active:
                    if event.key == p.K_RETURN:
                        if text != '':
                            print(text)
                            done = True
                            break
                            
                    elif event.key == p.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if event.unicode in 'abcdefghijklmnopqrstuvwxyzABCDEFJHIJKLMNOPQRSTUVWXYZ': 
                            text += event.unicode
                        else:
                            DrawText('Invalid character. Please try again!', screen, GAME_FONT_REG, 10, SCR_HEIGHT-40, CRIMSON_COL, None, 'left')

            #screen.fill((30, 30, 30))
            # Render the current text.
            txt_surface = GAME_FONT_REG.render(text, True, BLACK_COL)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the input_box rect.
            p.draw.rect(screen, color, input_box)
            frame_rect = input_box
            frame_rect.inflate(2,2)
            p.draw.rect(screen, CRIMSON_COL, frame_rect, 2)
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            p.display.flip()
            #clock.tick(30)
    return text

def Hangman(word):
    word = word.lower()
    empty_word = list(len(word)*'_')
    attempts = 6
    hint_cnt = 1
    vow_list, cons_list = word_split(word) 
    while attempts > 0:
        background_scr()
        showword(empty_word)
        DrawText('Guess a letter:', screen, GAME_FONT_INGAME, SCR_WIDTH/2.2, SCR_HEIGHT/1.75, WHITE_COL, None, 'left')
        ch = Input_Box()
        if ch == 'hint':
            if hint_cnt <= 5:
                hint_cnt += 1
                attempts -= 1
                ch = Hint(vow_list, cons_list)
                print('The hint letter is: ',ch)
                DrawText('The hint letter is' + ch, screen, GAME_FONT_REG, 10, SCR_HEIGHT-40, CRIMSON_COL, None, 'left')
            else:
                DrawText('Maximum two hints allowed!', screen, GAME_FONT_REG, 10, SCR_HEIGHT-40, CRIMSON_COL, None, 'left')
                print('Maximum two hints allowed!')
                continue

        elif len(ch) > 1:
            DrawText('Guess with only a letter', screen, GAME_FONT_REG, 10, SCR_HEIGHT-40, CRIMSON_COL, None, 'left')
            print('Guess with only a letter!')
            continue
        
        correct_guess = False

        for i in range(len(word)):
            if ch == word[i]:
                empty_word[i] = ch
                correct_guess = True

        if not correct_guess:
            DrawText('Your guess is incorrect. Try Again!', screen, GAME_FONT_REG, 10, SCR_HEIGHT-40, CRIMSON_COL, None, 'left')
            print("Your guess is incorrect. Try Again!")
            attempts -= 1
        
        else:
            DrawText('Your guess is correct', screen, GAME_FONT_REG, 10, SCR_HEIGHT-40, CRIMSON_COL, None, 'left')
            print('Your guess is correct!')
        
        print('Remaining attempts: ', attempts)
        showword(empty_word)

        if '_' not in empty_word:
            print("Congratulations! You won with ", attempts, ' attempt(s) remaining.')
            break
        
    else:
        print('You are Hung!')
        print('The word was: ', word)

def showword(word):
    s = ''
    for c in word:
        s += c + ' '
    DrawText(s, screen, GAME_FONT_TITLE, SCR_WIDTH/2.25, SCR_HEIGHT/1.2, WHITE_COL, None, 'left')

#RGB Screen
screen.fill((10,10,10))

#Start Screen
DrawText('HANGMAN', screen, GAME_FONT_TITLE, (SCR_WIDTH/2), SCR_HEIGHT/4, CRIMSON_COL, None, 'center')
screen.blit(logo, (SCR_WIDTH/2.5, SCR_HEIGHT/3))
DrawText("Press any key to start the game:", screen, GAME_FONT_REG, (SCR_WIDTH/2), SCR_HEIGHT - SCR_HEIGHT/6, WHITE_COL, None, 'center')

while not getnextkey():
    pass
#Game Loop

answer = 'y'
while answer.lower() != 'n':

    l = loadwords('engmix.txt', 5, 9)
    Hangman(give_word(l))
    DrawText('Do you wish to play again, Y or N: ', screen, GAME_FONT_INGAME, SCR_WIDTH/2.2, SCR_HEIGHT/1.75, WHITE_COL, None, 'left')
    answer = Input_Box()

    '''for event in p.event.get():
        if event.type == p.QUIT:
            running =  False '''        