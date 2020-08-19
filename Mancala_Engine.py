import time
class game:
    def __init__(self, player):
        self.board = [0, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 0]
        #       [N, [A, B, C, D, E, F, G, H, I, J, K, L], M]
        self.initplayer = player
        self.player = 1
        self.moveorder = []
        self.searchedpos = []
        self.movestring = ""
        #self.display()
    def playerswap(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1
    def display(self, board = True):
        """
        [N] L K J I H G []
        [ ] A B C D E F [M]
        """
        if board == True:
            board = self.board
            if self.player != self.initplayer:
                p = 'Your Opponent'
            if self.player == self.initplayer:
                p = 'You'
        else:
            player = board[0]
            if player != self.initplayer:
                p = 'Your Opponent'
            if player == self.initplayer:
                p = 'You'
            board = board[1]
            
        toprow = str(board[1][::-1][0:6])[1:-1]
        botrow = str(board[1][0:6])[1:-1]
        

                
        print("Opponent Score \t= \t" + str(board[0]))
        print("Your Score \t= \t" + str(board[2]) + '\n')
        print("\tL  K  J  I  H  G \t")
        print("[" + str(board[0]) + "]\t" + toprow + "\t[ ]")
        print("[ ]\t" + botrow + "\t[" + str(board[2]) + "]")
        print("\tA  B  C  D  E  F")
        print('\n' + 'Player to move: ' + p)
        print('-------------------------------------------------------------')      
    def check_legal(self, letter):
        letters = {"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,"f": 5,
                   "g": 6,"h": 7,"i": 8,"j": 9,"k": 10,"l": 11}
        
        letter = letter.lower()
        if letter in letters:
            idx = letters[letter]
        else:
            print("Input not recognised")
            return None
        if self.player == 1 and idx in [6, 7, 8, 9, 10, 11]:
            print("Wrong Player")
            return None
        if self.player == 2 and idx in [0, 1, 2, 3, 4, 5]:
            print("Wrong Player")
            return None
        
        return [letter, idx]
    
    def moveadd(self, letter):
        self.movestring += letter
        
    def get_ms(self):
        print(self.movestring)
                        
    def __move(self, let, state):
        player = state[0]
        board = state[1]
        
        pits = board[1]
        
        letters = {"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,"f": 5,
                   "g": 6,"h": 7,"i": 8,"j": 9,"k": 10,"l": 11}
        
        idx = letters[let + player - 1]

        combiboard = pits[6*player-6:6*player] + [board[-2*player+4]] \
                    +pits[-6*player+12:-6*player+18]
                                
        count = combiboard[idx]
        lastpit = (idx + count)%13
        combiboard[idx] = 0
        
        i, j = 0, 0
        
        while j < (count):
            combiboard[idx + i + 1] += 1
            
            i+=1
            if idx + i + 1 == 13:
                i = -1*idx - 1
            j+=1
        
        if lastpit in range(6):
            if combiboard[lastpit] == 1 and combiboard[12-lastpit] != 0:
                combiboard[6] += 1 + combiboard[12-lastpit]
                combiboard[lastpit], combiboard[12-lastpit] = 0, 0
            
        if player == 1:
            board = [board[0], combiboard[0:6] + combiboard[7:13], combiboard[6]]
        
        if player == 2:
            board = [combiboard[6], combiboard[7:13] + combiboard[0:6], board[2]]
            
        if lastpit != 6:
            player = -1*player + 3
    
        return [player, board]
        
    def move(self, let, disp = True):
        if self.check_legal(let) == None:
            return None
        letter, idx = self.check_legal(let)
                    
        pits = self.board[1]
        
        if self.player == 1:
            combiboard = pits[0:6] + [self.board[2]] + pits[6:12]
         
        if self.player == 2:
            combiboard = pits[6:12] + [self.board[0]] + pits[0:6]
            idx -= 6
            
        count = combiboard[idx]
        lastpit = (idx + count)%13
        print(lastpit)
        combiboard[idx] = 0
        
        i = 0
        j = 0
        
        while j < (count):
            combiboard[idx + i + 1] += 1
            
            i+=1
            if idx + i + 1 == 13:
                i = -1*idx - 1
            j+=1
            
        if lastpit in range(6):
            print(combiboard[12-lastpit])
            if combiboard[lastpit] == 1 and combiboard[12-lastpit] != 0:
                combiboard[6] += 1 + combiboard[12-lastpit]
                combiboard[lastpit], combiboard[12-lastpit] = 0, 0
                
        # end of game
        if combiboard[7*self.player-7:7*self.player-1] == [0,0,0,0,0,0]:
            self.board[2*self.player-2]  += sum(combiboard[-7*self.player+14:-7*self.player+20])
            combiboard[-7*self.player+14:-7*self.player+20] = [0,0,0,0,0,0]
        
        if self.player == 1:
            self.board = [self.board[0], combiboard[0:6] + combiboard[7:13], combiboard[6]]
        
        if self.player == 2:
            self.board = [combiboard[6], combiboard[7:13] + combiboard[0:6], self.board[2]]
            
            
        if lastpit != 6:
            self.playerswap()
            
        if disp == True:
            self.display()
            
        self.moveadd(letter)
        
    def calc_score(self, string):
        pass
        # take string
        movelist = [x for x in string]
        # create first move
        player, board = self.__move(movelist[0], [1, [0, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 0]])
        movelist.pop(0)
                
        # iterate
        while len(movelist) > 0:
            player, board = self.__move(movelist[0], [player, board])
            movelist.pop(0)
            
        # return score
        return [board[0], board[2]]
                
    def search2(self, depth, let = None, a = None, b = None, state = None):
        if state == None:
            p = self.player
            pp = (self.player-1)*6
            p2, pits, p1 = self.board
            top_level = True
        else:
            p = state[0]
            pp = (state[0] - 1)* 6
            p2, pits, p1 = state[1]
            top_level = False

        # a will always be maximising score and b will be the minimising score
        if a == None and b == None:
            if p == 2:
                a = p2
                b = p1
            else: 
                a = p1
                b = p2
                
        possmove = ['a','b','c','d','e','f','g','h','i','j','k','l'][0+pp:6+pp]
        
        if top_level: 
            prev_p = None
            pref_let = None
        else: 
            prev_p = p
        # need knowledge of what the previous player is...
        for x in possmove:
            if pits[possmove.index(x)] != 0:
                if prev_p != None and prev_p != p:
                    a, b = b, a
                
                new_p, res = self.__move(x, [p, [p2, pits, p1]])
                pot_a, pot_b = res[-2*p+4], res[2*p-2]
                #print(depth*'\t||', x, a, b, pot_a, pot_b)
                #comparing to THIS PLAYERS a and b
                prev_p = p
                if pot_a >= (a-2) and pot_b <= (b+2) and a <= 25 and b <= 25:
                    a, b = pot_a, pot_b

                    if depth == 1:
                        continue

                    prev_p, a, b = self.search2(depth-1, x,\
                                            (new_p*-1+2)*a + (new_p-1)*b
                                           ,(new_p-1)*a + (new_p*-1+2)*b,
                                           [new_p, res])
                    if top_level:
                        pref_let = x
        if top_level:
            print(pref_let)
        return prev_p, a, b


            
    def clear(self):
        self.searchedpos = []
        
    def search(self, depth, p, alpha, beta):
        #this time just return alpha or beta
        pass

def dogame():
    garry = int(input('Player (1 or 2):'))
    b = game(int(garry))
    
    if garry == 2:
        b.move(input('Enter Opponents first move: '))
        
        while b.player != garry:
            b.move(input('Enter Opponents first move: '))
    b.display()
    b.search2(5)
    mov = input('Your move: ')
    
    while mov != 'end':
        b.move(mov)
        if b.player != garry:
            opmov = input('Opponent move: ')
            b.move(opmov)
        b.search2(4)
        mov = input('Your move: ')
    
    

if __name__ == "__main__":

    #dogame()
    mancala = game(1)
    mancala.move('c')

