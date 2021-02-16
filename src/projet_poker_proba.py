import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

class Card :
    """ Classe représentant les cartes d'un jeu classique de 54 cartes.
    """
    VALUES = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    COLORS = ["\u2665","\u2660","\u2663","\u2666"] # Hearts,Spades,Clubs,Diamonds

    def __init__(self,value,color) :
        self.value=value
        self.color=color

    def __str__(self) :
        """ Fonction pour la représentation graphique """
        return self.VALUES[self.value]+self.COLORS[self.color]

    def get_remaining_cards(used_cards) :
        """ Retourne l'ensemble des cartes sauf celles présentes dans l'ensemble used_cards
        """
        res=[]
        for i in range(0,13) :
            for j in range(0,4) :
                c = Card(i,j)
                if not(c in used_cards) :
                    res.append(Card(i,j))
        return res

    """ Fonctions pour la comparaison des cartes (utilisées dans la gestion des mains)
    """
    def __lt__(self, other)  : # For x < y
        return self.value < other.value or (self.value == other.value and self.color < other.color)
    def __le__(self, other)  : # For x <= y
        return self.value < other.value or (self.value == other.value and self.color <= other.color)
    def __eq__(self, other)  : # For x == y
        return self.value == other.value and self.color == other.color
    def __ne__(self,other) : # For x != y
        return not(self == other)
    def __gt__(self, other)  : # For x > y
        return not(self <= other)
    def __ge__(self, other)  : # For x >= y
        return not(self < other)

class HoleCards :
    """ Classe représentant les 2 cartes du joueur
    """

    def __init__(self,card1,card2) :
        if card1 > card2 :
            self.card1=card1
            self.card2=card2
        else :
            self.card1=card2
            self.card2=card1

    def __str__(self) :
        """ Fonction pour la représentation graphique """
        return "("+str(self.card1)+","+str(self.card2)+")"

class CardValue :
    """ Classe interne pour la comparaison des mains
    """
    def __init__(self,number,value) :
        self.number = number
        self.value = value

    def __lt__(self, other)  : # For x < y
        return self.number < other.number or (self.number == other.number and self.value < other.value)
    def __le__(self, other)  : # For x <= y
        return self.number < other.number or (self.number == other.number and self.value <= other.value)
    def __eq__(self, other)  : # For x == y
        return self.value == other.value and self.number == other.number
    def __ne__(self,other) : # For x != y
        return not(self == other)
    def __gt__(self, other)  : # For x > y
        return not(self <= other)
    def __ge__(self, other)  : # For x >= y
        return not(self < other)

class Hand :
    """ Classe représentant une main (5 cartes)
    """
    def __init__(self,cards) :
        self.cards = cards
        self.cards.sort()

    def is_all_same_color(self) :
        """ Fonction interne """
        c = self.cards[0].color
        for i in range(1,5) :
            if self.cards[i].color != c :
                return False
        return True

    def is_following_values(self) :
        """ Fonction interne """
        ## test if straight with Ace after King
        straight_ace_after_king = self.cards[0].value==0
        for i in range(1,5) :
            if self.cards[i].value != (8+i) :
                straight_ace_after_king = False
                break
        if straight_ace_after_king :
            return True
        ## others cases
        for i in range(1,5) :
            if self.cards[i].value != (self.cards[i-1].value+1) :
                return False
        return True

    def get_cards_values(self) :
        """ Fonction interne """
        values = [0]*14
        res=[]
        for c in self.cards :
            values[(c.value+13)%14]+=1
        for i in range(1,14) :
            if values[i]!=0 :
                res.append(CardValue(values[i],i))
        res.sort(reverse=True)
        return res

    def get_St_value(self) :
        """ Fonction interne """
        if self.cards[0].value == 0 and self.cards[4].value==12 :
            return 13
        else :
            return self.cards[4].value

    def get_hand_value(self) :
        """ Fonction interne """
        if self.is_straight_flush() :
            return (9,self.get_St_value())
        if self.is_four_of_a_kind() :
            return (8,self.get_cards_values())
        if self.is_full_house() :
            return (7,self.get_cards_values())
        if self.is_flush() :
            return (6,self.get_cards_values())
        if self.is_straight() :
            return (5,self.get_cards_values())
        if self.is_three_of_a_kind() :
            return (4,self.get_cards_values())
        if self.is_two_pairs() :
            return (3,self.get_cards_values())
        if self.is_pair() :
            return (2,self.get_cards_values())
        else :
            return (1,self.get_cards_values())

    def is_straight_flush(self) :
        """ teste si la main est une quinte flush """
        return self.is_all_same_color() and self.is_following_values()

    def is_flush(self) :
        """ teste si la main est une couleur """
        return self.is_all_same_color() and not(self.is_following_values())

    def is_straight(self) :
        """ teste si la main est une suite """
        return not(self.is_all_same_color()) and self.is_following_values()

    def is_four_of_a_kind(self) :
        """ teste si la main est un carré """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        for i in values :
            if i==4 :
                return True
        return False

    def is_full_house(self) :
        """ teste si la main est un full """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        pair = False
        three_of_a_kind = False
        for i in values :
            if i==3 :
                three_of_a_kind = True
            if i==2 :
                pair = True
        return pair and three_of_a_kind

    def is_three_of_a_kind(self) :
        """ teste si la main est un brelan """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        three_of_a_kind = False
        for i in values :
            if i==3 :
                three_of_a_kind = True
            if i==2 :
                return False
        return three_of_a_kind

    def is_two_pairs(self) :
        """ teste si la main est deux paires """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        pair = False
        for i in values :
            if i==2 :
                if pair :
                    return True
                else :
                    pair = True
        return False

    def is_pair(self) :
        """ teste si la main est une paire """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        pair = False
        for i in values :
            if i==3 :
                return False
            if i==2 :
                if pair :
                    return False
                else :
                    pair = True
        return pair

    def __str__(self) :
        res = "("+str(self.cards[0])+","+str(self.cards[1])+","+str(self.cards[2])+","
        res+= str(self.cards[3])+","+str(self.cards[4])+")"
        return res

    def __lt__(self,other) :
        """ teste si la main est < other """
        if other == None :
            return False
        a,b = self.get_hand_value()
        aa,bb = other.get_hand_value()
        return a<aa or (a==aa and b < bb)

    def __le__(self,other) :
        """ teste si la main est <= other """
        if other == None :
            return False
        a,b = self.get_hand_value()
        aa,bb = other.get_hand_value()
        return a<aa or (a==aa and b <= bb)

    def __eq__(self,other) :
        """ teste si la main est == other """
        if other == None :
            return False
        a,b = self.get_hand_value()
        aa,bb = other.get_hand_value()
        return a==aa and b == bb

    def __ne__(self,other) :
        """ teste si la main est != other """
        return not(self == other)

    def __gt__(self, other)  :
        """ teste si la main est > other """
        return not(self <= other)

    def __ge__(self, other)  :
        """ teste si la main est >= other """
        return not(self < other)

class GameSituation :
    """ Classe représentant l'état du jeu :
        - hole_cards        : représente les cartes cachées du joueur
        - community_cards   : représente les cartes communes sur la table
    """
    def __init__(self,hole_cards,community_cards) :
        self.hole_cards = hole_cards
        self.community_cards = community_cards

    def get_best_hand(self) :
        """ Fonction retournant la meilleure main possible parmi les 7 cartes : 2 du joueur et 5 communes
            ATTENTION ! : à n'utiliser que s'il y a effectivement 5 cartes communes
        """
        if len(self.community_cards) != 5 :
            raise NameError("get_best_hand")
        cards_set = [self.hole_cards.card1,self.hole_cards.card2]
        cards_set.extend(self.community_cards)
        best_hand = None
        for i in range(0,len(cards_set)-1) :
            for j in range(i+1,len(cards_set)) :
                c_s = cards_set[0:i]
                c_s.extend(cards_set[i+1:j])
                c_s.extend(cards_set[j+1:len(cards_set)])
                h = Hand(c_s)
                if h > best_hand :
                    best_hand = h
        return best_hand

    def get_probabilities_after_river(self) :
        nbJeuxGagnants = 0
        nbJeuxPerdants = 0
        nbJeuxNull = 0

        res = [self.hole_cards.card1, self.hole_cards.card2]
        res.extend(self.community_cards)
        res = Card.get_remaining_cards(res)

        # My Best Hand
        myBestHand = self.get_best_hand()

        # Iterate for all combination
        for i in range(len(res)):
            for j in range(i+1,len(res)):
                # His best hand for this current combination
                hisBestHand = GameSituation(HoleCards(res[i], res[j]), self.community_cards).get_best_hand()

                # We check who won for this current combination
                if myBestHand > hisBestHand:
                    nbJeuxGagnants += 1
                elif myBestHand == hisBestHand:
                    nbJeuxNull += 1
                else:
                    nbJeuxPerdants += 1

        nbJeuxTotal=nbJeuxGagnants+nbJeuxNull+nbJeuxPerdants
        return nbJeuxGagnants/nbJeuxTotal,nbJeuxNull/nbJeuxTotal,nbJeuxPerdants/nbJeuxTotal

    def get_probabilities_after_turn(self) :
        nbJeuxGagnants = 0
        nbJeuxPerdants = 0
        nbJeuxNull = 0

        res = [self.hole_cards.card1, self.hole_cards.card2]
        res.extend(self.community_cards)
        res = Card.get_remaining_cards(res)

        for c in range(len(res)):
            currentCommunityCards = self.community_cards.copy()
            currentCommunityCards.append(res[c])
            myBestHand = GameSituation(self.hole_cards, currentCommunityCards).get_best_hand()
            for i in [x for x in range(len(res)) if x != c]:
                for j in [x for x in range(i+1,len(res)) if x != c]:
                    # His best hand for this current combination
                    hisBestHand = GameSituation(HoleCards(res[i], res[j]), currentCommunityCards).get_best_hand()

                    # We check who won for this current combination
                    if myBestHand > hisBestHand:
                        nbJeuxGagnants += 1
                    elif myBestHand == hisBestHand:
                        nbJeuxNull += 1
                    else:
                        nbJeuxPerdants += 1

        nbJeuxTotal=nbJeuxGagnants+nbJeuxNull+nbJeuxPerdants
        return nbJeuxGagnants/nbJeuxTotal,nbJeuxNull/nbJeuxTotal,nbJeuxPerdants/nbJeuxTotal

    def get_probabilities_after_flop(self) :
        nbJeuxGagnants = 0
        nbJeuxPerdants = 0
        nbJeuxNull = 0

        res = [self.hole_cards.card1, self.hole_cards.card2]
        res.extend(self.community_cards)
        res = Card.get_remaining_cards(res)
        print(len(res))

        for c in range(len(res)):
            for d in range(c,len(res)):
                currentCommunityCards = self.community_cards.copy()
                currentCommunityCards.append(res[c])
                currentCommunityCards.append(res[d])
                myBestHand = GameSituation(self.hole_cards, currentCommunityCards).get_best_hand()

                for i in [x for x in range(len(res)) if x != c and x != d]:
                    for j in [x for x in range(i+1,len(res)) if x != c and x != d]:
                        # His best hand for this current combination
                        hisBestHand = GameSituation(HoleCards(res[i], res[j]), currentCommunityCards).get_best_hand()

                        # We check who won for this current combination
                        if myBestHand > hisBestHand:
                            nbJeuxGagnants += 1
                        elif myBestHand == hisBestHand:
                            nbJeuxNull += 1
                        else:
                            nbJeuxPerdants += 1

        nbJeuxTotal=nbJeuxGagnants+nbJeuxNull+nbJeuxPerdants
        return nbJeuxGagnants/nbJeuxTotal,nbJeuxNull/nbJeuxTotal,nbJeuxPerdants/nbJeuxTotal

    def get_probabilities(self) :
        n = len(self.community_cards)
        if n == 5 :
            return self.get_probabilities_after_river()
        elif n == 4 :
            return self.get_probabilities_after_turn()
        elif n == 3 :
            return self.get_probabilities_after_flop()

    def __str__(self) :
        """ Fonction pour la représentation graphique """
        res = "HC : "+str(self.hole_cards)+" , CC = ("
        for c in self.community_cards :
            res+=str(c)+","
        return res[:-1]+")"

def fonction_principale() :
    h1=Hand([Card(0,1),Card(9,1),Card(10,1),Card(11,1),Card(12,1)])
    h2=Hand([Card(3,2),Card(3,3),Card(3,0),Card(3,1),Card(6,1)])
    h3=Hand([Card(3,2),Card(3,1),Card(3,0),Card(7,1),Card(7,3)])
    h4=Hand([Card(1,2),Card(3,2),Card(8,2),Card(9,2),Card(0,2)])
    h5=Hand([Card(5,2),Card(6,3),Card(7,0),Card(9,1),Card(8,1)])
    h6=Hand([Card(6,2),Card(6,3),Card(6,0),Card(3,1),Card(10,1)])
    h7=Hand([Card(10,2),Card(10,3),Card(12,0),Card(12,1),Card(4,1)])
    h8=Hand([Card(0,2),Card(0,3),Card(2,0),Card(8,1),Card(9,1)])
    h9=Hand([Card(1,2),Card(5,3),Card(6,0),Card(8,1),Card(11,1)])


    hands = [h1,h2,h3,h4,h5,h6,h7,h8,h9]

    print("Est-ce que "+str(h1)+" > "+str(h2)+" : "+str(h1 > h2))
    print("Est-ce que "+str(h3)+" == "+str(h4)+" : "+str(h3 == h4))
    print("Est-ce que "+str(h5)+" >= "+str(h6)+" : "+str(h5 >= h6))
    print("Est-ce que "+str(h7)+" < "+str(h8)+" : "+str(h7 < h8))
    print("Est-ce que "+str(h9)+" != "+str(h1)+" : "+str(h9 != h1))


    h_c = HoleCards(Card(1,0),Card(4,1))
    c_c = [Card(3,3),Card(2,1),Card(5,3),Card(4,2),Card(5,2)]

    gs = GameSituation(h_c,c_c)
    print(gs)

    start_time = time.time()
    print(gs.get_probabilities())
    print("--- %s seconds ---" % (time.time() - start_time))



    print("---------- Tests after river-----------------")

    h_cs = [HoleCards(Card(1,0),Card(4,1)),\
        HoleCards(Card(2,3),Card(5,0)),\
        HoleCards(Card(10,1),Card(10,2)),\
        HoleCards(Card(0,0),Card(12,0)),\
        HoleCards(Card(4,3),Card(4,2)),\
        ]
    c_cs = [[Card(3,3),Card(2,1),Card(5,3),Card(10,2),Card(11,1)],\
        [Card(8,3),Card(10,3),Card(5,1),Card(10,2),Card(11,1)],\
        [Card(11,3),Card(10,3),Card(5,1),Card(10,0),Card(11,1)],\
        [Card(7,3),Card(11,0),Card(8,0),Card(1,0),Card(7,0)],\
        [Card(4,0),Card(10,3),Card(5,1),Card(10,2),Card(11,1)],\
        ]
    res = [(0.9787878787878788, 0.00909090909090909, 0.012121212121212121),\
        (0.5383838383838384, 0.05454545454545454, 0.4070707070707071),\
        (0.998989898989899, 0.0, 0.00101010101010101),\
        (0.9707070707070707, 0.0, 0.029292929292929294),\
        (0.9787878787878788, 0.0, 0.021212121212121213),\
        ]

    for i in range(len(h_cs)) :
        print("---Test n°",i+1,"---")
        gs = GameSituation(h_cs[i],c_cs[i])
        print("|  ",gs)

        start_time = time.time()
        print("|\n|   gs.get_probabilities() :")
        print("|  ",gs.get_probabilities())
        print("|   --- %s seconds ---" % (time.time() - start_time))
        print("|\n|   gs.get_probabilities() doit retourner :")
        print("|  ",res[i])
        print("|   en environ 1s")

    print("---------- Tests after turn (plus longs)-----------------")

    h_cs = [HoleCards(Card(10,0),Card(11,0)),\
        HoleCards(Card(1,0),Card(4,1))]
    c_cs = [[Card(12,0),Card(9,0),Card(5,3),Card(5,2)],\
        [Card(3,3),Card(2,1),Card(5,3),Card(10,2)]]
    res = [(0.5851778656126482, 0.056455862977602106, 0.3583662714097497),\
        (0.9285682916117699, 0.030566534914361003, 0.04086517347386913)]
    for i in range(len(h_cs)) :
        print("---Test n°",i+1,"---")
        gs = GameSituation(h_cs[i],c_cs[i])
        print("|  ",gs)

        start_time = time.time()
        print("|\n|   gs.get_probabilities() :")
        print("|  ",gs.get_probabilities())
        print("|   --- %s seconds ---" % (time.time() - start_time))
        print("|\n|   gs.get_probabilities() doit retourner :")
        print("|  ",res[i])
        print("|   en environ 30s")

if __name__ == "__main__" :
    fonction_principale()
