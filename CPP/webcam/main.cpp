#include <iostream>
#include <string>
#include <sstream>

#include "opencv2/core.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/calib3d.hpp"


using namespace cv;
// Capture the Image from the webcam


int main()
{
    VideoCapture cap(0);
    cap.set(CV_CAP_PROP_AUTO_EXPOSURE,0.75);
    //  cap.set(CV_CAP_PROP_EXPOSURE, 40);
    float k[9] = {550.2499495823959, 0.0, 634.970638005679, 0.0, 548.8753588860187, 381.1055873002101, 0.0, 0.0, 1.0}; 
    float d[4] = {-0.03584706281933589, 0.0077362868057236946,-0.04587986231938219, 0.04834004050933801};
    Mat save_img;
    Mat undistorted;

    cv::Mat K_coef = cv::Mat(3, 3, CV_32F, k);
    cv::Mat D_coef = cv::Mat(1, 4, CV_32F, d);

    cap >> save_img;

    

    char Esc = 0;

    while (Esc != 27 && cap.isOpened()) {        
        bool Frame = cap.read(save_img);        
        if (!Frame || save_img.empty()) {       
            std::cout << "error: frame not read from webcam\n";      
            break;                                              
        }
        // namedWindow("save_img", CV_WINDOW_NORMAL);  
        imshow("imgOriginal", save_img);  
        cv::fisheye::undistortImage(save_img, undistorted, K_coef, D_coef);
        imwrite("test.jpg", undistorted);

        Esc = waitKey(1);
}
// imwrite("test.jpg",save_img); 
}


// int main(int argc, char** argv)
// {

// VideoCapture cap(0);

// // Get the frame
// Mat save_img; 
// for(;;)
// {
// cap >> save_img;

// if(save_img.empty())
// {
//   std::cerr << "Something is wrong with the webcam, could not get frame." << std::endl;
// }
// // Save the frame into a file
// imwrite("test.jpg", save_img); 

// cv::waitKey(1);// A JPG FILE IS BEING SAVED
// }

// }
// int main(int argc, char** argv)
// {
//     std::cout<<CV_VERSION<<std::endl;


//     // Initialize image capture module
//     cv::VideoCapture *cap;
//     cap = new cv::VideoCapture(0);
//     // cap->set(cv::CAP_PROP_AUTO_EXPOSURE, 0.25);

//     // Adjust exposure
//     float exposure;
//     cv::Mat frame;
//     if (true)
//     {
//         exposure = 0.5;
//     }
//     else
//     {
//         exposure = 0.001;
//     }
//     float gain = 1e-4;
//     for(;;)
//     {
//         cap->read(frame);
//         imshow("test", frame);
//         if (frame.empty())
//         {
//             std::cerr << "Blank frame captured!\n";
//             break;
//         }

//         // Set camera exposure
//         // cap->set(cv::CAP_PROP_EXPOSURE, exposure);

//         cv::Scalar img_mean_s = cv::mean(frame);
//         float img_mean = img_mean_s[0];
//         if (img_mean > 128-32 && img_mean < 128+32)
//         {
//             continue;
//         }
//         exposure += gain * (128 - img_mean) * exposure;
//         if (exposure > 0.7)
//         {
//             exposure = 0.7;
//         }
//         else if (exposure <=0.0)
//         {
//             exposure = 1e-6;
//         }
//     }

//     return 0;
// }