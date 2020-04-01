import random

class Card():
    '''
    Card class that will define each card in a deck
    '''
    def __init__(self,rank,suite):
        if (rank in ranks) and (suite in suites):
            self.rank=rank
            self.suite=suite
            self.value=cardvalues.get(rank)
        else:
            print('Invalid card')

    def __str__(self):
        return (f'{self.rank} of {self.suite}')

    def get_card_value(self):
        return self.value

class Deck():
    '''
    Deck class that contains all 52 cards
    '''
    def __init__(self):
        print('A new deck is ready for you')
        self.deck=[]
        for suite in suites:
            for rank in ranks:
                self.deck.append(Card(rank,suite))
    
    def __str__(self):
        mydeck=''
        for each_card in self.deck:
            mydeck+=str(each_card)+'\n'
        return mydeck
    
    def shuffle(self):
        print('Shuffling deck now...')
        random.shuffle(self.deck)
        print('Deck has been shuffled!')

    def deal(self):
        return self.deck.pop()
    
    def count_cards(self):
        return len(self.deck)

class Hand():
    '''
    Hand class to store the player hand and also the dealer hand
    '''
    def __init__(self):
        self.cards=[]
        self.value=0
        self.aces=0

    def add_card(self,card):
        self.cards.append(card)
        if (card.get_card_value()==11 and self.value>10):
            self.value+=1
        else:
            self.value+=card.get_card_value()

    def get_hand_value(self):
        return self.value

    def show_some_cards(self):
        myhand=''
        for each_card in self.cards[1:]:
            myhand+=str(each_card)+'\n'
        return myhand

    def __str__(self):
        myhand=''
        for each_card in self.cards:
            myhand+=str(each_card)+'\n'
        return myhand

class Chips():
    '''
    Chips class to store the value of chips that the player has
    '''
    def __init__(self,value=0):
        self.value=value

    def check_value(self):
        return self.value
    
    def win_bet(self,value):
        self.value+=value*2
    
    def lose_bet(self,value):
        self.value-=value


def take_bet(chips):
    global player_bet
    player_bet=0
    bet_taken=False
    while (not bet_taken):
        try:
            player_bet=int(input('How much would you like to bet: '))
            if player_bet > chips.check_value():
                print('You cannot bet more than you have... please try again!')
                bet_taken=False
                continue
        except:
            print('Please enter a valid bet to be placed.')
        else:
            bet_taken=True
            return player_bet

def buy_chips():
    chips_bought=False
    while (not chips_bought):
        try:
            chips_value=int(input('How much ££ would you like to buy chips worth: '))
        except:
            print('Please enter a valid ££ value.')
        else:
            chips_bought=True
            return chips_value

def hit(deck,hand):
    hand.add_card(deck.deal())

def showsomecards(playerhand,dealerhand):
    print('\nPlayer cards are:\n'+playerhand.__str__()+'Total score: '+str(playerhand.get_hand_value()))
    print('\nDealer cards are:\n# CARD FACE DOWN #\n'+dealerhand.show_some_cards())

def showallcards(playerhand,dealerhand):
    print('\nPlayer cards are:\n'+playerhand.__str__()+'Total score: '+str(playerhand.get_hand_value()))
    print('\nDealer cards are:\n'+dealerhand.__str__()+'Total score: '+str(dealerhand.get_hand_value()))

def hit_or_stay():
    try:
        global player_playing
        choice=str(input('Do you want to HIT - h or STAY - s: '))[0].lower()
        if choice=='h':
            player_playing = True
        else:
            player_playing = False
    except:
        print('Please enter valid value')
        hit_or_stay()

def is_busted(hand):
    if hand.get_hand_value() > 21:
        return True
    else:
        return False

def player_busted():
    global dealer_win
    global player_playing
    dealer_win=True
    player_playing=False
    print('Player is busted')

def dealer_busted():
    global player_win
    global dealer_playing
    player_win=True
    dealer_playing=False
    print('Dealer is busted')

def check_winner(playerhand,dealerhand):
    if player_win:
        return 'player'
    elif dealer_win:
        return 'dealer'
    else:
        if playerhand.get_hand_value()>dealerhand.get_hand_value():
            return 'player'
        elif dealerhand.get_hand_value()>playerhand.get_hand_value():
            return 'dealer'
        else:
            return 'tie'

def announcewinner(result,chips,betamount):
    if result=='player' or result=='tie':
        chips.win_bet(betamount)
        print('Congratulations you have won this round!!')
        print(f'You now have {chips.check_value()} chips in your hand!')
    else:
        chips.lose_bet(betamount)
        print('Sorry! the dealer has won this round :(')
        print(f'Your new chips balance is {chips.check_value()}')


def main():
    #Initialise the game by creating a deck, shuffling it, setting up the players and buying chips
    playerchips=Chips(buy_chips())
    replay=True
    global player_win, dealer_win, player_playing, dealer_playing
    while replay:
        deck=Deck()
        deck.shuffle()
        playerhand=Hand()
        dealerhand=Hand()
        player_bet=take_bet(playerchips)
        
        #Set the board up by dealing 2 cards to the player and 1 card to the dealer
        hit(deck,playerhand)
        hit(deck,dealerhand)
        hit(deck,playerhand)
        hit(deck,dealerhand)
        showsomecards(playerhand,dealerhand)

        while player_playing:
            hit_or_stay()
            if player_playing:
                hit(deck,playerhand)
                showsomecards(playerhand,dealerhand)
                if(is_busted(playerhand)):
                    player_busted()
                    break
        

        showallcards(playerhand,dealerhand)
        
        while (not dealer_win) and dealer_playing:
            if dealerhand.get_hand_value()<17:
                dealer_playing=True
                hit(deck,dealerhand)
                showallcards(playerhand,dealerhand)
                if(is_busted(dealerhand)):
                    dealer_busted()
                    break
            else:
                dealer_playing=False
        
        result=check_winner(playerhand,dealerhand)
        announcewinner(result,playerchips,player_bet)

        if (playerchips.check_value()==0):
            print('You are out of chips, please buy some more to play. Thanks for playing with us.')
            break
        play_again=input('Do you want to continue playing: ')
        if play_again[0].lower()=='y':
            replay=True
            player_playing=True
            dealer_playing=True
            player_win=False
            dealer_win=False
        else:
            player_playing=False
            dealer_playing=False
            replay=False

if __name__ == "__main__":
    player_playing=True
    dealer_playing=True
    player_win=False
    dealer_win=False
    suites = ('Hearts','Clubs','Spades','Diamonds')
    ranks = ('Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King')
    cardvalues = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
    playing = True
    main()