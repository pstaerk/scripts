#include <complex>
#include <fstream>
#include <string>
#include <iostream>
#include <tuple>
#include <utility>

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

constexpr std::tuple<double, double> calc_tuple_interpol(std::tuple<double, double> told, std::tuple<double, double> tnew, const double& alpha)
{
    double beta = (1-alpha);
    return std::tuple<double, double>{beta*std::get<0>(told)+alpha*std::get<0>(tnew), beta*std::get<1>(told)+alpha*std::get<1>(tnew)};
}

void interpolate_zoom(const int& px, const int& py, const int& iterations, std::tuple<double, double> xstart, std::tuple<double, double> ystart,
        std::tuple<double, double> xend, std::tuple<double, double> yend, const int& steps)
{
    std::tuple<double, double> xtemp;
    std::tuple<double, double> ytemp;
    double alpha = 0;
    for (int i = 0; i <= steps; ++i) {
        std::cout << "Calculating frame" << i << std::endl;
        // Interpolation factor
        alpha = (double)i / (double)steps;
        // Calculate the interpolated coordinates of this run
        xtemp = calc_tuple_interpol(xstart, xend, alpha);
        ytemp = calc_tuple_interpol(ystart, yend, alpha);

        std::cout << "Current window is x: " << std::get<0>(xtemp) << std::get<1>(xtemp) << std::endl;
        std::cout << "Current window is y: " << std::get<0>(ytemp) << std::get<1>(ytemp) << std::endl;
        
        // Calculate the set and save it with a marker according to the iteration
        picture_render(px, py, std::get<0>(xtemp), std::get<1>(xtemp), std::get<0>(ytemp), 
                std::get<1>(ytemp), iterations, "Render"+std::to_string(i)+".out"); 
    }
}

int main(int argc, char *argv[])
{
    std::cout << "Calculating the frame" << std::endl;
    /* picture_render(2*1000, 2*500, -2.5, 1., -1., 1., 1000, "Myfile2.txt"); */
    /* std::tuple<double, double> test = std::tuple<double, double>{-1., 1.}; */
    std::tuple<double, double> xstart{-2.5, 1};
    std::tuple<double, double> ystart{-1, 1};
    std::tuple<double, double> yend{-.013, .40};
    std::tuple<double, double> xend{-1.165, -.575};

    interpolate_zoom(2*1000, 2*500, 1000, xstart, ystart, xend, yend, 50);
    return 0;
}
