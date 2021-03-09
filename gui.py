from colorsFonts import *
from buttons import *
from roundedRectangle import *
from dokoengine import *

VERSION = "0.0.1"

p.display.set_caption("Dokohelper V" + VERSION)
WIDTH = 1920
HEIGHT = 1000
MAX_FPS = 15


class GameGUI:
    CARDIMAGES = {}
    CARDIMAGESHIGHLIGHTED = {}
    CARDHEIGHT = 140
    CARDWIDTH = 98
    def __init__(self, game, screen):
        self.screen = screen
        self.game = game 
        self.sideboard = Sideboard(self.game, self.screen)
        self.remaining = Remaining(self.game, self.screen)
        self.trickView = TrickView(self.game, self.screen)
        GameGUI.loadCardImages()

    def draw(self):
        self.screen.fill(COLORWHITE)
        self.trickView.draw()
        self.sideboard.draw()
        self.remaining.draw()

    def handleEvents(self, event):
        self.sideboard.handleEvents(event)
        self.remaining.handleCardClick(event)

    #draw a card, located here as it is used in multiple classes
    @staticmethod
    def drawCard(screen, card, x, y, width, height, highlighted):
        #draws a Card with the top-left corner at (x,y)
        draw_bordered_rounded_rect(screen, p.Rect(x, y, width+1, height+1), COLOR2, COLOR1, 7, 3)
        if highlighted:
            screen.blit(GameGUI.CARDIMAGESHIGHLIGHTED[card.GetType()], p.Rect(x, y, width, height))
        else:
            screen.blit(GameGUI.CARDIMAGES[card.GetType()], p.Rect(x, y, width, height))

    #load in images of the cards
    @staticmethod
    def loadCardImages():
        for card in FULLDECK:
            GameGUI.CARDIMAGES[card] = p.transform.scale(p.image.load("cards/" + card + ".png"), (GameGUI.CARDWIDTH, GameGUI.CARDHEIGHT))
            GameGUI.CARDIMAGESHIGHLIGHTED[card] = p.transform.scale(p.image.load("cards/" + card + "h.png"), (GameGUI.CARDWIDTH, GameGUI.CARDHEIGHT))

class TrickView:
    #displays the tricks
    CARDHEIGHT = 140
    CARDWIDTH = 98
    TRICKWIDTH = 10 + (CARDWIDTH + 10) * 4
    TRICKHEIGHT = CARDHEIGHT + 55

    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

    def drawTrick(self, trick, x, y):
        #draws a box containing the cards played, the points made, and the winner of the trick
        #players must be passed to correctly display who played which card
        draw_bordered_rounded_rect(self.screen, p.Rect(x, y, self.TRICKWIDTH, self.TRICKHEIGHT), COLOR3, COLOR0, 7, 1)
        #draw headline: Trick Number, Points, Winner
        text = FONT1.render("Stich " + str(trick.nr) + ":", True, COLOR0)
        self.screen.blit(text, [x + 10, y + 4])
        textPoints = FONT2.render("Punkte: " + str(trick.GetPoints()), True, COLOR0)
        self.screen.blit(textPoints, [x + 150, y + 8])
        #get the winner if the trick is completet
        if trick.IsCompletet():
            textWinner = FONT2.render("Gewinner: " + trick.GetWinner(self.game.gameround.mode).GetName(), True, COLOR0)
        else:
            textWinner = FONT2.render("Gewinner: --", True, COLOR0)
        self.screen.blit(textWinner, [x + 250, y + 8])
        #draw Cards
        for i in range(4):
            #draw played card
            cardx = x + 8 + i * (TrickView.CARDWIDTH + 10)
            #draw empty spaces for undecided cards
            if i < len(trick.cards):            
                GameGUI.drawCard(self.screen, trick.cards[i], cardx, y + 30, TrickView.CARDWIDTH, TrickView.CARDHEIGHT, False)
            else:
                draw_bordered_rounded_rect(self.screen, p.Rect(cardx, y + 30, TrickView.CARDWIDTH+1, TrickView.CARDHEIGHT+1), COLOR2, COLOR1, 7, 2)
            #draw player who played the card
            #draw winner highlighted
            color = COLOR0
            if trick.IsCompletet() and trick.players[(i + trick.beginner.GetNr()) % 4] == trick.GetWinner(self.game.gameround.mode):
                color = COLORRED
            playername = FONT2.render(trick.players[(i + trick.beginner.GetNr()) % 4].GetName(), True, color)
            self.screen.blit(playername, [cardx + 5, y + 35 + TrickView.CARDHEIGHT])

    def draw(self):
        for i in range(len(self.game.gameround.tricks)):
            x = (i % 3) * (self.TRICKWIDTH + 5) + 5
            y = (i // 3) * (self.TRICKHEIGHT + 5) + 5
            self.drawTrick(self.game.gameround.tricks[i], x, y)


class NewRoundMenu:
    STARTX = 550
    STARTY = 100
    WIDTH = 700
    HEIGHT = 600
    def __init__(self, screen, players, game):
        self.screen = screen
        self.game = game #required to start the new round from the menu
        #create Buttons for each gamemode
        self.modes = [mode for mode in MODI]
        self.players = [player.GetName() for player in players]
        self.active = False
        self.modeNames = [MODI[mode] for mode in self.modes]
        self.modeBoxes = RadioBoxGroup(self.screen, self.STARTX + 50, self.STARTY + 80, self.WIDTH - 100, self.modeNames, self.modes)
        self.playerBoxes = RadioBoxGroup(self.screen, self.STARTX + 50, self.STARTY + 110 + self.modeBoxes.GetHeight(), self.WIDTH - 100, self.players, self.players)
        self.exitButton = Button(self.screen, self.STARTX + self.WIDTH - 300, self.STARTY + self.HEIGHT - 70, "Abbrechen", self.cancel, COLOR0, COLOR_ACTIVE)
        self.startButton = Button(self.screen, self.STARTX + self.WIDTH - 150, self.STARTY + self.HEIGHT - 70, "Starten", self.start, COLOR0, COLOR_ACTIVE)

    def cancel(self):
        self.active = False

    def start(self):
        self.active = False
        #get selected mode from the modeBoxes
        mode = Mode(self.modeBoxes.returnSelected())
        beginner = self.game.players[self.playerBoxes.active]
        self.game.newRound(mode, beginner)

    def draw(self):
        if self.active:
            #draw background
            rect = p.Rect(self.STARTX, self.STARTY, self.WIDTH, self.HEIGHT)
            draw_rounded_rect(self.screen, rect, COLOR3, 20)
            draw_bordered_rounded_rect(self.screen, rect, COLOR3, COLOR0, 20, 3)
            #draw mode selection
            textMode = FONT0.render("Spielauswahl: ", True, COLOR0)
            self.screen.blit(textMode, [self.STARTX + 50, self.STARTY + 30])
            self.modeBoxes.draw()
            #draw player selection
            textPlayer = FONT0.render("Startspieler: ", True, COLOR0)
            self.screen.blit(textPlayer, [self.STARTX + 50, self.STARTY + self.modeBoxes.GetHeight() + 85])
            self.playerBoxes.draw()
            #draw exxit and start button
            self.exitButton.draw()
            self.startButton.draw()
    
    def handle_event(self, event):
        self.modeBoxes.handle_event(event)
        self.playerBoxes.handle_event(event)
        self.exitButton.handle_event(event)
        self.startButton.handle_event(event)
    
    def updatePlayerNames(self, players):
        #updates the player names in case they got changed. should be called before opening the menu
        self.players = [player.GetName() for player in players]
        self.playerBoxes = RadioBoxGroup(self.screen, self.STARTX + 50, self.STARTY + 180, self.WIDTH - 100, self.players, self.players)


#draws the remaining cards, that have not been played yet
class Remaining:
    CARDOFFSET = 36
    STARTX = 30
    STARTY = HEIGHT - 165
    CARDHEIGHT = 140
    CARDWIDTH = 98

    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.hovercard = -1 #save the cardindex of the card affected by hover


    def draw(self):
        #overdraw with white
        cardCount = len(self.game.gameround.deck.cards)
        rect = p.Rect(self.STARTX, self.STARTY, self.CARDOFFSET * 48 + 2, self.CARDHEIGHT + 2)
        p.draw.rect(self.screen, p.Color("white"), rect, 0)
        #draw cards
        for i in range(len(self.game.gameround.deck.cards)):
            if i == self.hovercard:
                #this card is hovered and must be highlighted
                GameGUI.drawCard(self.screen, self.game.gameround.deck.cards[i], self.STARTX + i * self.CARDOFFSET, self.STARTY, self.CARDWIDTH, self.CARDHEIGHT, True)
            else:
                GameGUI.drawCard(self.screen, self.game.gameround.deck.cards[i], self.STARTX + i * self.CARDOFFSET, self.STARTY, self.CARDWIDTH, self.CARDHEIGHT, False)

    def handleCardClick(self, event):
        if event.type == p.MOUSEBUTTONDOWN:
            lastCardOffset = len(self.game.gameround.deck.cards) - 1
            for pos in range(lastCardOffset):
                rect = p.Rect(self.STARTX + pos * self.CARDOFFSET, self.STARTY, self.CARDOFFSET, self.CARDHEIGHT)
                if rect.collidepoint(event.pos):
                    self.game.gameround.playCard(pos)
                    break
            #check last card seperately because it has larger hitbox
            if lastCardOffset >= 0:
                rect = p.Rect(self.STARTX + lastCardOffset * self.CARDOFFSET, self.STARTY, self.CARDWIDTH, self.CARDHEIGHT)
                if rect.collidepoint(event.pos):
                    self.game.gameround.playCard(lastCardOffset)
        elif event.type == p.MOUSEMOTION:
            #hovereffect
            self.hovercard = -1 #reset hovercard
            lastCardOffset = len(self.game.gameround.deck.cards) - 1
            for pos in range(lastCardOffset):
                rect = p.Rect(self.STARTX + pos * self.CARDOFFSET, self.STARTY, self.CARDOFFSET, self.CARDHEIGHT)
                if rect.collidepoint(event.pos):
                    self.hovercard = pos
                    break
            if lastCardOffset >= 0:
                rect = p.Rect(self.STARTX + lastCardOffset * self.CARDOFFSET, self.STARTY, self.CARDWIDTH, self.CARDHEIGHT)
                if rect.collidepoint(event.pos):
                    self.hovercard = lastCardOffset


class Sideboard:
    SIDEBOARDWIDTH = 550
    STARTX = WIDTH - SIDEBOARDWIDTH
    STARTY = 30
    def __init__(self, game, screen):
        self.playerFields = []
        self.boxPairs = []
        self.screen = screen
        self.game = game
        self.undoButton = Button(self.screen, self.STARTX, self.STARTY + 450, "Rückgängig", self.game.undoMove, COLOR0, COLOR_ACTIVE)
        self.newRoundButton = Button(self.screen, self.STARTX + 200, self.STARTY + 450, "Neue Runde", self.openNewRoundMenu, COLOR0, COLOR_ACTIVE)
        self.newRoundMenu = NewRoundMenu(self.screen, self.game.players, self.game)

        for i in range(4):
            self.playerFields.append(InputBox(self.STARTX, self.STARTY + 65 + i * 50, 200, 32, self.game.gameround.players[i].GetName()))
            self.boxPairs.append(ReContraPair(self.STARTX + 280, self.STARTY + 65 + i * 50, self.game, i))
        

    def draw(self):
        textMode = FONT0.render("Spielmodus: " + self.game.gameround.mode.GetName(), True, COLOR0)
        self.screen.blit(textMode, [self.STARTX, self.STARTY])
        self.drawPlayers()
        for playerField in self.playerFields:
            playerField.draw(self.screen)
        for boxPair in self.boxPairs:
            boxPair.draw(self.screen)
        self.drawTeamScore()
        self.undoButton.draw()
        self.newRoundButton.draw()
        self.newRoundMenu.draw()

    def handleInputBoxes(self, event):
        for i in range(len(self.playerFields)):
            self.playerFields[i].handle_event(event)
            #update playernames
            self.game.gameround.players[i].SetName(self.playerFields[i].text)

    def handleReContraPairs(self, event):
        for i in range(len(self.boxPairs)):
            self.boxPairs[i].handle_event(event)

    def handleEvents(self, event):
        self.handleInputBoxes(event)
        self.handleReContraPairs(event)
        self.undoButton.handle_event(event)
        self.newRoundButton.handle_event(event)
        if self.newRoundMenu.active:
            self.newRoundMenu.handle_event(event)

    def drawPlayers(self):
        for i in range(4):
            player = self.game.gameround.players[i]
            strPlayerinfo = str(player.GetPoints())
            strPlayerinfo += (5 - len(strPlayerinfo)) * " "
            textPlayerinfo = FONT1.render(strPlayerinfo, True, COLOR0)
            self.screen.blit(textPlayerinfo, [self.STARTX + 220, self.STARTY + 70 + i * 50])

    def drawTeamScore(self):
        textHeadline = FONT1.render("Teampunkte:", True, COLOR0)
        self.screen.blit(textHeadline, [self.STARTX, self.STARTY + 300])       
        textRe = FONT1.render("Re:", True, COLOR0)
        self.screen.blit(textRe, [self.STARTX, self.STARTY + 330])
        textContra = FONT1.render("Contra:", True, COLOR0)
        self.screen.blit(textContra, [self.STARTX, self.STARTY + 360])
        #display points of teams
        [rePoints, contraPoints] = self.game.gameround.GetTeamPoints()
        #overdraw old score
        p.draw.rect(self.screen, p.Color("white"), p.Rect(self.STARTX + 100, self.STARTY + 330, 50, 30), 0)
        p.draw.rect(self.screen, p.Color("white"), p.Rect(self.STARTX + 100, self.STARTY + 360, 50, 30), 0)
        #draw points
        textRePoints = FONT1.render(str(rePoints), True, COLOR0)
        self.screen.blit(textRePoints, [self.STARTX + 100, self.STARTY + 330])
        textContraPoints = FONT1.render(str(contraPoints), True, COLOR0)
        self.screen.blit(textContraPoints, [self.STARTX + 100, self.STARTY + 360])

    def openNewRoundMenu(self):
        #update the names with the player buttons in case they got changed
        self.newRoundMenu.updatePlayerNames(self.game.players)
        self.newRoundMenu.active = True
            
