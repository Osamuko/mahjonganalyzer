def separation():
    print "-------------------------------------------------------------------"

def roundValue(value):
    if value % 100 == 0:
        return value
    else:
        return int(value + 100) - (value % 100)
        
def playerRegistration():
    print "Please, input the players' names.\n"
    global player1, player2, player3, player4, players

    player1 = Player(raw_input("East: "), "East")
    player2 = Player(raw_input("South: "), "South")
    player3 = Player(raw_input("West: "), "West")
    player4 = Player(raw_input("North: "), "North")

    players = [player1, player2, player3, player4]
    print
    return players
    
def getWinner():
    invalid_input = "Please, enter a number from 1 to 6.\n"
    winner_input = False
    while winner_input == False:
        try:
            winner = int(raw_input("WINNER: 1.%s | 2.%s | 3.%s | 4.%s | 5.Draw | 6.Chonbo\n" \
            % (players[0].name,players[1].name,players[2].name,players[3].name)))
            if winner in range(1,7):
                winner_input = True
            else:
                print invalid_input
        except ValueError:
            print invalid_input
    return winner
    
def winType():
    invalid_input = "Please, choose 1 or 2"
    agari_input = False
    while agari_input == False:
        try:
            agari = int(raw_input("1.Ron | 2.Tsumo\n"))
            if agari in range(1,3):
                agari_input = True
            else:
                print invalid_input
        except ValueError:
            print invalid_input
    return agari
            
def getLoser():
    invalid_input = "Please, enter a number from 1 to 4"
    loser_input = False
    while loser_input == False:
        try:
            loser = int(raw_input("LOSER: 1.%s | 2.%s | 3.%s | 4.%s\n" \
            %(players[0].name,players[1].name,players[2].name,players[3].name)))
            if loser in range(1,5):
                loser_input = True
            else:
                print invalid_input
        except ValueError:
            print invalid_input
    return loser
    
def chonbo(sys,table):
    invalid_input = "Please, enter a number from 1 to 5"
    chonbo_input = False
    while chonbo_input == False:
        try:
            chonbo = int(raw_input("CHONBO: 1.%s | 2.%s | 3.%s | 4.%s | 5.Cancel\n" \
            %(players[0].name,players[1].name,players[2].name,players[3].name)))
            if chonbo in range(1,6):
                chonbo_input = True
            else:
                print invalid_input
        except ValueError:
            print invalid_input
    chonbo -= 1
    chonbo_confirm = raw_input("Are you sure? Y/N")
    if chonbo_confirm in "Yesyes":
        if chonbo < 4:
            if players[chonbo].isDealer():
                old_stdout = sys.stdout
                hands = open('hands.txt','a')
                sys.stdout = hands
                table.description()
                print
                for player in players:
                    player.description()
                print "%s: Dealer Chonbo: -12000 (+4000 all)" % players[chonbo].name
                sys.stdout = old_stdout
                hands.close()
                separation()
                print "%s: Dealer Chonbo: -12000 (+4000 all)" % players[chonbo].name
                players[chonbo].takeScore(12000)
                table.addKyoku()
                for player in players:
                    if player != players[chonbo]:
                        player.addScore(4000)
            else:
                old_stdout = sys.stdout
                hands = open('hands.txt','a')
                sys.stdout = hands
                table.description()
                print
                for player in players:
                    player.description()
                print "%s: No-Dealer Chonbo: -8000 (+2000/+4000)" % players[chonbo].name
                sys.stdout = old_stdout
                hands.close()
                separation()
                print "%s: No-Dealer Chonbo: -8000 (+2000/+4000)" % players[chonbo].name
                players[chonbo].takeScore(8000)
                for player in players:
                    if player != players[chonbo]:
                        if player.isDealer():
                            player.addScore(4000)
                        else:
                            player.addScore(2000)
    
def getFan():
    invalid_input = "Please, enter a correct fan number"
    fan = 0
    while (fan < 1):
        try:
            fan = int(raw_input("Fan: "))
        except ValueError:
            print invalid_input
            fan = 0
    return fan
    
def getFu():
    invalid_input = "Please, enter a correct fu number"
    fu = 0
    while (fu < 1):
        try:
            fu = int(raw_input("Fu: "))
        except ValueError:
            print invalid_input
            fu = 0
    return fu    
    
def getRiichi():
    invalid_input = "Please, select a valid player or cancel"
    reacher_input = False
    while reacher_input == False:
        try:
            reacher = int(raw_input("Add riichi stick?\n\n1.%s | 2.%s | 3.%s | 4.%s | 5.Cancel\n" \
            % (players[0].name, players[1].name, players[2].name, players[3].name)))
            if reacher in range(1,6):
                reacher_input = True
            else:
                print invalid_input
        except ValueError:
            print invalid_input
    return reacher
    
def orderPlayers(scoreboard):
    return sorted(scoreboard.items(), key=lambda x: x[1])
    
def tally(list):
    list.sort()
    for i in range(4):
        if list[i] >= 0:
            list[i] = (int((list[i] + 500)/1000)) -30
        else:
            list[i] = (int((list[i] - 500)/1000)) -30
    list[0] -= 20
    list[1] -= 10
    list[2] += 10
    list[3] = abs(list[0]+list[1]+list[2])
    list.sort(reverse=True)
    return list
    
def finalScores(players,table,datetime):
    end = datetime.datetime.now()
    separation()
    print "End time: %s" % end.strftime("%Y-%m-%d %H:%M")
    placement = ("1st","2nd","3rd","4th")
    rawscores = [i.score for i in players]
    rawscores.sort(reverse=True)
    scores = tally([i.score for i in players])
    scoreboard = {i.name:i.score for i in players}
    scoreboard = orderPlayers(scoreboard)
    separation()
    old_deposits = table.deposits
    for i in range(4):
        print "%s. %s: %s (%s)\n" %(placement[i], scoreboard[3-i][0], \
        rawscores[i]+table.deposits*1000, scores[i])
        table.resetDeposits()
    table.deposits = old_deposits
    separation()
    
def finalOutput(players,datetime,sys,start,table):
    old_stdout = sys.stdout
    hands = open("hands.txt","a")
    scores = open("scores.txt","a")
    sys.stdout = hands
    finalScores(players,table,datetime)
    sys.stdout = scores
    separation()
    print "Start time: %s" % start.strftime("%Y-%m-%d %H:%M")
    finalScores(players,table,datetime)
    hands.close()
    scores.close()
    sys.stdout = old_stdout

class Board(object):
    def __init__(self):
        self.round = "East"
        self.honba = 0
        self.kyoku = 0
        self.deposits = 0
        self.people_in_tenpai = 0
        self.people_in_noten = 0
        self.continues = True
        
    def nextRound(self):
        if self.round == "East":
            self.round = "South"
        elif self.round == "South":
            self.round = "West"
            
    def addHonba(self):
        self.honba += 1
        
    def addKyoku(self):
        self.kyoku += 1
        
    def addDeposits(self,deposits):
        self.deposits += deposits
        
    def description(self):
        separation()
        print "%s Round %s - Honba: %s - Deposits: %s" \
        % (self.round, self.kyoku+1, self.honba, self.deposits)
        
    def resetHonba(self):
        self.honba = 0
        
    def resetKyoku(self):
        self.kyoku = 0
    
    def resetDeposits(self):
        self.deposits = 0
            
    def agari(self,players,winning_hand,winner,loser,agari,sys,datetime):
        separation()
        if winner in range(4):
            self.agariOutput(players,winning_hand,winner,loser,agari)
        separation()
        print
        confirm = raw_input("Are you sure this is okay? Y/N\n")
        if confirm in "Yesyes":
            old_stdout = sys.stdout
            hands = open('hands.txt','a')
            sys.stdout = hands
            separation()
            now = datetime.datetime.now()
            print now.strftime("%Y-%m-%d %H:%M")
            self.description()
            print
            for player in players:
                player.description()
            self.agariOutput(players,winning_hand,winner,loser,agari)
            separation()
            sys.stdout = old_stdout
            hands.close()
            if players[winner].isDealer():
                if agari == 1:
                    players[winner].score += \
                    winning_hand.ronAgari("dealer",self.honba,self.deposits)
                    players[loser].score -= \
                    winning_hand.houjuu("to dealer",self.honba)
                else:
                    players[winner].score += \
                    winning_hand.tsumoAgari("dealer",self.honba,self.deposits)
                    for i in range(4):
                        if i != winner:
                            players[i].score -= \
                            winning_hand.tsumoKaburi("by dealer","nodealer",self.honba)
                self.addHonba()
            else:
                if agari == 1:
                    players[winner].score += \
                    winning_hand.ronAgari("nodealer",self.honba,self.deposits)
                    players[loser].score -= \
                    winning_hand.houjuu("to nodealer",self.honba)
                else:
                    players[winner].score += \
                    winning_hand.tsumoAgari("nodealer",self.honba,self.deposits)
                    for i in range(4):
                        if i != winner:
                            if players[i].isDealer():
                                players[i].score -= \
                                winning_hand.tsumoKaburi("by nodealer","dealer",self.honba)
                            else:
                                players[i].score -= \
                                winning_hand.tsumoKaburi("by nodealer","nodealer",self.honba)
                self.resetHonba()
                self.addKyoku()
                for player in players:
                    player.rotateSeat()
            self.resetDeposits()
        
            riichi_check = raw_input("Did someone riichi? Y/N \n")
            if riichi_check in "Yesyes":
                riichi_check = True
            else:
                riichi_check = False
            while riichi_check:
                reacher = getRiichi() - 1
                if reacher == 4:
                    break
                confirm = raw_input("%s's riichi stick will go to %s. Is this okay? Y/N" \
                % (players[reacher].name, players[winner].name))
                if confirm in "Yesyes":
                    players[reacher].takeScore(1000)
                    players[winner].addScore(1000)
                    print "%s's riichi stick went to %s" \
                    % (players[reacher].name, players[winner].name)
                    old_stdout = sys.stdout
                    hands = open('hands.txt','a')
                    sys.stdout = hands
                    print "%s's riichi stick went to %s" \
                    % (players[reacher].name, players[winner].name)
                    sys.stdout = old_stdout
                    hands.close()
                    more = raw_input("Any more? Y/N")
                    if more in "Nono":
                        riichi_check = False
                else:
                    print "Sorry, let's try again"
        else:
            print "Sorry, one more time"
            
    def ryuukyoku(self,players,sys,datetime):
        self.people_in_tenpai = 0
        self.people_in_noten = 0
        newdeposit = 0
        for player in players:
            print "%s: 1.Tenpai | 2.Noten | 3.Riichi" % player.name
            player.isTenpai()
            if player.tenpai:
                self.people_in_tenpai += 1
            else:
                self.people_in_noten += 1
            print player.name, player.tenpaiDeclaration()
        separation()
        self.ryuukyokuOutput(players)
        separation()
        dealer = 0
        confirm = raw_input("Proceed with this? Y/N")
        if confirm in "Yesyes":
            old_stdout = sys.stdout
            hands = open('hands.txt','a')
            sys.stdout = hands
            separation()
            now = datetime.datetime.now()
            print now.strftime("%Y-%m-%d %H:%M")
            self.description()
            print
            for player in players:
                player.description()
            separation()
            self.ryuukyokuOutput(players)
            separation()
            sys.stdout = old_stdout
            hands.close()
            for player in players:
                if player.isDealer():
                    dealer = player
                if player.riichi == 1:
                    self.addDeposits(1)
                    player.takeScore(1000)
                if self.people_in_tenpai != 0 and self.people_in_noten != 0:
                    if player.tenpai:
                        player.addScore(3000/self.people_in_tenpai)
                    else:
                        player.takeScore(3000/self.people_in_noten)          
            self.addHonba()
            if not dealer.tenpai:
                self.addKyoku()
                for player in players:
                    player.rotateSeat()
        else:
            print "Sorry, one more time"
            
    def agariOutput(self,players,winning_hand,winner,loser,agari):
        print "---------- Houra ----------"
        if players[winner].isDealer():
            if agari == 1:
                print players[winner].name,
                winning_hand.printRonAgari("dealer",self.honba,self.deposits)
                print players[loser].name,
                winning_hand.printHoujuu("to dealer",self.honba)
            else:
                print players[winner].name,
                winning_hand.printTsumoAgari("dealer",self.honba,self.deposits)
                for i in range(4):
                    if i != winner:
                        print players[i].name,
                        winning_hand.printTsumoKaburi("by dealer","nodealer",self.honba)
        else:
            if agari == 1:
                print players[winner].name,
                winning_hand.printRonAgari("nodealer",self.honba,self.deposits)
                print players[loser].name,
                winning_hand.printHoujuu("to nodealer",self.honba)
            else:
                print players[winner].name,
                winning_hand.printTsumoAgari("nodealer",self.honba,self.deposits)
                for i in range(4):
                    if i != winner:
                        if players[i].isDealer():
                            print players[i].name,
                            winning_hand.printTsumoKaburi("by nodealer","dealer",self.honba)
                        else:
                            print players[i].name,
                            winning_hand.printTsumoKaburi("by nodealer","nodealer",self.honba)
                            
    def ryuukyokuOutput(self,players):
        print "---------- Ryuukyoku ----------"
        for player in players:
            if self.people_in_tenpai == 0 or self.people_in_noten == 0:
                print "%s: %s: + 0 (- %s Deposit)" \
                % (player.name, player.tenpaiDeclaration(), player.riichi*1000)  
            else:
                if player.tenpai:
                    print "%s: %s: + %s (- %s Deposit)" \
                    % (player.name, player.tenpaiDeclaration(), \
                    (3000/self.people_in_tenpai), player.riichi*1000)
                else:
                    print "%s: %s: - %s (- %s Deposit)" \
                    % (player.name, player.tenpaiDeclaration(), \
                    (3000/self.people_in_noten), player.riichi*1000)
        
    def continueGame(self,players):
        for player in players:
            if not player.isPositive():
                print
                print player.name, "Buttobi\n"
                self.continues = False
        if self.kyoku == 4:
            self.nextRound()
            self.resetKyoku()
        if self.round == "West":
            for player in players:
                if player.isOver30():
                    self.continues = False
                    break
                else:
                    self.continues = True
            if self.kyoku == 4:
                self.continues = False
        elif self.round == "South" and self.kyoku == 3 and \
        self.honba >= 1 and players[3].isOver30():
            for player in players:
                if players[3].score >= player.score:
                    agariyame = True
            if agariyame:
                agariyame_confirm = raw_input("Agariyame? Y/N \n")
                if not agariyame_confirm in "Nono":
                    print
                    print "Agariyame \n"
                    self.continues = False
        
class Player(object):
    score = 25000
    def __init__(self,name,seat):
        self.name = name
        self.seat = seat
        self.tenpai = True
        self.riichi = 0
    
    def isPositive(self):
        return self.score >= 0
        
    def isOver30(self):
        return self.score >= 30000
        
    def isDealer(self):
        return self.seat == "East"
        
    def isTenpai(self):
        invalid_input = "Please, select an option from 1 to 3"
        ready_input = False
        while ready_input == False:
            try:
                ready = int(raw_input())
                if ready in range(1,4):
                    ready_input = True
            except ValueError:
                print invalid_input
        if ready == 1:
            self.tenpai = True
            self.riichi = 0
        elif ready == 3:
            self.tenpai = True
            self.riichi = 1
        else:
            self.tenpai = False
            self.riichi = 0
        
    def tenpaiDeclaration(self):
        if self.tenpai:
            return "Tenpai"
        else:
            return "Noten"
        
    def addScore(self,change):
        self.score += change
    
    def takeScore(self,change):
        self.score -= change
        
    def rotateSeat(self):
        if (self.seat == "East"):
            self.seat = "North"
        elif (self.seat == "North"):
            self.seat = "West"
        elif (self.seat == "West"):
            self.seat = "South"
        elif (self.seat == "South"):
            self.seat = "East"
            
    def description(self):
        print "%s Seat: %s: %s Points" \
        % (self.seat, self.name, self.score)
        
class Houra(object):
    def __init__(self,fan,fu):
        self.fan = fan
        self.fu = fu
        
        if (self.fu != 25) and (self.fu % 10 != 0):
            self.fu = int(self.fu + 10) - (self.fu % 10)
            
        self.limit = "%sFan %sFu" % (self.fan, self.fu)
        self.bp = self.fu * (2**(2+self.fan))
        
        if self.bp >= 2000 and self.fan <= 5:
            self.limit = "Mangan Hand"
            self.bp = 2000
        elif self.fan in range(6,8):
            self.limit = "Haneman Hand"
            self.bp = 3000
        elif self.fan in range(8,11):
            self.limit = "Baiman Hand"
            self.bp = 4000
        elif self.fan in range(11,13):
            self.limit = "Sanbaiman Hand"
            self.bp = 6000
        elif self.fan >= 13 and self.fan < 26:
            self.limit = "Yakuman Hand"
            self.bp = 8000
        elif self.fan >= 26 and self.fan < 39:
            self.limit = "Double Yakuman"
            self.bp = 16000
        elif self.fan >= 39 and self.fan < 52:
            self.limit = "Triple Yakuman"
            self.bp = 24000
        elif self.fan >= 52:
            self.limit = "Kasane Yakuman"
            self.bp = 32000
                       
        self.koron = roundValue(self.bp*4)
        self.oyaron = roundValue(self.bp*6)
        self.tsumoA = roundValue(self.bp)
        self.tsumoB = roundValue(self.bp*2)
            
    def ronAgari(self,is_dealer_or_not,honba,deposits):
        bonuses = honba*300 + deposits*1000
        if is_dealer_or_not == "dealer":
            return self.oyaron + bonuses
        else:
            return self.koron + bonuses
                
    def printRonAgari(self,is_dealer_or_not,honba,deposits):
        if is_dealer_or_not == "dealer":
            print "Ron (Dealer): %s: + %s (+%s)" \
            % (self.limit, self.oyaron + honba*300, deposits*1000)
        else:
            print "Ron (No-dealer): %s: + %s (+%s)" \
            % (self.limit, self.koron + honba*300, deposits*1000)
                
    def tsumoAgari(self,is_dealer_or_not,honba,deposits):
        bonuses = honba*300 + deposits*1000
        if is_dealer_or_not == "dealer":
            return self.tsumoB*3 + bonuses
        else:
            return self.tsumoA*2 + self.tsumoB + bonuses 
            
    def printTsumoAgari(self,is_dealer_or_not,honba,deposits):
        if is_dealer_or_not == "dealer":
            print "Tsumo (Dealer): %s: + %s (%s All) (+%s)" \
            % (self.limit, self.tsumoB*3 + honba*300, \
            self.tsumoB + honba*100, deposits*1000)
        else:
            print "Tsumo (No-dealer): %s: + %s (%s/%s) (+%s)" \
            % (self.limit, (self.tsumoA*2 + self.tsumoB) \
            + honba*300, self.tsumoA + honba*100, \
            self.tsumoB + honba*100, deposits*1000)
                
    def houjuu(self,to_dealer_or_not,honba):
        if to_dealer_or_not == "to dealer":
            return self.oyaron + honba*300
        else:
            return self.koron + honba*300
            
    def printHoujuu(self,to_dealer_or_not,honba):
        if to_dealer_or_not == "to dealer":
            print "Houjuu to-Dealer: %s: - %s" \
            % (self.limit, self.oyaron + honba*300)
        else:
            print "Houjuu to-NoDealer: %s: - %s" \
            % (self.limit, self.koron + honba*300)
            
    def tsumoKaburi(self,by_dealer_or_not,is_dealer_or_not,honba):
        if by_dealer_or_not != "by dealer" and is_dealer_or_not != "dealer":
            return self.tsumoA + honba*100
        else:
            return self.tsumoB + honba*100
            
    def printTsumoKaburi(self,by_dealer_or_not,is_dealer_or_not,honba):
        if is_dealer_or_not == "dealer":
            print "Oya Kaburi: %s: - %s" % (self.limit, self.tsumoB + honba*100)
        else:
            if by_dealer_or_not == "by dealer":
                print "Ko Kaburi: %s: - %s" % (self.limit, self.tsumoB + honba*100)
            else:
                print "Ko Kaburi: %s: - %s" % (self.limit, self.tsumoA + honba*100)
