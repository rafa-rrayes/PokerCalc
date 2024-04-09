from collections import Counter
import random

# Define hand rankings for comparison
hand_rankings = {
    "Straight Flush": 9,
    "Four of a Kind": 8,
    "Full House": 7,
    "Flush": 6,
    "Straight": 5,
    "Three of a Kind": 4,
    "Two Pair": 3,
    "One Pair": 2,
    "High Card": 1
}
card_ranking ={
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    'T':10,
    'J':11,
    'Q':12,
    'K':13,
    'A':14
}

def best_poker_hand(cardsPlayer, cardsTable):
    cards = cardsPlayer+cardsTable
    # Helper functions
    def is_flush(suits):
        suit_counts = Counter(suits)
        # Find all suits in the hand with 5 or more cards
        flush_suits = [suit for suit, count in suit_counts.items() if count >= 5]
        if flush_suits:
            listCard = [card_ranking[card[0]] for card in cards if card[1] == flush_suits[0]]
            listCard = sorted(listCard, reverse=True)

            if is_straight(listCard)[0]:
                return "Straight", is_straight(listCard)[1]
            return True, listCard
        return False, None
    
    def is_straight(hand):
        # Include Ace as both 14 and 1 if present
        all_values = set(hand)
        if 14 in all_values:
            all_values.add(1)
        
        # Sort the values in reverse
        sorted_values = sorted(all_values, reverse=True)
        
        # Check for straight sequences
        sequence = [sorted_values[0]]
        for value in sorted_values[1:]:
            if value == sequence[-1] - 1:
                sequence.append(value)
                if len(sequence) == 5:
                    return True, sequence  # Found a straight
            else:
                if len(sequence) >= 5:
                    break  # If we already have a straight, no need to continue
                sequence = [value]  # Start a new sequence

        if len(sequence) == 4 and sequence[-1] == 2 and 14 in hand:
            # Special case for Ace through 5 straight
            return True, [5, 4, 3, 2, 1]  # Representing Ace as 1 for the output

        return False, None  # No straight found
    def hand_ranking(counts):
        sorted_counts = counts.most_common()
        listCard = [card_ranking[card[0]] for card in cardsPlayer+cardsTable]
        listCard = sorted(listCard, reverse=True)
        allCards = sorted([card_ranking[i[0]] for i in cardsPlayer+cardsTable], reverse=True)
        if sorted_counts[0][1] == 4:
            for i in range(4):
                allCards.remove(sorted_counts[0][0])
            return "Four of a Kind", [sorted_counts[0][0]], [sorted_counts[0][0]]*4 + [allCards[0]]
        elif sorted_counts[0][1] == 3:
            if sorted_counts[1][1] == 2:
                return "Full House", [sorted_counts[0][0], sorted_counts[1][0]], [sorted_counts[0][0]]*3+[sorted_counts[1][0]]*2
            for i in range(3): allCards.remove(sorted_counts[0][0])
            return "Three of a Kind", sorted_counts[0][0], allCards[0:2]+[sorted_counts[0][0]]*3
        elif sorted_counts[0][1] == 2:
            allCards.remove(sorted_counts[0][0])
            allCards.remove(sorted_counts[0][0])
            if sorted_counts[1][1] == 2:
                allCards.remove(sorted_counts[1][0])
                allCards.remove(sorted_counts[1][0])
                if sorted_counts[0][0]> sorted_counts[1][0]:
                    return "Two Pair", [sorted_counts[0][0], sorted_counts[1][0]], [allCards[0]]+[sorted_counts[0][0], sorted_counts[1][0]]*2
                
                return "Two Pair", [sorted_counts[1][0], sorted_counts[0][0]], [allCards[0]]+[sorted_counts[0][0], sorted_counts[1][0]]*2
            return "One Pair", sorted_counts[0][0], allCards[0:3]+[sorted_counts[0][0]]*2
        else:
            return "High Card", listCard[0], allCards[0:5]
        
    # Identify flush
    has_straight, straight_high = is_straight([card_ranking[card[0]] for card in cards])
    suits = [i[1] for i in cards]
    has_flush, flush_high = is_flush(suits)
    if has_flush == "Straight":
        return "Straight Flush", flush_high, flush_high
    if has_flush:
        return "Flush", flush_high, flush_high
    if has_straight:
        return "Straight", straight_high, straight_high
    # Identify straight
    
    # Count occurrences of each card value
    
    counts = Counter(sorted([card_ranking[card[0]] for card in cards], reverse=True))
    
    
    # Other hand types
    
    hand_type, key_card, hand = hand_ranking(counts)
    return hand_type, key_card, hand

def whoWins(player, oponent, community_cards):
    global p1, p2, p3, p4, p5, p6, p7, p8, p9, p10
    player = best_poker_hand(player, community_cards)
    oponent = best_poker_hand(oponent, community_cards)
    PlPoints = hand_rankings[player[0]]
    OpPoints = hand_rankings[oponent[0]]
    
    if PlPoints < OpPoints:
        return "Lost"
    elif PlPoints > OpPoints:
        return "Won"
    elif PlPoints == OpPoints:
        if player[0] == "Four of a Kind":
            if player[1] < oponent[1]:
                return "Lost"
            elif player[1] > oponent[1]:
                return "Won"
            else:
                res = highCard(player[2], oponent[2])
                return res
        elif player[0] == "High Card":
            if player[1] < oponent[1]:
                return "Lost"
            elif player[1] > oponent[1]:
                return "Won"
            else:
                return highCard(player[2], oponent[2])
        elif player[0] == "One Pair":
            if player[1] < oponent[1]:
                return "Lost"
            elif player[1] > oponent[1]:
                return "Won"
            else:
                return highCard(player[2], oponent[2])
        elif player[0] == "Three of a Kind":
            if player[1] < oponent[1]:
                return "Lost"
            elif player[1] > oponent[1]:
                
                return "Won"
            else:
                res = highCard(player[2], oponent[2])
                return res
        elif player[0] == "Full House":
            if player[1][0] < oponent[1][0]:
                return "Lost"
            elif player[1][0] > oponent[1][0]:
                return "Won"
            else:
                if player[1][1] < oponent[1][1]:
                    return "Lost"
                elif player[1][1] > oponent[1][1]:
                    return "Won"
                else:
                    return "Draw"
        elif player[0] == "Two Pair":
            
            if player[1][0] < oponent[1][0]:
                return "Lost"
            elif player[1][0] > oponent[1][0]:
                return "Won"
            else:
                if player[1][1] < oponent[1][1]:
                    return "Lost"
                elif player[1][1] > oponent[1][1]:
                    return "Won"
                else:
                    return highCard(player[2], oponent[2])
        elif player[0] == "Flush":
            res = highCard(player[1], oponent[1])
            return res
        elif player[0] == "Straight":
            res = highCard(player[1], oponent[1])
            return res
    return "Won"

def simulate_poker_game(player_hand, community_cards, num_players):
    player_hand = player_hand.copy()
    community_cards = community_cards.copy()
    suits = 'CHSD'  # Clubs, Hearts, Spades, Diamonds
    ranks = '23456789TJQKA'
    deck = [r + s for s in suits for r in ranks]
    for card in player_hand + community_cards:
        deck.remove(card)
    while len(player_hand) < 2:
        carta = random.choice(deck)
        player_hand.append(carta)
        deck.remove(carta)
    # Complete the community cards
    while len(community_cards) < 5:
        carta = random.choice(deck)
        community_cards.append(carta)
        deck.remove(carta)


    other_players_hands = []
    for _ in range(num_players - 1):
        newplayer_hand = []
        newplayer_hand.append(random.choice(deck))
        deck.remove(newplayer_hand[0])
        newplayer_hand.append(random.choice(deck))
        deck.remove(newplayer_hand[1])
        other_players_hands.append(newplayer_hand)
    
    bestHand = best_poker_hand(player_hand, community_cards)
    # Determine the best hand for each other player and compare
    draw = False
    for hand in other_players_hands:
        playerStat = whoWins(player_hand, hand, community_cards)
        if playerStat == "Lost":
            return ["Lost", bestHand]
        elif playerStat == "Draw":
            draw = True
    if draw:
        return ["Draw" , bestHand]
    return ["Won", bestHand]
def highCard(hand1, hand2):
    hand1 = sorted(hand1, reverse=True)
    hand2 = sorted(hand2, reverse=True)
    for i, card in enumerate(hand1):
        if i == 5:
            break
        if card > hand2[i]:
            return "Won"
        elif card < hand2[i]:
            return "Lost"
    return "Draw"


def calculateProb(player_hand, community_cards, num_players, numsimulations):
    amountWon = 0
    amountLost = 0
    amountDraw = 0
    outs = {
        'High Card': 0,
        'One Pair': 0,
        'Two Pair': 0,
        'Three of a Kind': 0,
        'Straight': 0,
        'Flush': 0,
        'Full House': 0,
        'Four of a Kind': 0,
        'Straight Flush': 0
    }
    for i in range(numsimulations):
        community = community_cards.copy()
        player_won, bestHand = simulate_poker_game(player_hand, community, num_players)

        if player_won == "Won":
            amountWon += 1
        elif player_won == "Lost":
            amountLost += 1
        else:
            amountDraw += 1
        outs[bestHand[0]] += 100/(numsimulations)
    
    return [round(amountWon/numsimulations*100, 2) ,  round(amountDraw/numsimulations*100, 2), round(amountLost/numsimulations*100, 2)/(num_players-1), outs]

if __name__ =='__main__':
    player_hand_example = ['AH', 'AC']
    community_cards_example =[]
    num_players_example = 4
    prob = calculateProb(player_hand_example, community_cards_example, num_players_example, 10000)
    print(prob)
