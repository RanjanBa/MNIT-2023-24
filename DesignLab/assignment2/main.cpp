#include <iostream>
#include <vector>
#include <string>
#include <stdlib.h>
#include <algorithm>
#include "get_hand.h"

using namespace std;

void showCards(vector<Card *> &cards)
{
    for (int i = 0; i < cards.size(); i++)
    {
        cout << "(" << cards[i]->value << "," << cards[i]->suit << ")";
        if (i < cards.size() - 1)
        {
            cout << " , ";
        }
    }

    cout << endl;
}

int getCardValue(char ch)
{
    if (ch == 'T')
    {
        return 10;
    }
    else if (ch == 'J')
    {
        return 11;
    }
    else if (ch == 'Q')
    {
        return 12;
    }
    else if (ch == 'K')
    {
        return 13;
    }
    else if (ch == 'A')
    {
        return 1;
    }
    else
    {
        return int(ch - '0');
    }
}

int rankPlayer(vector<Card *> &black_cards, vector<Card *> &white_cards)
{
    vector<int> black_values;

    for (int i = 0; i < black_cards.size(); i++)
    {
        int val = black_cards[i]->value;
        if (black_cards[i]->value == 1)
        {
            val = 14;
        }
        black_values.push_back(val);
    }

    sort(black_values.begin(), black_values.end());

    vector<int> white_values;

    for (int i = 0; i < white_cards.size(); i++)
    {
        int val = white_cards[i]->value;
        if (white_cards[i]->value == 1)
        {
            val = 14;
        }
        white_values.push_back(val);
    }

    sort(white_values.begin(), white_values.end());

    for (int i = black_values.size() - 1; i >= 0; i--)
    {
        if (black_values[i] > white_values[i])
        {
            return 1;
        }
        else if (black_values[i] < white_values[i])
        {
            return -1;
        }
    }

    return 0;
}

void whoIsWinning()
{
    vector<Card *> black_cards;
    int cnt = 5;
    cout << "Black Hand cards : ";
    while (cnt--)
    {
        string str;
        cin >> str;
        cout << str << " ";
        Card *card = new Card(getCardValue(str[0]), str[1]);
        black_cards.push_back(card);
    }
    cout << endl;

    // fflush(stdin);

    vector<Card *> white_cards;
    cnt = 5;
    cout << "White Hand Cards : ";
    while (cnt--)
    {
        string str;
        cin >> str;
        cout << str << " ";
        Card *card = new Card(getCardValue(str[0]), str[1]);
        white_cards.push_back(card);
    }
    cout << endl;

    // fflush(stdin);

    showCards(black_cards);
    showCards(white_cards);

    Hand h1 = getHand(black_cards);
    Hand h2 = getHand(white_cards);

    if (h1 > h2)
    {
        cout << "BLACK WINS.\n";
    }
    else if (h1 < h2)
    {
        cout << "WHITE WINS.\n";
    }
    else
    {
        int rank = rankPlayer(black_cards, white_cards);

        if (rank == 1)
        {
            cout << "BLACK WINS.\n";
        }
        else if (rank == -1)
        {
            cout << "WHITE WINS.\n";
        }
        else
        {
            cout << "TIE.\n";
        }
    }
}

int main()
{
    int n;
    cin >> n;

    while (n--)
    {
        whoIsWinning();
        cout << endl;
    }

    return 0;
}