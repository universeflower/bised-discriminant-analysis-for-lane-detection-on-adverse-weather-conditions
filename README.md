Biased Discriminant Analysis for Lane Detection in Adverse Weather Conditions
Background
The lane detection technology is crucial for the safe operation of autonomous vehicles. However, it often faces challenges in conditions such as adverse weather or road wear, which significantly affect its reliability. This research aims to address these challenges by proposing a method using Biased Discriminant Analysis (BDA) and a Hat Kernel for lane detection under such adverse conditions.

Problem Statement
Autonomous vehicles rely on lane detection for safe navigation. Unfortunately, environmental factors such as weather conditions (rain, fog, snow) and road surface deterioration can decrease the accuracy of lane detection. Our approach aims to solve this problem by improving the lane detection system's performance under challenging conditions.

Approach
The lane detection pipeline consists of the following steps:

Image Preprocessing and Resizing (640x640): The input image is loaded and resized to 640x640 pixels for consistency and compatibility with the model.

Lane Detection with Yolov5: The Yolov5 model, a CNN-based backbone, is used to detect lanes. It extracts key features in the Neck section, combines multi-scale features, and predicts bounding boxes and classes in the Head section. The model is trained with large datasets and can be fine-tuned for specific projects.

Edge Detection with Hat Kernel: A Hat Kernel is applied to enhance the contour detection by highlighting the edges of lanes. The kernel has structural features, with the middle row set to a positive value (+1) and the last row to a negative value (-1), effectively amplifying road boundary detection.

Pixel Classification Based on Size: The pixels are classified based on their size and the condition:

Pixel > 50: Classified as lane pixels.
Feature Extraction: The pixel values of detected lanes are analyzed to extract features that help distinguish the lanes from the background and other elements.

Lane Mask Enhancement and Noise Removal: The lane mask is further strengthened by reducing noise and improving accuracy.

Final Lane Mask Saving: The enhanced lane mask is saved as the final output.

Methodology
1. Yolov5
Yolov5 uses a CNN-based backbone to extract essential features. It then combines features of different scales at the Neck and makes predictions (bounding boxes and classes) in the Head. By employing Non-Maximum Suppression (NMS), the model removes redundant detections, ensuring a more accurate output. The model can be trained on large datasets and fine-tuned for specific tasks.

2. Hat Kernel
The Hat Kernel is designed with a structural feature where the middle row is set to a positive value (1), and the last row is set to a negative value (-1). This kernel takes advantage of the horizontal characteristics of road boundaries to enhance edge identification, suppressing unnecessary background and elements while accentuating the flat road region.

3. Biased Discriminant Analysis
Biased Discriminant Analysis calculates the average grayscale value around each pixel, extracting it as a feature vector. The covariance matrix for both the target class and non-target class is computed. A bias-weighted decision boundary is then established to separate the target class (lane pixels) from the other classes.

Installation
To get started with the project, you need to have Python 3.8+ and the required dependencies installed.


