'''
Saves all the Gamemodes with the ranks
'''

#for creating all cards in a game
SUITS = ['C', 'S', 'H', 'D']
VALS = ['A', '0', 'K', '9', 'Q', 'J']
FULLDECK = [suit + val for suit in SUITS for val in VALS]

#ranks for different gamemodes
RANK_VAL = ["A", "0", "K", "Q", "J", "9"] #ranks if no card is trump
#trump cards in normal game 
RANK_NORMAL = ["H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "DA", "D0", "DK", "D9"]
#

#saves which entry in TRUMPCARDS has to be chosen for a specific mode
DECKFORMODE = {
    "normal" : "normal"
}

#saves the trumpcards depending on the gamemode
TRUMPCARDS = {
    "normal" : ["CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "DA", "D0", "D9", "DK", "H0"]
}

#saves the names for the Modi
MODI = {
    "normal" : "Normalspiel"
}

#saves in which modes the H10 has a special role
HEART10GAMES = ["normal"]

#saves the ranking of Trumpcards for the modes
RANKS = {
    "normal" : RANK_NORMAL
}

#Fallback Playernames 
FALLBACKNAMES = ["Spieler 1", "Spieler 2", "Spieler 3", "Spieler 4"]