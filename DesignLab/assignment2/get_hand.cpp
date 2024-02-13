#include "get_hand.h"
#include <algorithm>
#include <unordered_map>

bool isConsecutive(vector<int> &values, int start_idx)
{
    for (int i = 0; i < values.size() - 1; i++)
    {
        int idx = (start_idx + i) % values.size();
        int cur = values[idx];
        int next = cur + 1;
        if (cur == 13)
        {
            next = 1;
        }

        if (next != values[(idx + 1) % values.size()])
        {
            return false;
        }
    }

    return true;
}

bool isStraightFlush(vector<Card *> &cards)
{
    for (int i = 1; i < cards.size(); i++)
    {
        if (cards[i - 1]->suit != cards[i]->suit)
        {
            return false;
        }
    }

    vector<int> values;

    for (int i = 0; i < cards.size(); i++)
    {
        values.push_back(cards[i]->value);
    }

    sort(values.begin(), values.end());

    for (int i = 0; i < values.size(); i++)
    {
        if (isConsecutive(values, i))
        {
            return true;
        }
    }

    return false;
}

bool isFourOfAKind(vector<Card *> &cards)
{
    int mx_cnt = 0;

    for (int i = 0; i < cards.size(); i++)
    {
        int val = cards[i]->value;
        int cnt = 0;
        for (int j = 0; j < cards.size(); j++)
        {
            if (cards[j]->value == val)
            {
                cnt++;
            }
        }

        mx_cnt = max(mx_cnt, cnt);
        if (mx_cnt == 4)
        {
            return true;
        }
    }

    return false;
}

bool isFullHouse(vector<Card *> &cards)
{
    int mx_cnt = 0;
    int res_diff = -1;

    for (int i = 0; i < cards.size(); i++)
    {
        int val = cards[i]->value;
        int cnt = 0;
        int diff = -1;
        for (int j = 0; j < cards.size(); j++)
        {
            if (cards[j]->value == val)
            {
                cnt++;
            }
            else
            {
                diff = cards[j]->value;
            }
        }

        mx_cnt = max(mx_cnt, cnt);
        if (mx_cnt == 3 && diff != -1)
        {
            res_diff = diff;
        }
    }

    if (mx_cnt != 3)
    {
        return false;
    }

    int cnt = 0;
    for (int j = 0; j < cards.size(); j++)
    {
        if (cards[j]->value == res_diff)
        {
            cnt++;
        }
    }

    if (cnt == 2)
    {
        return true;
    }

    return false;
}

bool isFlush(vector<Card *> cards)
{
    for (int i = 1; i < cards.size(); i++)
    {
        if (cards[i - 1]->suit != cards[i]->suit)
        {
            return false;
        }
    }

    return true;
}

bool isStraight(vector<Card *> cards)
{
    vector<int> values;

    for (int i = 0; i < cards.size(); i++)
    {
        values.push_back(cards[i]->value);
    }

    sort(values.begin(), values.end());

    for (int i = 0; i < values.size(); i++)
    {
        if (isConsecutive(values, i))
        {
            return true;
        }
    }

    return false;
}

bool isThreeOfAKind(vector<Card *> cards)
{
    int mx_cnt = 0;

    for (int i = 0; i < cards.size(); i++)
    {
        int val = cards[i]->value;
        int cnt = 0;
        for (int j = 0; j < cards.size(); j++)
        {
            if (cards[j]->value == val)
            {
                cnt++;
            }
        }

        mx_cnt = max(mx_cnt, cnt);
    }

    if (mx_cnt != 3)
    {
        return false;
    }

    return true;
}

bool isTwoPairs(vector<Card *> cards)
{
    unordered_map<int, int> mp;

    for (int i = 0; i < cards.size(); i++)
    {
        mp[cards[i]->value]++;
    }

    int no_of_pairs = 0;

    for (auto it : mp)
    {
        if (it.second == 2)
        {
            no_of_pairs++;
        }
    }

    if (no_of_pairs == 2)
    {
        return true;
    }

    return false;
}

bool isPair(vector<Card *> cards)
{
    unordered_map<int, int> mp;

    for (int i = 0; i < cards.size(); i++)
    {
        mp[cards[i]->value]++;
    }

    int no_of_pairs = 0;

    for (auto it : mp)
    {
        if (it.second == 2)
        {
            no_of_pairs++;
        }
    }

    if (no_of_pairs == 1)
    {
        return true;
    }

    return false;
}

enum Hand getHand(vector<Card *> &cards)
{
    if (isStraightFlush(cards))
    {
        cout << "STRAIGHT FLUSH\n";
        return STRAIGHT_FLUSH;
    }
    if (isFourOfAKind(cards))
    {
        cout << "FOUR OF A KIND\n";
        return FOUR_OF_A_KIND;
    }

    if (isFullHouse(cards))
    {
        cout << "FULL HOUSE\n";
        return FULL_HOUSE;
    }

    if (isFlush(cards))
    {
        cout << "FLUSH\n";
        return FLUSH;
    }

    if (isStraight(cards))
    {
        cout << "STRAIGHT\n";
        return STRAIGHT;
    }

    if (isThreeOfAKind(cards))
    {
        cout << "THREE OF A KIND\n";
        return THREE_OF_A_KIND;
    }

    if (isTwoPairs(cards))
    {
        cout << "TWO PAIRS\n";
        return TWO_PAIRS;
    }

    if (isPair(cards))
    {
        cout << "PAIR\n";
        return PAIR;
    }

    cout << "HIGH CARD\n";
    return HIGH_CARD;
}