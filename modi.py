'''
Saves all the Gamemodes with the ranks and other constants
'''

#Fallback Playernames 
FALLBACKNAMES = ["Spieler 1", "Spieler 2", "Spieler 3", "Spieler 4"]

#for creating all cards in a game
SUITS = ['C', 'S', 'H', 'D']
VALS = ['A', '0', 'K', '9', 'Q', 'J']
FULLDECK = [suit + val for suit in SUITS for val in VALS]

#ranks if no card is trump
RANK_VAL = ["A", "0", "K", "Q", "J", "9"]

#ranks used in multiple gamemodes
RANKNORMAL = ["H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "DA", "D0", "DK", "D9"]
RANKNORMALS = ["DA", "H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "D0", "DK", "D9"]

#saves the ranking of Trumpcards for the modes
RANKS = {
    "normal" : RANKNORMAL,
    "normals" : RANKNORMALS,
    "hochzeit" : RANKNORMAL,
    "hochzeits" : RANKNORMALS,
    "armut" : RANKNORMAL,
    "armuts" : RANKNORMALS,
    "karo" : RANKNORMAL,
    "karos" : RANKNORMALS,
    "herz" : ["H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "HA", "HK", "H9"],
    "herzs" : ["HA", "H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "HK", "H9"],
    "pik" : ["H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "SA", "S0", "SK", "S9"],
    "piks" : ["SA", "H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "S0", "SK", "S9"],
    "kreuz" : ["H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "CA", "C0", "CK", "C9"],
    "kreuzs" : ["CA", "H0", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ", "C0", "CK", "C9"],
    "buben" : ["CJ", "SJ", "HJ", "DJ"],
    "damen" : ["CQ", "SQ", "HQ", "DQ"],
    "könige" : ["CK", "SK", "HK", "DK"],
    "köhler" : ["CK", "SK", "HK", "DK", "CQ", "SQ", "HQ", "DQ", "CJ", "SJ", "HJ", "DJ"],
    "fleischlos" : []
}

#saves the names for the Modi
MODI = {
    "normal" : "Normalspiel",
    "normals" : "Normalspiel (Schwein)",
    "hochzeit" : "Hochzeit",
    "hochzeits" : "Hochzeit (Schwein)",
    "armut" : "Armut",
    "armuts" : "Armut (Schwein)",
    "karo" : "Karo-Solo",
    "karos" : "Karo-Solo (Schwein)",
    "herz" : "Herz-Solo",
    "herzs" : "Herz-Solo (Schwein)",
    "pik" : "Pik-Solo",
    "piks" : "Pik-Solo (Schwein)",
    "kreuz" : "Kreuz-Solo",
    "kreuzs" : "Kreuz-Solo (Schwein",
    "buben" : "Buben-Solo",
    "damen" : "Damen-Solo",
    "könige" : "König-Solo",
    "köhler" : "Köhler-Solo",
    "fleischlos" : "Fleischlos"
}

#Modes without Schwein for the mode selection menu
MODINOSCHWEIN = [
    "normal", "hochzeit", "armut", "karo", "herz", "pik", "kreuz", "buben", "damen", "könige", "köhler", "fleischlos"
]

#saves which modes are soli, to immediately assign teams (assumes that solo-player always begins the round)
SOLI = [
    "karo", "karos", "herz", "herzs", "pik", "piks", "kreuz", "kreuzs", "buben", "damen", "könige", "köhler", "fleischlos"
]

#saves in which modes the H10 has a special role
HEART10GAMES = [
    "normal", "normals", "hochzeit", "hochzeits", "armut", "armuts", "karo", "karos", "herz", "herzs",
    "pik", "piks", "kreuz", "kreuzs"
]

#saves in which modes schwein is available
SCHWEINAVAILABLE = [
    "normal", "hochzeit", "armut", "karo", "herz", "pik", "kreuz"
]