from random import shuffle

class Cards:
    def __init__(self):
        self.values = [1,2,3]

class Deck:

    deck = []
    def __init__(self):
        cards = Cards().values
        self.deck = [num for num in cards for _ in range(3)]

    def shuffleCards(self):
        shuffle(self.deck)
        return self.deck
    
    def pop(self,index: int):
        self.deck.pop(index)
    
    def getSize(self):
        return len(self.deck)

class Player:
    def __init__(self, name: str, player_type: str, deck ):
        self.name = name
        self.player_type = player_type
        self.deck = deck
        self.hand = []
    
        if self.player_type.lower() == "ai":
            print("Player " + self.name + " is beep boop")
        elif self.player_type.lower() == "human":
            print("Player " + self.name + " is flesh and bones")
    
    def discard(self,card):
        if card in self.hand:
            self.hand.remove(card)
            print( self.name + " discarded a " + str(card))
            self.draw()
        else:
            print("Illegal Move! You don't have that card")

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
        elif self.hand[0] == self.hand[1] and self.hand[0] == 3:
            return 25
        else: return sum(self.hand)



class Game:
    def __init__(self, player1: Player, player2: Player, deck: Deck):
        self.player1 = player1
        self.player2 = player2
        self.deck = deck
        print("New instance of a game Created. Shuffling deck. Player 1: " + self.player1.name + " VS Player 2: " + self.player2.name )

    def getWinner(self):
        if self.player1.calculateScore() > self.player2.calculateScore():
            print(self.player1.name + " wins with a hand of: " + ', '.join(str(e) for e in self.player1.hand))
        else:
            print(self.player2.name + " wins with a hand of: " + ', '.join(str(e) for e in self.player2.hand))

    



shuffled_deck = Deck().shuffleCards()
print(shuffled_deck)
Idan = Player("Idan", "Human", shuffled_deck)
AI = Player("Blue", "AI",shuffled_deck)

game = Game(Idan, AI, shuffled_deck)

Idan.draw()
print(shuffled_deck)
print("Idan's hand is: " + ', '.join(str(e) for e in Idan.hand))
AI.draw()
print(shuffled_deck)
print("AI's hand is: " + ', '.join(str(e) for e in AI.hand))

Idan.discard(Idan.hand[0])

game.getWinner()


