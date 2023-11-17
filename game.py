class Game:
    

    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0
        print("Se instancio esta clase")

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]
    
    # Al finalizar el juego, se actualiza el archivo con las nuevas victorias
    # def update_wins(wins):
    #     with open("wins.txt", "w") as file:
    #         file.write(str(wins[0]) + "\n")
    #         file.write(str(wins[1]) + "\n")


    # def load_wins():
    #     try:
    #         with open("wins.txt", "r") as file:
    #             wins_data = file.readlines()
    #             return [int(wins_data[0].strip()), int(wins_data[1].strip())]
    #     except FileNotFoundError:
    #         return [0, 0]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]
        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1
        
        ##self.update_wins()
        return winner

    def getWins(self):
        return self.wins
    
    def updateScore(self,winner):
        if(winner == 0):
            self.wins[0] += 1
        elif(winner == 1):
            self.wins[1] += 1

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False