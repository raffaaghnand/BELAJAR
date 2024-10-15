#ifndef PERMEN_HPP
#define PERMEN_HPP

#include<opencv4/opencv2/opencv.hpp>
using namespace cv;

class Permen {
public:
    Point posisi;
    int radius;
    Scalar warna;
    Point kecepatan;

    Permen(Point posisi, int radius, Scalar warna);
    void gerak(int lebarLayar, int tinggiLayar);
    void gambar(Mat &frame);
};
#endif
