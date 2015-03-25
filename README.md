# SkinDetector
This is a high-speed python based skin detection system using OpenCV, it is done using adaptive thresholding, reference papers can be found below. It is designed for processing VGA sized images in real time for the [Gesture Control](https://github.com/WillBrennan/GestureControl) project.


## Quick Start
Getting the app to run is pretty easy. This script will not [install OpenCV](http://docs.opencv.org/doc/tutorials/introduction/linux_install/linux_install.html). However to install the rest of the project dependencies and run the demo script use the following commands.

```bash
# Clone the repo
git clone https://github.com/WillBrennan/SkinDetector && cd SkinDetector
# Install requirements
python setup.py install
# Run the bot
python main.py <directory of images> --display
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
[Skin Segementation Using Multiple Thresholds](http://www.ivl.disco.unimib.it/papers2003/EI06-EI109%20Skin-paper.pdf)


## Demonstration
![Demo on Astronaught](https://raw.githubusercontent.com/WillBrennan/SkinDetector/master/demo.png "Demonstration")

