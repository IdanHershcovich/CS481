from random import shuffle, choice
import copy
import itertools

#initializing the values of the deck
class Cards:
    def __init__(self):
        self.values = [1,2,3]

#Class responsible for deck creation and shuffling
class Deck:
    deck = []
    def __init__(self):
        self.cards = Cards()
        card_list = self.cards.values
        self.deck = [num for num in card_list for _ in range(3)]

    def shuffleCards(self):
        shuffle(self.deck)
        return self.deck
    
    def pop(self,index: int):
        self.deck.pop(index)

#Player class contains the necessary args to initialize any type of player, 
# has a function for each type of player, and functions related to player actions 
class Player:
    def __init__(self, name: str ):
        self.name = name
        self.player_type = ""
        self.deck = []
        self.prob = Probability(self)
        self.hand = []

    #given a card, discard that card if its hand and draw one more
    def discard(self,card):
        if card in self.hand:
            self.hand.remove(card)
            print( self.name + " discarded a " + str(card))
            self.draw()
        else:
            print("Illegal Move! You don't have that card")

    #Nothing changes. Passes turn
    def stand(self):
        print("Standing and passing turn!")

    #Will draw the amount of cards needed to have a full hand. 
    def draw(self):
        i = 0
        while len(self.hand) < 2:
            self.hand.append(self.deck[0])
            self.deck.pop(0)
            i+=1
        print("{} drew {} cards. Current hand is: {} Deck size is now {}. ".format(self.name, i, self.hand, len(self.deck)))
    
    #used for calculating the winner. Takes the player's hand and returns the rank value
    def calculateScore(self):
        if self.hand[0] == self.hand[1] and self.hand[0] == 3:
            return 100
        elif self.hand[0] == self.hand[1] and self.hand[0] == 2:
            return 50
        elif self.hand[0] == self.hand[1] and self.hand[0] == 1:
            return 25
        else: return sum(self.hand)

    #function for the human player. Will ask the user for input in the form of an int to decide what to do.
    def humanPlayer(self):
        active = True
        while(active):
            print("What will you do? 1.Discard-" + str(self.hand[0]) + "    2.Discard-" + str(self.hand[1]) + "   3. Stand")
            turn_choice = int(input())
            if turn_choice == 1:
                self.discard(self.hand[0])
            elif turn_choice == 2:
                self.discard(self.hand[1])
            elif turn_choice == 3:
                self.stand()
            active = False

    #reinforced learning ai.
    def reinforced(self):
        #current state. Used to calculate v at this state
        v_i = self.hand
        
        #computes the probability of all possible states going from the current state
        p_of_next_state = self.prob.probOfNextState(self.hand)

        #expected value computed with the current hand and all the computed probabilities
        expected_val = self.prob.expectedValue(self.hand,p_of_next_state)
        
        #used to decide what move to take. Expected val can return as an int, the card to be discarded, 
        # or as a string, "stand"
        if isinstance(expected_val,int):
            self.discard(expected_val)
        else: self.stand()
        
        #now that we moved states, we compute the new value function at the new state
        self.prob.update_vi(self.hand, v_i)

    #Random player. will select anything at random
    def randy(self):
        possible_moves = [self.hand[0], self.hand[1], "stand"]
        selected_move = choice(possible_moves)

        #check what to do based on the random choice
        if isinstance(selected_move,int):
            self.discard(selected_move)
        elif selected_move == "stand":
            self.stand()
    
    #edgy thinker. will only discard a 1 and if its not a pair of 1s
    def deepPreschooler(self):
        if self.hand[0] == self.hand[1]:
            self.stand()
        elif 1 in self.hand:
            self.discard(1)
        else:
            self.stand()
    
    #weird guy. Will discard the lowest odd numbered card
    def oddBall(self):
        odds = []
        for m in self.hand:
            if m & 1:
                odds.append(m)
        if odds:
            self.discard(min(odds))
        else: self.stand()

#Class containing everything related to calculations and probabilities
class Probability:
    def __init__(self, player):
        #initial value function
        self.v  = {
            11: 0.5,
            12: 0.5,
            13: 0.5,
            22: 0.5,
            23: 0.5,
            33: 0.5,
        }
        #how often the states happened. Used for next state value calculation. Transition matrix
        self.state_frequency = {
        11: 0,
        12: 0,
        13: 0,
        22: 0,
        23: 0,
        33: 0,
    }
        self.player = player
        #arbitrary LR
        self.learning_rate = 0.1
    
    
    #Computes the prob of every possible state. The transition matrix
    #return value is a nested list. the outer list contains two elements, each one being a list containing the state, 
    #and a dictionary with the transition matrix
    def probOfNextState(self,current_state):
        hand = sorted(current_state)
        state_probs = []
        deck  = Deck().deck
        deck.remove(hand[0])
        deck.remove(hand[1])
        for i in range(len(hand)):
            self.state_frequency = {key : 0 for key in self.state_frequency}
            for j in range(len(deck)):
                h = copy.deepcopy(hand)
                h.pop(i)
                h.append(deck[j])
                h = sorted(h)
                h = int(''.join(str(e) for e in h))
                if  h in self.state_frequency:
                    self.state_frequency[h] += 1/7
            state_probs.append([hand[i], self.state_frequency])
        
        return state_probs  

    #returns the best action to take based on the given transition matrix
    def expectedValue(self,current_state, transition_matrix):
        actions = {}
        state = sorted(current_state)
        state = int(''.join(str(e) for e in state))
        for i in range(len(transition_matrix)):
            #Computing the sum of each state in the transition matrix using dictionaries
            result = {key: transition_matrix[i][1].get(key, 0) * self.v.get(key, 0) for key in set(transition_matrix[i][1]) | set(self.v)}
            actions[transition_matrix[i][0]] = sum(result.values())

        actions["stand"] = 1 * self.v[state]
        return max(actions, key=actions.get)

    #vmax is the move taken and hand is the original hand before making the move
    # v'i = vi + a(vmax - vi)
    def update_vi(self,v_max, hand):
        hand = sorted(hand)
        vmax = sorted(v_max)
        hand = int(''.join(str(e) for e in hand))
        vmax = int(''.join(str(e) for e in vmax))
        v_i = self.v[hand] + self.learning_rate * (self.v[vmax] - self.v[hand])
        self.v[hand] = v_i

        print("Updated V with Vi")
        print(self.v)


    #Used to update the value function depending on if the ai won or lost
    def update_vj(self,hand,game_result):
        hand = sorted(hand)

        hand = int(''.join(str(e) for e in hand))
        
        

        v_j = self.v[hand] + self.learning_rate * (game_result - self.v[hand])
        self.v[hand] = v_j

        print("Updated V with Vj")
        print(self.v)


#Class that creates the game, and has functions related to the game rules
class Game:
    #Initialize the reinforced ai
    def __init__(self):
        self.player1 = Player("Reinforced_AI")
        self.player2 = None
        self.winner = ""
        self.game_count = 0
        print("New instance of a game Created. Shuffling deck." )
        
    #Since player 1 is always the reinforced ai, here we just set its opponent and give each players their decks
    def setPlayers(self, player2):
        deck = Deck().shuffleCards()
        self.player2 = player2
        self.player1.deck = deck
        self.player2.deck = deck

        print(self.player1.name + " VS " + self.player2.name)

    #returns the winner based on the score. No information about ties was given in the HW so not taken into account
    def getWinner(self):
        if self.player1.calculateScore() > self.player2.calculateScore():
            winner = self.player1.name
            print(self.player1.name + " wins with a hand of: " + ', '.join(str(e) for e in self.player1.hand))
            print("\n")
        elif self.player1.calculateScore() < self.player2.calculateScore() :
            print(self.player2.name + " wins with a hand of: " + ', '.join(str(e) for e in self.player2.hand ))
            print("\n")
            winner = self.player2.name
        else: winner = "Tie"
        return winner

    #resets the hands after every game
    def cleanup(self):
        self.player1.hand = []
        self.player2.hand = []

    #Play the game, draw cards, print to the console what is going on. Alternates between reinforced ai and the other player
    def startGame(self):
        if self.game_count & 1:
            self.player1.draw()
            self.player2.draw()
            print(self.player1.name + " is going first")
            self.player1.reinforced()
            print(self.player2.name + "'s turn")
            if self.player2.name == "human":
                self.player2.humanPlayer()
            elif self.player2.name == "randy":
                self.player2.randy()
            elif self.player2.name == "deeppreschooler":
                self.player2.deepPreschooler()
            elif self.player2.name == "oddball":
                self.player2.oddBall()
            self.game_count +=1

            #Same thing but player 2 starts
        else:
            self.player2.draw()
            self.player1.draw()
            
            print(self.player2.name + " is going first")
            if self.player2.name == "human":
                self.player2.humanPlayer()
            elif self.player2.name == "randy":
                self.player2.randy()
            elif self.player2.name == "deeppreschooler":
                self.player2.deepPreschooler()
            elif self.player2.name == "oddball":
                self.player2.oddBall()
            print(self.player1.name + "'s turn")
            self.player1.reinforced()
            self.game_count+=1

        #determine winner
        self.winner = self.getWinner()

        #update Vj based on the results
        if self.winner == "Reinforced_AI":
            self.player1.prob.update_vj(self.player1.hand,1)
        elif self.winner == "Tie":
            self.player1.prob.update_vj(self.player1.hand,0.25)
        else: self.player1.prob.update_vj(self.player1.hand, -1)

        self.cleanup()
            

    

                



g = Game()
i = 0
while i < 100:
    print("\n Run " + str(i) + "\n" )
    # if i < 50:
    #     g.setPlayers(Player("human"))
    #     g.startGame()
    g.setPlayers(Player("randy"))
    g.startGame()
    g.setPlayers(Player("deeppreschooler"))
    g.startGame()
    g.setPlayers(Player("oddball"))
    g.startGame()
    i+=1

#Since no termination criteria was given, I'm running 100 trials. 

