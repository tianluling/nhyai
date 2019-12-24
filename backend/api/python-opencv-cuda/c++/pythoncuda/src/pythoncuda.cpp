/*M///////////////////////////////////////////////////////////////////////////////////////
//
//  IMPORTANT: READ BEFORE DOWNLOADING, COPYING, INSTALLING OR USING.
//
//  By downloading, copying, installing or using the software you agree to this license.
//  If you do not agree to this license, do not download, install,
//  copy or use the software.
//
//
//                          License Agreement
//                For Open Source Computer Vision Library
//
// Copyright (C) 2000-2008, Intel Corporation, all rights reserved.
// Copyright (C) 2009, Willow Garage Inc., all rights reserved.
// Third party copyrights are property of their respective owners.
//
// Redistribution and use in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:
//
//   * Redistribution's of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//   * Redistribution's in binary form must reproduce the above copyright notice,
//     this list of conditions and the following disclaimer in the documentation
//     and/or other materials provided with the distribution.
//
//   * The name of the copyright holders may not be used to endorse or promote products
//     derived from this software without specific prior written permission.
//
// This software is provided by the copyright holders and contributors "as is" and
// any express or implied warranties, including, but not limited to, the implied
// warranties of merchantability and fitness for a particular purpose are disclaimed.
// In no event shall the Intel Corporation or contributors be liable for any direct,
// indirect, incidental, special, exemplary, or consequential damages
// (including, but not limited to, procurement of substitute goods or services;
// loss of use, data, or profits; or business interruption) however caused
// and on any theory of liability, whether in contract, strict liability,
// or tort (including negligence or otherwise) arising in any way out of
// the use of this software, even if advised of the possibility of such damage.
//
//M*/
//################################################################################
//
//                    Created by Neeraj Gulia
//
//################################################################################

#include "precomp.hpp"

namespace cv
{
    namespace pythoncuda
    {

        CV_EXPORTS_W void cpuOpticalFlowFarneback( InputArray prev, InputArray next, InputOutputArray flow,
                                           double pyr_scale, int levels, int winsize,
                                           int iterations, int poly_n, double poly_sigma, int flags )
        {
            cv::calcOpticalFlowFarneback(prev, next, flow, pyr_scale, levels, winsize,
                                        iterations, poly_n, poly_sigma, flags);
        }
        
        CV_EXPORTS_W void gpuOpticalFlowFarneback( InputArray prev, InputArray next, InputOutputArray flow,
                                           double pyr_scale, int levels, int winsize,
                                           int iterations, int poly_n, double poly_sigma, int flags )
        {
            cv::Ptr<cv::cuda::FarnebackOpticalFlow> farn = cv::cuda::FarnebackOpticalFlow::create();
            farn->setPyrScale(pyr_scale);
            farn->setNumLevels(levels);
            farn->setFastPyramids(false);
            farn->setWinSize(winsize);
            farn->setNumIters(iterations);
            farn->setPolyN(poly_n);
            farn->setPolySigma(poly_sigma);
            farn->setFlags(flags);

            cv::cuda::GpuMat d_flow, d_prev, d_next;
            d_prev.upload(prev);
            d_next.upload(next);
            farn->calc(d_prev, d_next, d_flow);
            d_flow.download(flow);
        }
        
        CV_EXPORTS_W void cpuOpticalFlowPyrLK( InputArray prevImg, InputArray nextImg,
                                        InputArray prevPts, InputOutputArray nextPts,
                                        OutputArray status, OutputArray err,
                                        Size winSize = Size(21,21), int maxLevel = 3,
                                        TermCriteria criteria = TermCriteria(TermCriteria::COUNT+TermCriteria::EPS, 30, 0.01),
                                        int flags = 0, double minEigThreshold = 1e-4 )
        {
            cv::calcOpticalFlowPyrLK(prevImg, nextImg, prevPts, nextPts, status, err, 
                                winSize, maxLevel, criteria, flags, minEigThreshold );
        }
        
        CV_EXPORTS_W void gpuOpticalFlowPyrLK( InputArray prevImg, InputArray nextImg,
                                        InputArray prevPts, InputOutputArray nextPts,
                                        OutputArray status, OutputArray err,
                                        Size winSize = Size(21,21), int maxLevel = 3, int iterations = 30)
        {                       
            Ptr<cuda::SparsePyrLKOpticalFlow> d_pyrLK_sparse = cuda::SparsePyrLKOpticalFlow::create(winSize, maxLevel, iterations);
            const cv::cuda::GpuMat d_prevImg(prevImg);
            const cv::cuda::GpuMat d_nextImg(nextImg);
            const cv::cuda::GpuMat d_err;
            const cv::cuda::GpuMat d_pts(prevPts.getMat().reshape(2, 1)); //convert rows to 1
            cv::cuda::GpuMat d_nextPts;
            cv::cuda::GpuMat d_status;
            
            d_pyrLK_sparse->calc(d_prevImg, d_nextImg, d_pts, d_nextPts, d_status, d_err);
            cv::Mat& nextPtsRef = nextPts.getMatRef();
            d_nextPts.download(nextPtsRef);
            nextPtsRef = nextPtsRef.t(); //revert the matrix to its actual shape
            d_status.download(status);
            d_err.download(err);
        }

        CV_EXPORTS_W int cpuFindSimilaritiesBetweenImages( cv::Mat &original, cv::Mat &image_to_compare, float ratio=0.75 )
        {
            auto start_time = std::chrono::high_resolution_clock::now(); 
    
            // Check if 2 images are equals
            Mat original_gray,image_to_compare_gray , dst;
            cv::cvtColor(original, original_gray, cv::COLOR_BGR2GRAY);
            original_gray.convertTo(original_gray, CV_8UC1);
            cv::cvtColor(image_to_compare, image_to_compare_gray, cv::COLOR_BGR2GRAY);
            image_to_compare_gray.convertTo(image_to_compare_gray, CV_8UC1);

            absdiff(original_gray, image_to_compare_gray, dst);
            cv::Scalar s = sum(dst);

            if (s == cv::Scalar::all(0)) {
                std::cout << "The images are completely Equal" << std::endl;
            }else {
                // std::cout << "The images are NOT equal" << endl;
            }

            //提取特征点方法
            double min_hessian = 400;
            cv::Ptr<cv::xfeatures2d::SURF> surf = cv::xfeatures2d::SURF::create(min_hessian);
            
            //特征点
            std::vector<cv::KeyPoint> kp_1, kp_2;

            //特征点匹配
            cv::Mat desc_1, desc_2;
            //提取特征点并计算特征描述子
            surf->detectAndCompute(original_gray, cv::Mat(), kp_1, desc_1);
            surf->detectAndCompute(image_to_compare_gray, cv::Mat(), kp_2, desc_2);

            std::vector<std::vector<cv::DMatch>> matches;

            cv::Ptr<cv::FlannBasedMatcher> matcher = cv::FlannBasedMatcher::create();
            matcher->knnMatch(desc_1, desc_2, matches, 2);

            std::vector<cv::DMatch> goodMatches;
            for (unsigned int i = 0; i < matches.size(); ++i) {
                if (matches[i][0].distance < matches[i][1].distance * ratio)
                    goodMatches.push_back(matches[i][0]);
            }

            auto stop_time = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double, std::milli> fp_ms = stop_time - start_time;
            // std::cout << "Time taken by cpu function: "<< fp_ms.count() << " ms" << endl;

            return goodMatches.size();
        }

        CV_EXPORTS_W int gpuFindSimilaritiesBetweenImages( cv::Mat &original, cv::Mat &image_to_compare, float ratio=0.75 )
        {
            auto start_time = std::chrono::high_resolution_clock::now();
    
            cv::cuda::GpuMat original_gpu, original_gray_gpu, image_to_compare_gpu, image_to_compare_gray_gpu, log;
            original_gpu.upload(original);
            cv::cuda::cvtColor(original_gpu, original_gray_gpu, cv::COLOR_BGR2GRAY);
            original_gray_gpu.convertTo(original_gray_gpu, CV_8UC1);

            image_to_compare_gpu.upload(image_to_compare);
            cv::cuda::cvtColor(image_to_compare_gpu, image_to_compare_gray_gpu, cv::COLOR_BGR2GRAY);
            image_to_compare_gray_gpu.convertTo(image_to_compare_gray_gpu, CV_8UC1);

            // Check if 2 images are equals
            cv::cuda::GpuMat dst;
            cv::cuda::absdiff(original_gpu, image_to_compare_gpu, dst);
            cv::Scalar s = cv::cuda::sum(dst);

            if (s == cv::Scalar::all(0)) {
                std::cout << "The images are completely Equal" << std::endl;
            }else {
                // std::cout << "The images are NOT equal" << endl;
            }

            //提取特征点方法
            std::vector<cv::KeyPoint> cpukp_1, cpukp_2;
            cv::cuda::GpuMat kp_1, kp_2;
            cv::cuda::GpuMat desc_1, desc_2;
            cv::cuda::GpuMat mask_1;
            cv::cuda::GpuMat mask_2;
            cv::cuda::Stream m_stream;
            cv::Ptr< cv::cuda::ORB > orb = cv::cuda::ORB::create(1500);
            cv::Ptr< cv::cuda::DescriptorMatcher > matcher = cv::cuda::DescriptorMatcher::createBFMatcher(cv::NORM_HAMMING);

            orb->detectAndComputeAsync(original_gray_gpu, mask_1, kp_1, desc_1, false, m_stream);
            m_stream.waitForCompletion();
            orb->convert(kp_1, cpukp_1);

            orb->detectAndComputeAsync(image_to_compare_gray_gpu, mask_2, kp_2, desc_2, false, m_stream);
            m_stream.waitForCompletion();
            orb->convert(kp_2, cpukp_2);

            std::vector<cv::DMatch> goodMatches;
            if (desc_2.rows > 0) {
                std::vector<std::vector<cv::DMatch>> cpuKnnMatches;
                cv::cuda::GpuMat gpuKnnMatches;
                matcher -> knnMatchAsync(desc_2, desc_1, gpuKnnMatches, 2, noArray(), m_stream);
                m_stream.waitForCompletion();
                matcher->knnMatchConvert(gpuKnnMatches, cpuKnnMatches); // download matches from gpu and put into vector<vector<DMatch>> form on cpu
                
                for (std::vector<std::vector<cv::DMatch> >::const_iterator it = cpuKnnMatches.begin(); it != cpuKnnMatches.end(); ++it) {
                    if (it->size() > 1 && (*it)[0].distance <  (*it)[1].distance* ratio) {
                        DMatch m = (*it)[0];
                        goodMatches.push_back(m); 
                    }
                }
            }

            auto stop_time = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double, std::milli> fp_ms = stop_time - start_time;
            // std::cout << "Time taken by gpu function: "<< fp_ms.count() << " ms" << endl;

            return goodMatches.size();
        }

        CV_EXPORTS_W void readDirectory(cv::String directory_name, bool useCuda, std::vector<cv::String> check_img_list, float ratio=0.75 )
        {
            auto start_time = std::chrono::high_resolution_clock::now();

            cv::String path(directory_name); //select only jpg
            std::vector<cv::String> fn;
            std::vector<cv::String> filenames;
            std::vector<cv::String> names;
            std::vector<cv::Mat> images;
            cv::glob(path,fn,false);
            size_t count = fn.size();
            // std::vector<cv::String> check_img_list;

            if (count == 0) {
                std::cout << "File " << directory_name << " not exits" << std::endl;
                // return check_img_list;
            }
            
            for (size_t k=0; k<fn.size(); ++k)
            {
                cv::Mat im = cv::imread(fn[k]);
                if (im.empty()) continue;
                images.push_back(im);
                cv::String::size_type iPos = fn[k].find_last_of('/' ) + 1;
                cv::String filename = fn[k].substr(iPos, fn[k].length() - iPos);
                cv::String name = filename.substr(0, filename.rfind("."));
                filenames.push_back(filename);
                names.push_back(name);
            }

            sort(names.begin(), names.end(),[](cv::String a, cv::String b) {return stoi(a) < stoi(b); });

            std::cout << "images length:" << images.size() << std::endl;

            if (images.size() > 1) {
                int good_matcher;
                std::vector<cv::DMatch> goodMatches;
                for (unsigned int i = 0; i < images.size() - 1; ++i) {
                    cv::Mat original = images[i];
                    cv::Mat image_to_compare = images[i+1];
                    if (useCuda == true) {
                        good_matcher = gpuFindSimilaritiesBetweenImages(original, image_to_compare, ratio);
                        // cout << i <<" , good_matcher with gpu:" << good_matcher  << endl;
                        // cout << i <<" , file path:" << names[i]  << ".jpg" << endl;
                    }else {
                        good_matcher = cpuFindSimilaritiesBetweenImages(original, image_to_compare, ratio);
                        // cout << i <<" , good_matcher with cpu:" << good_matcher  << endl;
                        // cout << i <<" , file path:" << names[i]  << ".jpg" << endl;
                    }

                    if (good_matcher<=120) {
                        if (check_img_list.size() == 0){
                            check_img_list.push_back(names[i] + ".jpg");
                            check_img_list.push_back(names[i+1] + ".jpg");
                        } else {
                            check_img_list.push_back(names[i+1]  + ".jpg");
                        }
                    } else {
                        if (check_img_list.size() == 0){
                            check_img_list.push_back(names[i] + ".jpg");
                        }
                    }
                }
                std::cout << "check_img_list length: " << check_img_list.size() << std::endl;

                // for (unsigned int j = 0; j < check_img_list.size() ; ++j) {
                //     cout << check_img_list[j] << endl;
                // }

                auto stop_time = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double, std::milli> fp_ms = stop_time - start_time;
                if (useCuda == true) {
                    std::cout << "Time taken by read_directory gpu function: "<< fp_ms.count() << " ms" << std::endl;
                }else {
                    std::cout << "Time taken by read_directory cpu function: "<< fp_ms.count() << " ms" << std::endl;
                }
                
            }else {
                std::cout << "images length must be more then one!" << std::endl;
            }
        }

    }
}
