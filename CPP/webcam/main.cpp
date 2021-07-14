#include <iostream>
#include <string>
#include <sstream>

#include "opencv2/core.hpp"
#include "opencv2/highgui.hpp"
using namespace cv;

int main(int argc, char** argv)
{
    std::cout<<CV_VERSION<<std::endl;


    // Initialize image capture module
    cv::VideoCapture *cap;
    cap = new cv::VideoCapture(0);
    // cap->set(cv::CAP_PROP_AUTO_EXPOSURE, 0.25);

    // Adjust exposure
    float exposure;
    cv::Mat frame;
    if (true)
    {
        exposure = 0.5;
    }
    else
    {
        exposure = 0.001;
    }
    float gain = 1e-4;
    for(;;)
    {
        cap->read(frame);
        imshow("test", frame);
        if (frame.empty())
        {
            std::cerr << "Blank frame captured!\n";
            break;
        }

        // Set camera exposure
        // cap->set(cv::CAP_PROP_EXPOSURE, exposure);

        cv::Scalar img_mean_s = cv::mean(frame);
        float img_mean = img_mean_s[0];
        if (img_mean > 128-32 && img_mean < 128+32)
        {
            continue;
        }
        exposure += gain * (128 - img_mean) * exposure;
        if (exposure > 0.7)
        {
            exposure = 0.7;
        }
        else if (exposure <=0.0)
        {
            exposure = 1e-6;
        }
    }

    return 0;
}