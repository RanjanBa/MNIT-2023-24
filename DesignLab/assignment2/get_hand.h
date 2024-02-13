#include <iostream>
#include <vector>
#include "card.h"

using namespace std;

enum Hand {
    HIGH_CARD,
    PAIR,
    TWO_PAIRS,
    THREE_OF_A_KIND,
    STRAIGHT,
    FLUSH,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    STRAIGHT_FLUSH,
};

Hand getHand(vector<Card*> &);