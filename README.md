# SkinDetector
============
This is a python based skin detection system using OpenCV, 


## Quick Start
Getting the app to run is pretty easy, just clone the repo, install requirements, and then run! This script
will not install OpenCV, to do that, the following commands must be used, 

```bash
 sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
git clone https://github.com/Itseez/opencv.git
~/opencv
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
make
sudo make install
```

To install the rest of the project dependencies and run 

```bash
# Clone the repo
git clone https://github.com/WillBrennan/SkinDetector && cd SkinDetector
# Install requirements
python setup.py install
# Run the bot
python test_images.py
```
## Usage
Usage of this as  a submodule is simple, just clone into your projects directory (or preferably add as a git submodule), and your ready to go. Below
is an example code usage.

```python
import os
import cv2
import numpy
import SkinDetector

img_path = raw_input("Please Enter Image Path")
assert os.path.exists(img_path), "img_path does not exsist"
image = cv2.imread(img_path)
mask = SkinDetector.process(image)
cv2.imshow("input", image)
cv2.imshow("mask", mask)
cv2.waitKey(0)
```

## References

