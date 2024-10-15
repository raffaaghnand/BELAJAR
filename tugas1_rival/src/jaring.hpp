#ifndef JARING_HPP
#define JARING_HPP

#include<opencv4/opencv2/opencv.hpp>
using namespace cv;

class Jaring {
public:
    Point posisi;
    Scalar warnaDeteksiLow, warnaDeteksiHigh;

    Jaring(Scalar warnaDeteksiLow, Scalar warnaDeteksiHigh);
    void deteksi(Mat &frame, Mat &hsv);
    void gambar(Mat &frame);
};
#endif
