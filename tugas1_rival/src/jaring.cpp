#include "jaring.hpp"

Jaring::Jaring(Scalar warnaDeteksiLow, Scalar warnaDeteksiHigh)
    : warnaDeteksiLow(warnaDeteksiLow), warnaDeteksiHigh(warnaDeteksiHigh), posisi(Point(0, 0)) {}

void Jaring::deteksi(Mat &frame, Mat &hsv) {
    Mat mask;
    inRange(hsv, warnaDeteksiLow, warnaDeteksiHigh, mask);
    Moments m = moments(mask, true);
    if (m.m00 > 0) {
        posisi = Point(m.m10/m.m00, m.m01/m.m00);
    }
}

void Jaring::gambar(Mat &frame) {
    circle(frame, posisi, 50, Scalar(255, 255, 255), 2);
}
