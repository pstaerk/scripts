#include <complex>
#include <fstream>
#include <string>
#include <iostream>
#include <tuple>

const int mandel_iterator(double x, double y, int iterations)
{
    using namespace std::complex_literals;
    std::complex<double> c0 = x + 1i*y;
    std::complex<double> c = 0;
    for (int i = 0; i < iterations; ++i) {
        if (std::abs(c) > 2) {
            return i;
        }
        c = c*c + c0;
    }
    return 0;
}

const void picture_render(const int& px, const int& py, const double& xmin, const double& xmax, const double& ymin, const double& ymax, const int& iterations, const std::string& filename)
{
    int set[px][py];
    double stepx = (xmax - xmin)/px;
    double stepy = (ymax - ymin)/py;
    #pragma omp parallel
    #pragma omp for
    for (int i = 0; i < px; ++i) {
        for (int j = 0; j < py; ++j) {
            set[i][j] = mandel_iterator(xmin + stepx*i, ymin + stepy*j, iterations);
        }
    }

    // Save array to file
    std::ofstream outfile;

    outfile.open(filename, std::ios_base::out);

    #pragma omp parallel
    #pragma omp for ordered
    for (int i = 0; i < px; ++i) {
        for (int j = 0; j < py; ++j) {
            #pragma omp ordered
            outfile << set[i][j] << ';';            
        }
        #pragma omp ordered
        outfile << std::endl;
    }
}

void interpolate_zoom(std::tuple<double, double> xstart, std::tuple<double, double> ystart,
        std::tuple<double, double> xend, std::tuple<double, double> yend, const int& steps)
{
    for (int i = 0; i <= steps; ++i) {
        // Calculate the interpolated coordinates of this run
        // Calculate the set and save it with a marker
    }
}

int main(int argc, char *argv[])
{
    picture_render(2*1000, 2*500, -2.5, 1., -1., 1., 1000, "Myfile2.txt");
    /* std::tuple<double, double> test = std::tuple<double, double>{-1., 1.}; */
    /* interpolate_zoom(std::tuple<double, double>{-2., 2.}); */
    return 0;
}
