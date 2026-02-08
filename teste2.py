from collections import Counter
hand_rankings = {
    "Straight Flush": 9,
    "Four of a Kind": 8,
    "Full Hose": 7,
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
    't':10,
    'j':11,
    'q':12,
    'k':13,
    'a':14
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
            print(sorted_counts)
            if sorted_counts[1][1] >= 2:
                return "Full Hose", [sorted_counts[0][0], sorted_counts[1][0]], [sorted_counts[0][0]]*3+[sorted_counts[1][0]]*2
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
    hand_type, key_card, hand = hand_ranking(counts)
    return hand_type, key_card, hand
playerCards = ['2h', '2c']
tableCards = ['2d', 'ah', '3s', 'qc', 'ad']
print(best_poker_hand(playerCards, tableCards))