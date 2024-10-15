#include "permen.hpp"

Permen::Permen(Point posisi, int radius, Scalar warna)
    : posisi(posisi), radius(radius), warna(warna), kecepatan(Point(5, 5)) {}

void Permen::gerak(int lebarLayar, int tinggiLayar) {
    posisi += kecepatan;

    if (posisi.x < 0 || posisi.x > lebarLayar) kecepatan.x *= -1;
    if (posisi.y < 0 || posisi.y > tinggiLayar) kecepatan.y *= -1;
}

void Permen::gambar(Mat &frame) {
    circle(frame, posisi, radius, warna, -1);
}
