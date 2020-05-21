# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
            self.startrm = (0,0)
            self.current = (0,0)
            self.last_rm = None
            self.possible_moves = []
            self.step_history = []
            self.rm_history = []
            self.step_to_take = []
            self.escape = False
            self.made_turn = False
            self.got_gold = False
            self.atstart = True
            self.step_count = 1
            self.find_other = False
            self.danger_rm = []
            self.maybe_danger = [] # room may contain pit or wumpus
            self.forsure_danger = []
            self.other_move = []
            self.agentdir = "right"
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
            self.possible_moves = self.check_possible(self.current)
            print("current room: ", self.current)
            print("last room: ", self.last_rm)
            if self.current not in self.rm_history:
                    self.rm_history.append(self.current)
            
            if len(self.step_to_take) != 0:
                    move = self.step_to_take[-1]
                    del self.step_to_take[-1]
                    self.step_history.append(move)
                    return move
            
            if self.escape == True:
                    if self.current == self.startrm:
                            self.atstart = True
                    if self.atstart == True:
                            return Agent.Action.CLIMB
                    else:
                            self.find_other = True
                            self.escape = False
                            self.current = self.last_rm
                            return Agent.Action.FORWARD
    
            if self.find_other == True:
                    print("possible move: ", self.possible_moves)
                    self.find_other = False
                    self.last_rm = self.current
                    self.current = self.possible_moves[0][0]
                    return self.possible_moves[0][1]

            
            if glitter:
                    self.escape = True
                    self.turnback()
                    self.got_gold = True
                    self.atstart = False
                    return Agent.Action.GRAB
            
            if bump:
                    if self.escape == True:
                            return Agent.Action.CLIMB
                    else:
                            self.escape = True
                            self.made_turn = True
                            self.turnback()
                            self.atstart = False
                            self.find_other = True
                            return Agent.Action.TURN_LEFT
        
            if stench:
                    if self.current == self.startrm:
                            return Agent.Action.CLIMB
                    else:
                            self.escape = True
                            self.atstart = False
                            self.made_turn = True
                            self.turnback()
                            self.find_other = True
                            return Agent.Action.TURN_LEFT

            if breeze:
                    if self.current == self.startrm:
                            return Agent.Action.CLIMB
                    else:
                            self.escape = True
                            self.atstart = False
                            self.made_turn = True
                            self.turnback()
                            self.find_other = True
                            return Agent.Action.TURN_LEFT
            
            self.atstart = False
            self.last_rm = self.current
            self.current = self.possible_moves[0][0]
            self.step_count += 1
            self.step_history.append(self.possible_moves[0][1])
            return self.possible_moves[0][1]

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def turnback(self):
            if self.made_turn == True:
                    self.step_to_take.append(Agent.Action.TURN_LEFT)
                    self.made_turn = False
            else:
                    self.step_to_take.append(Agent.Action.TURN_LEFT)
                    self.step_to_take.append(Agent.Action.TURN_LEFT)
   
    def do_opposite(self, act):
            pass

    def check_possible(self, current_move):
            moves = []
            if(self.current[0] + 1, self.current[1]) not in self.rm_history:
                    moves.append(((self.current[0] + 1, self.current[1]), Agent.Action.FORWARD))
            if(self.current[0], self.current[1] + 1) not in self.rm_history:
                    moves.append(((self.current[0], self.current[1] + 1), Agent.Action.TURN_RIGHT))
            if self.atstart != True:
                    if(self.current[0] - 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] - 1, self.current[1]), "back"))
                    if(self.current[0], self.current[1] - 1) not in self.rm_history:
                            moves.append(((self.current[0], self.current[1] - 1), Agent.Action.TURN_LEFT))
            return moves
            """moves = []
            if self.agentdir == "right":
                    if(self.current[0] + 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] + 1, self.current[1]), Agent.Action.FORWARD)) #up/forward
                    if(self.current[0], self.current[1] + 1) not in self.rm_history:
                            moves.append(((self.current[0], self.current[1] + 1), Agent.Action.TURN_LEFT)) #left
                    if(self.current[0] - 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] - 1, self.current[1]), "back")) #down
                    if(self.current[0], self.current[1] - 1) not in self.rm_history:
                            moves.append(((self.current[0], self.current[1] - 1), Agent.Action.TURN_RIGHT)) #right
            elif self.agentdir == "left":
                    if(self.current[0] + 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] + 1, self.current[1]), "back")) #up/forward
                    if(self.current[0], self.current[1] + 1) not in self.rm_history:
                            moves.append(((self.current[0], self.current[1] + 1), Agent.Action.TURN_RIGHT)) #left
                    if(self.current[0] - 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] - 1, self.current[1]), Agent.Action.FORWARD)) #down
                    if(self.current[0], self.current[1] - 1) not in self.rm_history:
                            moves.append(((self.current[0], self.current[1] - 1), Agent.Action.TURN_LEFT)) #right
            elif self.agentdir == "up":
                    if(self.current[0] + 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] + 1, self.current[1]), Agent.Action.TURN_RIGHT)) #up/forward
                    if(self.current[0], self.current[1] + 1) not in self.rm_history:
                            moves.append(((self.current[0], self.current[1] + 1), Agent.Action.FORWARD)) #left
                    if(self.current[0] - 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] - 1, self.current[1]), Agent.Action.TURN_LEFT)) #down
                    if(self.current[0], self.current[1] - 1) not in self.rm_history:
                                moves.append(((self.current[0], self.current[1] - 1), "back")) #right
            else:
                    if(self.current[0] + 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] + 1, self.current[1]), Agent.Action.TURN_LEFT)) #up/forward
                    if(self.current[0], self.current[1] + 1) not in self.rm_history:
                            moves.append(((self.current[0], self.current[1] + 1), "back")) #left
                    if(self.current[0] - 1, self.current[1]) not in self.rm_history:
                            moves.append(((self.current[0] - 1, self.current[1]), Agent.Action.TURN_RIGHT)) #down
                    if(self.current[0], self.current[1] - 1) not in self.rm_history:
                            moves.append(((self.current[0], self.current[1] - 1), Agent.Action.FORWARD)) #right
                                    
            return moves

    def determine_danger(self, current_move, types):
            if self.last_rm != (self.current[0] + 1, self.current[1]):
                    self.maybe_danger.append(((self.current[0] + 1, self.current[1]), types))
            if self.last_rm != (self.current[0] - 1, self.current[1]):
                    self.maybe_danger.append(((self.current[0] - 1, self.current[1]), types))
            if self.last_rm != (self.current[0], self.current[1] + 1):
                    self.maybe_danger.append(((self.current[0], self.current[1] + 1), types))
            if self.last_rm != (self.current[0], self.current[1] - 1):
                    self.maybe_danger.append(((self.current[0], self.current[1] - 1), types))

    def find_optional_move(self):
            a = 0
            for x in self.maybe_danger:
                    sure_danger = 0
                    b = 0
                    for y in self.maybe_danger:
                            if x[0] == y[0]:
                                    if x[1] == y[1]:
                                            sure_danger += 1
                            b += 1
                    if sure_danger >= 2:
                            self.forsure_danger.append((x[0], x[1]))
                    else:
                            for i in self.possible_moves:
                                    if x[0] in i:
                                            self.other_move.append(i)
                    a += 1

    def optional_move(self):
            self.find_optional_move()
            for(int i = 0; i < len(self.possible_moves); i++):
                    if self.possible_moves[i] in self.maybe_danger:
                            del self.possible_moves[i]"""

    def do_sth(self, next_move, direction):
            self.current = next_move
            self.danger = False
            if direction == Agent.Action.FORWARD:
                    return direction
            elif direction == "back":
                    self.escape = True
                    self.made_turn = True
                    self.turnback()
                    self.get_dir(self.agentdir, Agent.Action.TURN_LEFT)
                    return Agent.Action.TURN_LEFT
            else:
                    self.escape = True
                    self.get_dir(self.agentdir, direction)
                    return direction

    def get_dir(self, current_dir, turns):
            direct = ["left", "up", "right", "down"]
            i = direct.index(current_dir)
            if turns == Agent.Action.TURN_LEFT:
                    self.agentdir = direct[i-1];
            if turns == Agent.Action.TURN_RIGHT:
                    if i+1 >= len(direct):
                            self.agentdir = direct[0]
                    else:
                            self.agentdir = direct[i+1]

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
