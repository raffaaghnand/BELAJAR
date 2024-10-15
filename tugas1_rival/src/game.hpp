#ifndef GAME_HPP
#define GAME_HPP

#include "permen.hpp"
#include "jaring.hpp"
#include <vector>
using namespace std;

class Game {
public:
    vector<Permen> permens;
    Jaring jaring;
    int skor;

    Game(Jaring jaring);
    void tambahPermen(Permen permen);
    void update(Mat &frame, Mat &hsv);
};
#endif
