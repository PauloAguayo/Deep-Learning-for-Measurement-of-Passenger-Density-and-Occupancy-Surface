# Deep Learning for Measurement of Passenger Density and Occupancy Surface
This work studies the effect of density and occupancy surface with passengers. This is done through Artificial Neural Networks, namely Deep Learning. 
The detection model is Faster RCNN with InceptionV2. This model was trained to detect only human heads.

# Install
Create a virtual environment and install the next libraries:

- Python >=3 
- Tensorflow 1.14
- OpenCV
- Shapely
- xlsxwriter
- scipy.spatial
- numpy
- argparse

# Parser
The program has 9 parser variables, which only 3 are required.

- '-m' (required): path to object detection model.
- '-l' (required): path to labels file.
- '-i' (required): path to optional input image file.
- '-o' (optional): path and name to optional output image file. Default: 'results/output.jpg'.
- '-t' (optional): minimum probability to filter weak detection. Default=0.8.
- '-c' (optional): option for un-distort input image. 'store_true' variable.
- '-r' (optional): resize input image. Default="720,1280". Must follow the same format.
- '-H' (optional): z-coordinate for camera positioning. Default=2.5.
- '-p' (optional): z-coordinate for people high. Default=1.7.
- '-a' (optional): positioning angle in degrees. Default=15.

# Instructions

Step 0 (optional): In the beginning, is highly recommended to apply the un-distort effect (parser variable '-c'). If you do, you'll be directed to the undistorted image with a balance of 1. In case you want to correct this value, you'll be asked. Otherwise, just press 'enter'.

Step 1: The program will ask for the ground truth area (in m2) of interest.

Step 2: Once the image pops up, the coords that defines the geometry of the polygon must be selected. This is done by clicking twice over a pixel and then pressing 'a'. In case you get wrong, press 'r' to delete the selected points. The selected polygon must be a convex one, and the points need to be selected in a linear order. To finish and continue press 'esc'.

Step 3: At this point the program has already detected the heads of passengers. So the next step is focused on the failures. In case that the algorithm hasn't detected a head, it can be donde manually, by clicking a pixel and keeping it pressed until generate a square that select the missed detection. After this, must press 'a'.
In case of wrong detections the procedure is the same, but instead of 'a' press 'z' to remove the detection. The selected square must be intersected with the wrong one in at least 50%. To finish and continue, press 'esc'.

Step 4: The final image is retrieved, and its excel file with values.


# Example
$ python object_detection_image.py -m inference_graph/frozen_inference_graph.pb -l inference_graph/labelmap.pbtxt -i test_1.png -c
