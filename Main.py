#!/usr/bin/env python
import datetime
import sys
from mahjong import *

print "Welcome! Mahjong Score Calculator v0.9 (Beta)\n"
print "xkime (c)2013 All Wrongs Reserved\n"
"""Pardon my noobness at programming and Python in general.
Forward any bugs you find to xkime (nicobsas at gmail).
Feel free to build a GUI. Just e-mail me about it,
it would be cool for me to see it."""

table = Board()
players = playerRegistration()
start = datetime.datetime.now()

print "Start time: %s \n" % start.strftime("%Y-%m-%d %H:%M")

while table.continues:
    table.description()
    print
    for player in players:
        player.description()
    print
    loser = 0
    winner = getWinner() - 1
    if winner < 4:
        agari = winType()
        if agari == 1:
            loser = getLoser() - 1
            while winner == loser:
                print "Derp, you can't ron yourself!"
                loser = getLoser()
        fan = getFan()
        fu = getFu()
        winning_hand = Houra(fan,fu)
        table.agari(players,winning_hand,winner,loser,agari,sys,datetime)
    elif winner == 4:
        table.ryuukyoku(players,sys,datetime)
    else:
        chonbo(sys,table)
    table.continueGame(players)
    
finalOutput(players,datetime,sys,start,table)    
finalScores(players,table,datetime)

raw_input("Thanks for using this tool. Press any key to exit.")