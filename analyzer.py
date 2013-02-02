import sys
import datetime
old_stdout = sys.stdout
now = datetime.datetime.now()

def average(a,b):
    a = a*100
    average = a/b
    return average
    
def loadplayers(s):
    players = []
    list = ""
    for line in s:
        list += line
    player = list.split(" ")
    for i in player:
        players.append(i)
    return players

clubname = ""
seats = ("East", "South", "West", "North")
placement = ("1st. ", "2nd. ", "3rd. ", "4th. ")

playerlist = open("players.txt", "a+")
players = loadplayers(playerlist)
playerlist.close()

print "Welcome to xkime's Offline Mahjong Stat Analyzer v 0.8\n"
print "Try to avoid strange characters. I'm not sure all of them are compatible."
print "Input your Club or Group's name:\n"
clubname = raw_input()
print
print "Players currently in the list:\n"
for player in players:
    print player
print
print "Add more players?\n"
confirm = raw_input()
if confirm in "Nono":
    confirm = False
else:
    confirm = True
while confirm:
    print "Input the player's nickname (no spaces, only players with games):\n"
    try:
        newplayer = raw_input()
        if " " in newplayer:
            print "Sorry, avoid using spaces in names."
        else:
            players.append(newplayer)
            print "%s has been added to the list.\n" % newplayer
            print "Add more?\n"
            confirm = raw_input()
            if confirm in "Nono":
                confirm = False
            else:
                confirm = True
    except ValueError:
        print "Invalid name.\n"

print "Players: \n"        
for player in players:
    print player
print "\n"
       
print "Delete a player?\n"
confirm = raw_input()
if confirm in "Nono":
    confirm = False
else:
    confirm = True
while confirm:
    print "Input the player's nickname (no spaces, please, and make sure it matches your hands.txt):\n"
    try:
        newplayer = raw_input()
        players.remove(newplayer)
        print "%s has been removed from the list.\n" % newplayer
        print "Remove more?\n"
        confirm = raw_input()
        if confirm in "Nono":
            confirm = False
        else:
            confirm = True
    except:
        print "Make sure that player is in the list, please.\n"
        
playerlist = open("players.txt","w")
sys.stdout = playerlist
for player in players:
    print player,
sys.stdout = old_stdout
playerlist.close()
        
for player in players:
    print "Analyzing %s..." % player

handcount = 0
ryuukyokucount = 0
houracount = 0
chonbocount = 0
gamecount = {i:0 for i in players}
playcount = {i:0 for i in players}
roncount = {i:0 for i in players}
dealcount = {i:0 for i in players}
tsumocount = {i:0 for i in players}
drawcount = {i:0 for i in players}
tenpaicount = {i:0 for i in players}
notencount = {i:0 for i in players}
topcount = {i:0 for i in players}
sndcount = {i:0 for i in players}
trdcount = {i:0 for i in players}
lstcount = {i:0 for i in players}
gaincount = {i:0 for i in players}
losscount = {i:0 for i in players}
ronprofit = {i:0 for i in players}
tsumoprofit = {i:0 for i in players}
houjuuloss = {i:0 for i in players}
houjuutodealercount = {i:0 for i in players}
badriichicount = {i:0 for i in players}


with open("hands.txt") as file:
    for line in file:
        part = line.split()
        if "Round" in line:
                handcount += 1
        if "Ryuukyoku" in line:
            ryuukyokucount += 1
        if "Houra" in line:
            houracount += 1
        if "Chonbo" in line:
            chonbocount += 1
        for i in players:
            if "Seat: " + i in line:
                playcount[i] += 1
            for x in placement:
                if x + i in line:
                    gamecount[i] += 1
            if i in line and "Ron" in line:
                roncount[i] += 1
                ronprofit[i] += int(part[6])
            if i + " Houjuu" in line:
                dealcount[i] += 1
                houjuuloss[i] += int(part[6])
            if i in line and "Tsumo" in line:
                tsumocount[i] += 1
                tsumoprofit[i] += int(part[6])
            if i + ": Tenpai" in line:
                tenpaicount[i] += 1
                drawcount[i] += 1
            if i + ": Noten" in line:
                notencount[i] += 1
                drawcount[i] += 1
            if placement[0] + i in line:
                topcount[i] += 1
            elif placement[1] + i in line:
                sndcount[i] += 1
            elif placement[2] + i in line:
                trdcount[i] += 1
            elif placement[3] + i in line:
                lstcount[i] += 1
            if i + " Ron" in line or i + " Tsumo" in line:
                gaincount[i] += int(part[6])
            if i + ": Tenpai: " in line:
                gaincount[i] += int(part[3])
            if (i + " Houjuu" in line) or (i + " Ko" in line) or (i + " Oya" in line):
                losscount[i] -= int(part[6])
            if i + ": Noten: " in line:
                losscount[i] -= int(part[3])
            if i + " Houjuu to-Dealer:" in line:
                houjuutodealercount[i] += 1
            if i + "'s riichi" in line:
                badriichicount[i] += 1
            if i in line and "(- 1000 Deposit)" in line:
                badriichicount[i] += 1
                
wincount = {i:roncount[i]+tsumocount[i] for i in players}
totalprofit = {i:gaincount[i]+losscount[i] for i in players}

ronrate = {i:0 for i in players}
tsumorate = {i:0 for i in players}
tenpairate = {i:0 for i in players}
houjuutodealerrate = {i:0 for i in players}

for i in players:
    if wincount[i] > 0:
        ronrate[i] = average(roncount[i],wincount[i])
        tsumorate[i] = average(tsumocount[i],wincount[i])
    if drawcount[i] > 0:
        tenpairate[i] = average(tenpaicount[i],drawcount[i])
    if dealcount[i] > 0:
        houjuutodealerrate[i] = average(houjuutodealercount[i],dealcount[i])
        
toprate = {i:0 for i in players}
sndrate = {i:0 for i in players}
trdrate = {i:0 for i in players}
lstrate = {i:0 for i in players}
winrate = {i:0 for i in players}
dealrate = {i:0 for i in players}
drawrate = {i:0 for i in players}
badriichirate = {i:0 for i in players}
profitratehand = {i:0 for i in players}
profitrategame = {i:0 for i in players}
rongainrate = {i:0 for i in players}
tsumogainrate = {i:0 for i in players}
houjuulossrate = {i:0 for i in players}

for i in players:
    if gamecount[i] > 0:
        toprate[i] = average(topcount[i],gamecount[i])
        sndrate[i] = average(sndcount[i],gamecount[i])
        trdrate[i] = average(trdcount[i],gamecount[i])
        lstrate[i] = average(lstcount[i],gamecount[i])
        profitrategame[i] = totalprofit[i]/gamecount[i]
    if playcount[i] > 0:
        winrate[i] = average(wincount[i],playcount[i])
        dealrate[i] = average(dealcount[i],playcount[i])
        drawrate[i] = average(drawcount[i],playcount[i])
        badriichirate[i] = average(badriichicount[i],playcount[i])
        profitratehand[i] = totalprofit[i]/playcount[i]
        rongainrate[i] = ronprofit[i]/playcount[i]
        tsumogainrate[i] = tsumoprofit[i]/playcount[i]
        houjuulossrate[i] = houjuuloss[i]/playcount[i]
        if roncount[i] > 0:
            rongainrate[i] = ronprofit[i]/roncount[i]
        if tsumocount[i] > 0:
            tsumogainrate[i] = tsumoprofit[i]/tsumocount[i]
        if dealcount[i] > 0:
            houjuulossrate[i] = houjuuloss[i]/dealcount[i]
                    
seiseki = open("seiseki%s.txt" % now.strftime("%Y-%m-%d"),"w")
sys.stdout = seiseki
print clubname
print
print "Date: %s \n" % now.strftime("%Y-%m-%d %H:%M")
print "Number of hands: " + str(handcount)
print "Houra rate: %s%% (%s times)" % (average(houracount,handcount), houracount)
print "Ryuukyoku rate: %s%% (%s times)" % (average(ryuukyokucount,handcount), ryuukyokucount)
print "Chonbo rate: %s%% (%s times)" % (average(chonbocount,handcount), chonbocount)
print
for i in players:
    print "--- " + i + " ---"
    print
    print "Games played: %s (%s hands)" % (gamecount[i], playcount[i])
    print "1st: %s%% (%s times)" % (toprate[i], topcount[i])
    print "2nd: %s%% (%s times)" % (sndrate[i], sndcount[i])
    print "3rd: %s%% (%s times)" % (trdrate[i], trdcount[i])
    print "4th: %s%% (%s times)" % (lstrate[i], lstcount[i])
    print "Hand win rate: %s%% (%s times)" % (winrate[i], wincount[i])
    print "Ron rate: %s%% (%s times)" % (ronrate[i], roncount[i])
    print "Average ron win: +%s points" % rongainrate[i]
    print "Tsumo rate: %s%% (%s times)" % (tsumorate[i], tsumocount[i])
    print "Average tsumo win: +%s points" %tsumogainrate[i]
    print "Deal in rate: %s%% (%s times)" % (dealrate[i], dealcount[i])
    print "--Into dealer: %s%% (%s times)" % (houjuutodealerrate[i], houjuutodealercount[i]) 
    print "Average deal in value: -%s points" %houjuulossrate[i]
    print "Ryuukyoku rate: %s%% (%s times)" % (drawrate[i], drawcount[i])
    print "Tenpai during ryuukyoku: %s%% (%s times)" % (tenpairate[i], tenpaicount[i])
    print "Fruitless riichi declarations: %s%% (%s times)" % (badriichirate[i],badriichicount[i])
    print
    print "Average point gain per game: %s" % profitrategame[i]
    print "Average point gain per hand: %s" % profitratehand[i]
    print
    print
sys.stdout = old_stdout
seiseki.close()

print "Analysis has finished. Check your seiseki.txt file. Thanks for using this tool! -xkime"
raw_input("Press any key to exit. E-mails/Support: nicobsas@gmail.com")