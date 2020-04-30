from random import shuffle, choice
import itertools

class Cards:
    def __init__(self):
        self.values = [1,2,3]
    
    

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
    
    def getSize(self):
        return len(self.deck)
    def combinations(self):
        return set(list(itertools.combinations(self.deck, 2)))
    def permutations(self):
        return set(list(itertools.permutations(self.deck, 2)))

class Player:
    def __init__(self, name: str ):

        self.name = name
        self.player_type = ""
        self.deck = []
        self.hand = []
    
    ### Discard with the prompt to select the card. Used for human player
    # def discard(self):
    #     card = 0
    #     print(" Which card would you like to discard? " + ', '.join(str(e) for e in self.hand))
    #     card = int(input())
    #     if card in self.hand:
    #         self.hand.remove(card)
    #         print( self.name + " discarded a " + str(card))
    #         self.draw()
    #     else:
    #         print("Illegal Move! You don't have that card")

    def discard(self,card):
        if card in self.hand:
            self.hand.remove(card)
            print( self.name + " discarded a " + str(card))
            self.draw()
        else:
            print("Illegal Move! You don't have that card")

    

    

    def stand(self):
        print("Standing and passing turn!")

    def draw(self):
        i = 0
        while len(self.hand) < 2:
            self.hand.append(self.deck[0])
            self.deck.pop(0)
            i+=1
        print("{} drew {} cards. Current hand is: {} Deck size is now {}. ".format(self.name, i, self.hand, len(self.deck)))
    
    def calculateScore(self):
        if self.hand[0] == self.hand[1] and self.hand[0] == 3:
            return 100
        elif self.hand[0] == self.hand[1] and self.hand[0] == 2:
            return 50
        elif self.hand[0] == self.hand[1] and self.hand[0] == 1:
            return 25
        else: return sum(self.hand)

    def randy(self):
        possible_moves = ["discard", "stand"]
        selected_move = choice(possible_moves)

        if selected_move == "discard":
            self.discard(choice(self.hand))
        elif selected_move == "stand":
            self.stand()
    
    def deepPreschooler(self):
        if self.hand[0] == self.hand[1]:
            self.stand()
        elif 1 in self.hand:
            self.discard(1)
        else:
            self.stand()
    
    def oddBall():
        m = min(self.hand)
        if m & 1:
            self.discard(m)
        else:
            self.stand()
class Probability:
    states = {
        11: 25,
        12: 3,
        13: 4,
        22: 50,
        23: 5,
        33: 100,
    }



class Game:
    def __init__(self, deck: Deck, ai_player, chosen_player):
        self.player1 = ai_player
        self.player2 = chosen_player
        self.deck = deck
        self.winner = ""
        print("New instance of a game Created. Shuffling deck." )
    
    # def setPlayers(self):
    #     players = 0
    #     player = ""
    #     player_type = ""
    #     while players < 2:
    #         player = input("Enter Player " + str(players + 1) + " 's name: ")
    #         player = Player(player)
    #         while(True):
    #             print("What type of player is this? 1.Human     2.AI ")
    #             player_type  = int(input())
    #             if 1 <= player_type <= 2:
    #                 break
    #             else:
    #                 print("That was not a valid option. ")
    #                 continue
    #         players +=1
    #         if players == 1:
    #             self.player1 = player
    #             self.player1.type = player_type
    #         elif players == 2:
    #             self.player2 = player
    #             self.player2.type = player_type
        self.player1.deck = self.deck
        self.player2.deck = self.deck

    def startGame(self):
        self.setPlayers()
        print(self.player1.name)
        print(self.player2.name)
        self.player1.draw()
        print(self.player1.name + "'s hand is: " + ', '.join(str(e) for e in self.player1.hand))
        self.player2.draw()
        print(self.player2.name + "'s hand is: " + ', '.join(str(e) for e in self.player2.hand))
        while self.winner == "":
            self.turn(self.player1)
            self.turn(self.player2)
            self.winner = self.getWinner()

    def turn(self,active_player):
        print("It is " + active_player.name + "'s turn. ")
        print(active_player.name + "'s hand is: " + ', '.join(str(e) for e in active_player.hand))
        print("What will you do? 1.Discard a card   2.Stand ")
        turn_choice = int(input())
        if turn_choice == 1:
            active_player.discard()
        elif turn_choice == 2:
            active_player.stand()
            

    def getWinner(self):
        if self.player1.calculateScore() > self.player2.calculateScore():
            winner = self.player1.name
            print(self.player1.name + " wins with a hand of: " + ', '.join(str(e) for e in self.player1.hand))
        else:
            print(self.player2.name + " wins with a hand of: " + ', '.join(str(e) for e in self.player2.hand))
            winner = self.player2.name
        return winner

            

        



    
r = Player("randy").randy()


# deck = Deck()
# c = deck.combinations()
# print(c)
# shuffled_deck = deck.shuffleCards()


# print(shuffled_deck)

# game_vs_human = Game(shuffled_deck)
# game.startGame()



