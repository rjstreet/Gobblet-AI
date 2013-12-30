from easyAI import TwoPlayersGame

class GobbletAI(TwoPlayersGame.TwoPlayersGame):
  """
    Basic data structure for the board is
      13 14 15 16
      9  10 11 12
      5  6  7  8
      1  2  3  4
      
      with each space a list showing [ player_occupying, size ]
      
      The player_pieces array has a running list of the number of pieces in each size for each player

      Moves are structured as [position, piece size]      
  """
  def __init__(self, players):
    self.players = players
    self.nplayer =  1
    self.player_pieces = [ [3,3,3], [3,3,3] ]
    self.board = [[[-1],[-1]] for i in range(16)]

  def possible_moves(self):
    moves = []
    for pp in range(3):
      for bpi, bp in enumerate(self.board):
        if (bp[0][0]==-1 and self.player_pieces[self.nplayer-1][pp] > 0 )or ( self.three_in_a_row(bpi) and bp[1][0] < pp and self.player_pieces[self.nplayer-1][pp] > 0 ):
          moves.append(["off",bpi,pp])

    for mbpi, mbp in enumerate(self.board):
      if mbp[0][0] == self.nplayer:
        for bpi, bp in enumerate(self.board):
          if bpi != mbpi and (bp[0][0]==-1 or bp[1][0] < pp ):
            moves.append(["on",[mbpi,mbp[1][0]],[bpi,mbp[1][0]]])
    return moves
    
  def three_in_a_row(self, bpi):
    row = int(bpi / 4)
    col = bpi % 4
    count = 0
    for i in range(4):
      if self.board[(row*4)+count][0][0] == self.nopponent:
        count = count + 1
    if count > 2:
      return True
    count = 0
    for i in range(4):
      if self.board[col*count][0][0] == self.nopponent:
        count = count + 1
    if count > 2:
      return True
    count = 0
    if bpi in [0,5,10,15]:
      for i in range(4):
        if self.board[i*5][0][0] == self.nopponent:
          count = count + 1
      if count > 2:
        return True
    if bpi in [3,6,9,12]:
      for i in range(4):
        if self.board[(i+1)*3][0][0] == self.nopponent:
          count = count + 1
      if count > 2:
        return True
    return False
    
  def make_move(self, move):
    if move[0] == "off":
      self.board[ move[1] ][0].insert(0,self.nplayer)
      self.board[ move[1] ][1].insert(0, move[2])
      self.player_pieces[self.nplayer-1][ move[2] ] = self.player_pieces[self.nplayer-1][ move[2] ] - 1
    if move[0] == "on":
      self.board[ move[2][0] ][0].insert(0,self.nplayer)
      self.board[ move[2][0] ][1].insert(0, move[1][1])
      self.board[move[1][0]][0].pop(0)
      self.board[move[1][0]][1].pop(0)
      
  def show(self):
    for i in range(4):
      for j in range(4):
        print(self.board[i*4+j][0][0], end=" ")
        print("-", end=" ")
        print(self.board[i*4+j][1][0], end=" ")
        print(" | ", end=" ")
      print()
    print()
    print(self.player_pieces)
                
  def lose(self):
    return any( [all([(self.board[c-1][0][0]== self.nopponent)
                      for c in line])
                      for line in [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15], # horiz.
                                   [0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15], # vertical
                                   [0,5,10,15],[3,6,9,12]]]) # diagonal
                                  
  def is_over(self):
    return (self.possible_moves() == []) or self.lose()

  def scoring(self):
    return -100 if self.lose() else 0
    
if( __name__ == "__main__" ):
  from easyAI import Player
  from easyAI.AI import Negamax
  ai_algo1 = Negamax.Negamax( 1 )
  ai_algo2 = Negamax.Negamax( 3 )
  GobbletAI( [Player.AI_Player(ai_algo1),Player.AI_Player(ai_algo2)] ).play() 
      