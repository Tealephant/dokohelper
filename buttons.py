import pygame as p
from colorsFonts import *

p.init()

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = p.Rect(x, y, w, h)
        self.color = COLORWHITE
        self.text = text
        self.txt_surface = FONT1.render(text, True, COLOR0)
        self.active = False

    def handle_event(self, event):
        if event.type == p.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.text = ""
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLORWHITE
            self.txt_surface = FONT1.render(self.text, True, COLOR0)
        if event.type == p.KEYDOWN:
            if self.active:
                if event.key == p.K_RETURN:
                    self.active = False
                    self.color = COLORWHITE
                elif event.key == p.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 16:
                        self.text += event.unicode
                self.txt_surface = FONT1.render(self.text, True, COLOR0)

    def draw(self, screen):
        p.draw.rect(screen, COLORWHITE, self.rect, 0)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        p.draw.rect(screen, self.color, self.rect, 2)

class ReContraPair:
    def __init__(self, x, y, game, nr):
        self.txt_surface1 = FONT1.render("Re", True, COLOR0)
        self.txt_surface2 = FONT1.render("Contra", True, COLOR0)
        self.rect1 = p.Rect(x, y, self.txt_surface1.get_width() + 10, self.txt_surface1.get_height() + 10)
        self.rect2 = p.Rect(x + self.rect1.width + 30, y, self.txt_surface2.get_width() + 10, self.txt_surface2.get_height() + 10)
        self.game = game
        self.nr = nr #playernr for this box

    def draw(self, screen):
        screen.blit(self.txt_surface1, (self.rect1.x+5, self.rect1.y+5))    
        screen.blit(self.txt_surface2, (self.rect2.x+5, self.rect2.y+5))
        #redraws borders depending on which option is active
        active = self.game.players[self.nr].team
        locked = self.game.players[self.nr].locked
        if active == 0:
            #remove highlighting borders
            p.draw.rect(screen, COLORWHITE, self.rect1, 2)
            p.draw.rect(screen, COLORWHITE, self.rect2, 2)
        elif active == 1:
            if locked:
                p.draw.rect(screen, COLORRED, self.rect1, 2)
            else:
                p.draw.rect(screen, COLOR0, self.rect1, 2)
            p.draw.rect(screen, COLORWHITE, self.rect2, 2)
        elif active == 2:
            p.draw.rect(screen, COLORWHITE, self.rect1, 2)
            if locked:
                p.draw.rect(screen, COLORRED, self.rect2, 2)
            else:
                p.draw.rect(screen, COLOR0, self.rect2, 2)

    def handle_event(self, event):
        #handle the clicks
        if not self.game.players[self.nr].locked:
            #only changable if not locked
            if event.type == p.MOUSEBUTTONDOWN:
                active = self.game.players[self.nr].team
                if self.rect1.collidepoint(event.pos):
                    #re selected
                    if active == 1:
                        self.game.players[self.nr].team = 0
                    else:
                        self.game.players[self.nr].team = 1
                elif self.rect2.collidepoint(event.pos):
                    #contra selected
                    if active == 2:
                        self.game.players[self.nr].team = 0
                    else:
                        self.game.players[self.nr].team = 2

class Button:
    def __init__(self, screen, x, y, text, callback, color, hoverColor):
        self.screen = screen
        self.text = text
        self.callback = callback
        self.color = color
        self.hoverColor = hoverColor
        self.text_surface = FONT1.render(text, True, color)
        self.text_surface_hover = FONT1.render(text, True, hoverColor)
        self.rect = p.Rect(x, y, self.text_surface.get_width() + 10, self.text_surface.get_height() + 10)
        self.hover = False

    def draw(self):
        txt_surface = self.text_surface_hover if self.hover else self.text_surface #hovereffect
        self.screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))    
        color = self.hoverColor if self.hover else self.color
        p.draw.rect(self.screen, color, self.rect, 2)
        
    def handle_event(self, event):
        if event.type == p.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()  # Call the function.
        elif event.type == p.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
    
class RadioBox:
    def __init__(self, screen, x, y, text, color, hoverColor):
        self.screen = screen
        self.text = text
        self.color = color
        self.hoverColor = hoverColor
        self.text_surface = FONT1.render(self.text, True, color)
        self.text_surface_hover = FONT1.render(self.text, True, hoverColor)
        self.rect = p.Rect(x, y, self.text_surface.get_width() + 10, self.text_surface.get_height() + 10)
        self.hover = False
        self.active = False

    def draw(self):
        self.text_surface = FONT1.render(self.text, True, self.color)
        self.text_surface_hover = FONT1.render(self.text, True, self.hoverColor)
        txt_surface = self.text_surface_hover if self.hover else self.text_surface #hovereffect
        self.screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))    
        color = self.hoverColor if self.hover else self.color
        if self.active:
            color = COLORRED
        p.draw.rect(self.screen, color, self.rect, 2)
    
    def handle_event(self, event):
        #only responsible for the hovereffect
        if event.type == p.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

    def GetWidth(self):
        return self.rect.w 

class RadioBoxGroup:
    def __init__(self, screen, x, y, maxWidth, texts, keys, active=0):
        self.screen = screen
        self.x = x
        self.y = y
        self.maxWidth = maxWidth
        self.active = active
        self.boxes = []
        self.texts = texts
        self.keys = keys

        self.yHeight = 50 #height of boxline in case there are multiple lines
        #create the buttons
        xOffset = 0
        self.yOffset = 0 #needed to determine height
        #x and y offset determine the position of the boxes depending on how many there are
        for text in self.texts:
            box = RadioBox(self.screen, self.x + xOffset, self.y + self.yOffset, text, COLOR0, COLOR_ACTIVE)
            if xOffset + box.GetWidth() > self.maxWidth:
                #boxline is to big, put rest of boxes in new line
                xOffset = 0
                if len(self.boxes) != 0:
                    #first box should not have additional yOffset
                    self.yOffset += self.yHeight
                box = RadioBox(self.screen, self.x + xOffset, self.y + self.yOffset, text, COLOR0, COLOR_ACTIVE)
            self.boxes.append(box)
            xOffset += self.boxes[-1].GetWidth() + 10
        #notify active box of its status
        self.boxes[active].active = True

    def draw(self):
        #hovereffect
        for box in self.boxes:
            box.draw()

    def returnSelected(self):
        #returns the textkey (doesnt need to be the text actually displayed on the button) of the selected box
        return self.keys[self.active]

    def GetHeight(self):
        #returns the height of the boxes. dependent on how many buttons are inside
        return self.yHeight + self.yOffset

    def handle_event(self, event):
        #handle hover
        for box in self.boxes:
            box.handle_event(event)
        #handle the clicks
        if event.type == p.MOUSEBUTTONDOWN:
            for box in self.boxes:
                if box.rect.collidepoint(event.pos):
                    self.active = self.boxes.index(box)
                    #let active box kno, that it is active
                    for i in range(len(self.boxes)):
                        if i == self.active:
                            self.boxes[i].active = True
                        else:
                            self.boxes[i].active = False
                    break
