#include "game.hpp"

Game::Game(Jaring jaring) : jaring(jaring), skor(0) {}

void Game::tambahPermen(Permen permen) {
    permens.push_back(permen);
}

void Game::update(Mat &frame, Mat &hsv) {
    jaring.deteksi(frame, hsv);
    jaring.gambar(frame);

    for (auto &permen : permens) {
        permen.gerak(frame.cols, frame.rows);
        permen.gambar(frame);

        if (norm(permen.posisi - jaring.posisi) < permen.radius + 50) {
            skor++;
            permen.posisi = Point(rand() % frame.cols, rand() % frame.rows); 
        }
    }

    putText(frame, "Score: " + to_string(skor), Point(10, 30), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 0), 2);
}
