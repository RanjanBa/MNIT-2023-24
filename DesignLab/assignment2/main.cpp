#include<iostream>
#include<vector>
#include<string>
//#include "card.h"
#include "get_hand.h"

using namespace std;

void whoIsWinning() {
    vector<Card*> blackCards;  
    int cnt = 5;
    while (cnt--)
    {
        string str;
        cin >> str;
        Card *card = new Card(str[0] - '0', str[1]);
        blackCards.push_back(card);
    }

    vector<Card*> whiteCards;
    cnt = 5;

    while (cnt--)
    {
        string str;
        cin >> str;
        Card *card = new Card(str[0] - '0', str[1]);
        whiteCards.push_back(card);
    }

    Hand h1 = getValue(blackCards);
    cout << h1 << endl;
}

int main() {
    int n;
    cin >> n;
    
    while(n--) {
        whoIsWinning();
    }

    return 0;
}