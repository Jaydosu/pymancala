class game:
    def __init__(self, player):
        self.board = [0, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 0]
        #       [N, [A, B, C, D, E, F, G, H, I, J, K, L], M]
        self.initplayer = player
        self.player = 1
        self.moveorder = []
        self.searchedpos = []
        self.movestring = ""

    def playerswap(self):
        self.player = -1*self.player + 3

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
        player, board = state

        pits = board[1]

        letters = {"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,"f": 5,
                   "g": 6,"h": 7,"i": 8,"j": 9,"k": 10,"l": 11}

        idx = letters[let]

        if player == 1:
            combiboard = pits[0:6] + [self.board[2]] + pits[6:12]

        else:
            combiboard = pits[6:12] + [self.board[0]] + pits[0:6]
            idx -= 6

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

        if lastpit in {0,1,2,3,4,5} and combiboard[lastpit] == 1 and combiboard[12-lastpit] != 0:
            combiboard[6] += 1 + combiboard[12-lastpit]
            combiboard[lastpit], combiboard[12-lastpit] = 0, 0

        if player == 1:
            if combiboard[0:6] == [0,0,0,0,0,0]:
                self.board[0] += sum(combiboard[7:13])
                combiboard[7:13] = [0,0,0,0,0,0]
            self.board = [self.board[0], combiboard[0:6] + combiboard[7:13], combiboard[6]]

        else:
            if combiboard[7:13] == [0,0,0,0,0,0]:
                self.board[2] = sum(combiboard[0:6])
                combiboard[0:6] = [0,0,0,0,0,0]
            self.board = [combiboard[6], combiboard[7:13] + combiboard[0:6], self.board[2]]

        if lastpit != 6:
            player = -1*player + 3

        return [player, board]

    def move(self, let, disp = True):
        letter, idx = self.check_legal(let)

        pits = self.board[1]

        if self.player == 1:
            combiboard = pits[0:6] + [self.board[2]] + pits[6:12]

        else:
            combiboard = pits[6:12] + [self.board[0]] + pits[0:6]
            idx -= 6

        count = combiboard[idx]
        lastpit = (idx + count)%13
        combiboard[idx] = 0

        i = 0
        j = 0

        while j < (count):
            combiboard[idx + i + 1] += 1
            i+=1
            if idx + i + 1 == 13:
                i = -1*idx - 1
            j+=1

        if lastpit in {0,1,2,3,4,5} and combiboard[lastpit] == 1 and combiboard[12-lastpit] != 0:
            combiboard[6] += 1 + combiboard[12-lastpit]
            combiboard[lastpit], combiboard[12-lastpit] = 0, 0

        if self.player == 1:
            if combiboard[0:6] == [0,0,0,0,0,0]:
                self.board[0] += sum(combiboard[7:13])
                combiboard[7:13] = [0,0,0,0,0,0]
            self.board = [self.board[0], combiboard[0:6] + combiboard[7:13], combiboard[6]]

        else:
            if combiboard[7:13] == [0,0,0,0,0,0]:
                self.board[2] = sum(combiboard[0:6])
                combiboard[0:6] = [0,0,0,0,0,0]
            self.board = [combiboard[6], combiboard[7:13] + combiboard[0:6], self.board[2]]

        if lastpit != 6:
            self.playerswap()

        if disp == True:
            self.display()

        self.moveadd(letter)
        
    def eval(self, state):
        player, board = state
        pits = board[1] 
        
        # The evaluation function should provide an objective view of game state
        # It should factor in each players score but also the potential score
        
        # Game state should be an estimate of how many moves are left in the game 
        

    def search(self, depth, p, alpha, beta):
        #this time just return alpha or beta
        pass


if __name__ == "__main__":
    import time
    import cProfile
    import timeit
    #dogame()
    #mancala = game(1)
    mancala = game(1)
    c = min(timeit.Timer(v1).repeat(repeat = 100, number = 100000))
    d = min(timeit.Timer(v2).repeat(repeat = 100, number = 100000))

    print(c,d)
