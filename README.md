# useful_programs
A compilation of some useful programs for later reference.

These programs are not written for a single cohesive purpose. Most can be run independently of the others. This is simply a repository of useful snippets of code I have written or adapted from other works. I try to give credit to the original authors where applicable.

Feel free to use or adapt as desired. 

## Index:
### 1. [fb_extract.py](fb_extract.py)
Extracts the 'Foreground' and 'Background' from an image into two separate images. While the extract pipeline is rather generic in its approach, I have tailored it specifically to deal with extreme dynamic ranges (black background, high intensity bloom foreground). The target images here were highly reflective spacecraft images. [Original Reference.](https://dahtah.github.io/imager/foreground_background.html)
### 2. [fb_example_extract_all_images.py](fb_example_extract_all_images.py)
Simple example code written for a colleague to use fb_extract.py
### 3. [rosbag_image_extract.py](rosbag_image_extract.py)
Code to extract images from a ros .bag file. [Original Reference.](https://gist.github.com/wngreene/835cda68ddd9c5416defce876a4d7dd9)
