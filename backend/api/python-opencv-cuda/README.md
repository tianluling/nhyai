# python-opencv-cuda

## Solution
1. Create custom opencv_contrib module
2. Write C++ code to wrap the OpenCV CUDA method
3. Using OpenCV python bindings, expose your custom method
4. Build opencv with opencv_contrib
5. Run python code to test

## Steps to create the build
### Unzip the source: 
1. opencv source code: https://github.com/opencv/opencv/archive/3.4.2.zip
2. opencv_contrib source code: https://github.com/opencv/opencv_contrib/archive/3.4.2.zip

### Create custom module
1.	Copy the folder named "pythoncuda" (inside c++ folder) to: opencv_contrib/modules

### Build opencv using following cmake command
1. create build directory inside the opencv folder, cd to the build directory
2. cmake (I used anaconda3 with environment named as: tensorflow_p36 (with python 3.6))
```
cmake \
-D CMAKE_BUILD_TYPE=RELEASE \
-D WITH_CUDA=ON \
-D CMAKE_INSTALL_PREFIX="/usr/local" \
-D OPENCV_EXTRA_MODULES_PATH="/home/nhydev/github/opencv_contrib/modules" \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D INSTALL_C_EXAMPLES=ON \
-D BUILD_SHARED_LIBS=ON \
-D BUILD_DOCS=OFF \
-D BUILD_TESTS=OFF \
-D BUILD_EXAMPLES=ON \
-D BUILD_PERF_TESTS=OFF \
-D BUILD_opencv_dnn=ON \
-D TINYDNN_USE_NNPACK=ON \
-D TINYDNN_USE_TBB=ON \
-D TINYDNN_USE_OMP=ON \
-D ENABLE_FAST_MATH=ON \
-D WITH_OPENMP=ON \
-D WITH_TBB=ON \
-D WITH_IPP=OFF \
-D MKL_WITH_TBB=ON \
-D MKL_WITH_OPENMP=ON \
-D OPENCV_ENABLE_NONFREE=ON \
-D BUILD_opencv_python2=OFF \
-D OPENCV_GENERATE_PKGCONFIG=YES \
-D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-10.1 \
-D DCMAKE_LIBRARY_PATH=${CUDA_TOOLKIT_ROOT_DIR}/lib64/stubs \
-D CUDA_ARCH_BIN="6.0 6.1 7.0 7.5" \
-D CUDA_ARCH_PTX="" \
-D PYTHON_EXECUTABLE="/home/nhydev/anaconda3/envs/py35/bin/python" \
-D PYTHON_LIBRARY="/home/nhydev/anaconda3/envs/py35/lib/python3.7" \
-D PYTHON3_LIBRARY="/home/nhydev/anaconda3/envs/py35/lib/python3.7" \
-D PYTHON3_EXECUTABLE="/home/nhydev/anaconda3/envs/py35/bin/python" \
-D PYTHON3_INCLUDE_DIR="/home/nhydev/anaconda3/envs/py35/include/python3.7m" \
-D PYTHON3_INCLUDE_DIR2="/home/nhydev/anaconda3/envs/py35/include" \
-D PYTHON3_NUMPY_INCLUDE_DIRS="/home/nhydev/anaconda3/envs/py35/lib/python3.7/site-packages/numpy/core/include" \
-D PYTHON3_INCLUDE_PATH="/home/nhydev/anaconda3/envs/py35/include/python3.7m" \
-D PYTHON3_LIBRARIES="/home/nhydev/anaconda3/envs/py35/lib/libpython3.7m.so" \
..
```
2. ``` make -j$(nproc)```
3. ``` sudo make install ```
4. ``` sudo ldconfig ```

### Test the code
1. Activate conda environment
2. Go to folder: python/ and execute the cpu-opt_flow.py and gpu-opt_flow.py python files
``` 
python cpu-opt_flow.py
python gpu-opt_flow.py 

import cv2
print(cv2.getBuildInformation())
cv2.pythoncuda.readDirectory
cv2.pythoncuda.gpuFindSimilaritiesBetweenImages
cv2.pythoncuda.cpuFindSimilaritiesBetweenImages
```

### Output at my end:
``` total time in optical flow CPU processing: 74.15 sec, for: 794 frames. FPS: 10.71 ```

``` total time in optical flow GPU processing: 21.98 sec, for: 794 frames. FPS: 36.12 ```

### Harware configuration:
* CPU - i7 7th Gen  
* GPU - [NVIDIA TITAN Xp](https://www.nvidia.com/en-us/titan/titan-xp)
* RAM - 32 GB
