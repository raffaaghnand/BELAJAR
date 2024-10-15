#include <opencv4/opencv2/opencv.hpp>
#include <iostream>
#include "game.hpp"
#include "permen.hpp"
#include "jaring.hpp"


using namespace cv;
using namespace std;

int main() {
    VideoCapture kamera(0);

    if (!kamera.isOpened()) {
        cerr << "Tidak bisa membuka kamera" << endl;
        return -1;
    }

    Jaring jaring(Scalar(160, 100, 100), Scalar(179, 255, 255)); 
    Game game(jaring);

    game.tambahPermen(Permen(Point(100, 100), 40, Scalar(0, 0, 255))); 
    game.tambahPermen(Permen(Point(200, 200), 40, Scalar(0, 255, 255))); 
    game.tambahPermen(Permen(Point(300, 300), 40, Scalar(0, 255, 0))); 
    game.tambahPermen(Permen(Point(400, 400), 40, Scalar(255, 0, 0))); 
    game.tambahPermen(Permen(Point(100, 100), 40, Scalar(0, 180, 200))); 
    game.tambahPermen(Permen(Point(200, 200), 40, Scalar(255, 180, 0))); 
    game.tambahPermen(Permen(Point(300, 300), 40, Scalar(255, 0, 180))); 
    game.tambahPermen(Permen(Point(400, 400), 40, Scalar(180, 0, 255))); 

    Mat frame, hsv;
    while (true) {
        kamera >> frame;
        if (frame.empty()) break;

        cvtColor(frame, hsv, COLOR_BGR2HSV);
        game.update(frame, hsv);

        imshow("Game Mulyadi by Raffa", frame);

        if (waitKey(30) == 32) {
            break;
        }
    }

    return 0;

} 