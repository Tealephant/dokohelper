from random import randrange
from modi import *

class Card:
    '''
    Card-Type is saved as 2 character string:
    First Letter: Suit: C: Clubs (Kreuz), S: Spades (Pik), H: Hearts (Herz), D: Diamond (Karo)
    Second Letter: Value: 9: nine, 0: ten, A: ace, j: jack, q: queen, k: king
    '''
    def __init__(self, type, trump):
        self.type = type
        self.trump = trump
    
    def GetVal(self):
        return self.type[1]
    def GetSuit(self):
        return self.type[0]

    def GetPoints(self):
        #returns the number of points a card is worth in this round
        val = self.GetVal()
        if val == '9':
            return 0
        elif val == '0':
            return 10
        elif val == 'A':
            return 11
        elif val == 'J':
            return 2
        elif val == 'Q':
            return 3
        elif val == 'K':
            return 4

#returns true if the value of card1 is strictly better than the value of card 2
def cmpCardByVal(card1, card2):
    return RANK_VAL.index(card1.GetVal()) < RANK_VAL.index(card2.GetVal())

class Trick:
    def __init__(self, nr, players, beginner):
        self.nr = nr
        self.cards = []
        self.beginner = beginner #player to play the first card
        self.players = players
        self.__winner = 0
        self.__points = 0

    def GetCard(self, pos):
        return self.cards[pos]
    
    def AddCard(self, card):
        if len(self.cards) < 4:
            self.cards.append(card)
        else:
            print("Error: Trick is already full!")
    
    def RemoveCard(self):
        if len(self.cards) > 0:
            self.cards.pop()
        
    def GetPoints(self):
        points = 0
        for card in self.cards:
            points += card.GetPoints()
        return points

    def GetWinner(self, mode):
        if self.IsCompletet():
            winner = 0 #start with beginner card, check for each card if it has a higher ranking
            highestCard = self.cards[0]
            for i in range(1, 4):
                currentCard = self.cards[i]
                if not highestCard.trump:
                    #highest card is not trump
                    if not currentCard.trump:
                        #card is not trump
                        if currentCard.GetSuit() != highestCard.GetSuit():
                            #card is of not matching suit and not trump
                            continue
                        else:
                            if cmpCardByVal(currentCard, highestCard):
                                #card is of matching suit and strictly higher value
                                highestCard = currentCard
                                winner = i
                            else:
                                continue
                    else:
                        #trump played, first time
                        highestCard = currentCard
                        winner = i
                else:
                    #highest card is trump
                    if not currentCard.trump:
                        #fehl on trumpf -> weaker
                        continue
                    else:
                        #both cards are trump -> get strongest
                        if mode.heart10active:
                            #check if second heart10 beat the first one
                            if highestCard.type == "H0" and currentCard.type == "H0":
                                #second h10 beats the first one
                                highestCard = currentCard
                                winner = i
                                continue
                        #no heart10 in this mode or already checked if special h10 case occured
                        if cmpCardByRank(currentCard, highestCard, RANKS[mode.type]):
                            #new card is strongly better (when equal, first card wins) than highestcard
                            highestCard = currentCard
                            winner = i
            #winner holds the position of the winning card. winning player is decided depending on this and the beginner
            return self.players[(winner + self.players.index(self.beginner)) % 4]
        else:
            print("Error: Cant decide winner, trick is still undecided!")
    
    #checks if the trick is full
    def IsCompletet(self):
        return len(self.cards) >= 4

    def GetCardPlayerIndex(self, pos):
        #returns the index of the player in game.players who played the card at position pos in this trick
        return (pos + self.players.index(self.beginner)) % 4

class Round:
    def __init__(self, players, beginner, mode):
        self.tricks = []
        self.players = players
        self.beginner = beginner #Player to start this round
        self.mode = mode
        self.deck = Deck(mode)
        self.NewTrick()
        #update playerPoints will reset them in case a new round is startet
        #this is needed, as the players and their are saved in the class game and not in gameround
        self.UpdatePlayerPoints()
        #the players team must also be reset
        self.ResetPlayerTeams()
        self.teamsLocked = False #true if teams are decided


    def GetPlayerPoints(self, nr):
        return self.players[nr].points

    #returns array [Repoints, Contrapoints] with points of the respective team
    def GetTeamPoints(self):
        points = [0, 0]
        for player in self.players:
            playerteam = player.team
            if playerteam == 1:
                points[0] += player.points
            elif playerteam == 2:
                points[1] += player.points
        return points
    
    def AddPlayerPoints(self, nr, points):
        self.players[nr].AddPoints(points)

    #get the cardnumber that will be played next (so new game starts at turn 1, ends at turn 48)
    def GetTurn(self):
        if len(self.tricks) > 0:
            return 4 * (len(self.tricks) - 1) + len(self.tricks[-1].cards) + 1
        else:
            print("Error: False Turnnumber")
            return 0

    def UpdatePlayerPoints(self):
        #update player points
        playerPoints = [0, 0, 0, 0]
        for trick in self.tricks:
            if trick.IsCompletet():
                winner = trick.GetWinner(self.mode)
                playerPoints[winner.nr] += trick.GetPoints()
        #update points
        for player in self.players:
            player.points = playerPoints[player.nr]

    def ResetPlayerTeams(self):
        #reset player teams
        for player in self.players:
            player.team = 0
            player.locked = False

    #adds a new empty Trick
    def NewTrick(self):
        if len(self.tricks) >= 12:
            print("Error: Already played 12 tricks!")
        else:
            beginner = self.beginner if len(self.tricks) == 0 else self.tricks[-1].GetWinner(self.mode)
            trick = Trick(len(self.tricks) + 1, self.players, beginner)
            self.tricks.append(trick)

    #plays the card at position pos in the current deck
    def playCard(self, pos):
        if self.GetTurn() > 48 or self.GetTurn() < 1:
            print("Error: Already played 12 tricks!")
        #check if the current trick is full or not
        if len(self.tricks) == 0:
            self.NewTrick()
        if 0 <= pos < len(self.deck.cards):
            #add card to trick
            self.tricks[-1].AddCard(self.deck.cards[pos])
            #add new trick if current one is full
            if self.tricks[-1].IsCompletet() and len(self.tricks) < 12:
                self.NewTrick()
            #remove card from deck
            self.deck.cards.pop(pos)
            self.UpdatePlayerPoints()
            self.CheckTeams()
        else:
            print("Error: To be played card is not in deck!")

    def CheckTeams(self):
        #checks if the teams are derivable from the current gamestate and sets them if possible    
        #reset player teams (important so the undo button workds as intended)
        self.ResetPlayerTeams()
        mode = self.mode.type    
        if mode == "normal" or mode == "normals":
            #check for CQ in normal game
            #saves amount of CQ played to detect if teams are set
            cqPlayed = 0
            for trick in self.tricks:
                for i in range(len(trick.cards)):
                    if trick.cards[i].type == "CQ":
                        #player who played this card is Re
                        pos = trick.GetCardPlayerIndex(i)
                        self.players[pos].team = 1
                        self.players[pos].locked = True
                        cqPlayed += 1
            
            if cqPlayed == 2:
                #bot CQ played -> teams are set
                for player in self.players:
                    if not player.locked:
                        #team is not automatically assigned -> these players must be contra
                        player.team = 2
                        player.locked = True
        elif mode in SOLI:
            #solo player is re, other players contra
            self.beginner.team = 1
            self.beginner.locked = True
            for player in self.players:
                if not player.locked:
                    player.team = 1
                    player.locked = True
        elif mode == "hochzeit" or mode == "hochzeits" or mode == "armut" or mode == "armuts":
            #would require team-choosing in new round menu. Pretty useless
            pass


#Players in the Game
class Player:
    def __init__(self, nr, name):
        self.nr = nr
        self.name = name
        self.roundPoints = 0
        self.team = 0 #0: undecided, 1: Re, 2: Contra
        self.locked = False #is the team locked?

    def SetName(self, name):
        self.name = name[0:14]

#Gametype of this Round
class Mode:
    def __init__(self, type):
        self.type = type
        self.heart10active = False
        if self.type in HEART10GAMES:
            self.heart10active = True

    def GetName(self):
        return MODI[self.type]

#compare 2 cards (dependent on mode)
#reference is an Array with the cards (as type strings) in descending order
def cmpCardByRank(card1, card2, reference):
    return reference.index(card1.type) < reference.index(card2.type)

class Deck:
    def __init__(self, mode):
        self.cards = []

        #add all cards to the deck
        for type in FULLDECK:
            #set trump cards depending on game mode
            if type in RANKS[mode.type]:
                for i in range(2):
                    self.cards.append(Card(type, True))
            else:
                for i in range(2):
                    self.cards.append(Card(type, False))

    #puts card back into the deck and in the correct position
    def putCardBack(self, card):
        pos = 0
        for i in self.cards:
            if cmpCardByRank(i, card, FULLDECK):
                #card has a lower rank than i, so it is sorted to the right
                pos += 1
            else:
                break
        self.cards.insert(pos, card)


class Game:
    PLAYERNAMEFILE = "playernames.txt"
    def __init__(self):
        self.players = []
        playernames = Game.readPlayerNames()
        for nr in range(4):
            self.players.append(Player(nr, playernames[nr]))
        mode = Mode("normal")
        self.gameround = Round(self.players, self.players[0], mode)
        self.readPlayerNames()
    
    def __del__(self):
        #write current playernames to file when the game is ended
        self.writePlayerNames()

    def createRandomRound(self, mode):
    #creates a random round for testing purposes
        self.gameround = Round(self.players, self.players[0], mode)
        for i in range (48, 0, -1):
            #draw random card
            pos = randrange(i)
            self.gameround.playCard(pos)

    def newRound(self, mode, beginner):
        self.gameround = Round(self.players, beginner, mode)

    def undoMove(self):
        #this is implementet in Game, so the moves of the correct gameround are undone
        if self.gameround.GetTurn() > 1:
            #moves can only be undone, if they occured
            if len(self.gameround.tricks[-1].cards) == 0:
                #no cards played in current trick -> remove last card from last trick
                self.gameround.tricks.pop() #remove new empty trick

            lastCard = self.gameround.tricks[-1].cards[-1] #get last card from trick
            self.gameround.tricks[-1].cards.pop() #remove card from trick
            self.gameround.deck.putCardBack(lastCard) #put card back in playeble deck
            self.gameround.UpdatePlayerPoints()
            self.gameround.CheckTeams()

    def writePlayerNames(self):
        #writes the current playernames into the txtfile
        txtfile = open(Game.PLAYERNAMEFILE, "w")
        for player in self.players:
            txtfile.write(player.name + "\n")
        txtfile.close()

    @staticmethod
    def readPlayerNames():
        #reads the player names from a txt file if it exists. otherwise a new file with standard playernames will be created
        formatted = FALLBACKNAMES
        try:
            playernames = open(Game.PLAYERNAMEFILE).readlines()
            if len(playernames) == 4:
                #correct amount of players
                formatted = [name[0:14].rstrip() for name in playernames] #cut names if they are too long
        except Exception: 
            pass
        return formatted

                
        