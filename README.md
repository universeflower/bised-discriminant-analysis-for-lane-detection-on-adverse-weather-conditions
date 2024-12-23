# Biased Discriminant Analysis for Lane Detection in Adverse Weather Conditions

## Background

Lane detection technology is essential for the safe operation of autonomous vehicles. However, it often faces challenges in conditions such as adverse weather or road wear, which significantly affect its reliability. This project aims to solve this problem by proposing a method using **Biased Discriminant Analysis (BDA)** and a **Hat Kernel** for lane detection under adverse conditions.

## Problem Statement

Autonomous vehicles depend on lane detection for safe navigation. Environmental factors, such as weather conditions (rain, fog, snow) and road surface deterioration, can decrease lane detection accuracy. This research proposes a solution to enhance lane detection reliability in such challenging scenarios.

## Approach

The lane detection pipeline consists of the following steps:

1. **Image Preprocessing and Resizing (640x640):**  
   The input image is loaded and resized to 640x640 pixels for consistency with the model input requirements.
   
2. **Lane Detection with Yolov5:**  
   We use the **Yolov5** model, which is based on a CNN backbone to detect lanes. Yolov5 extracts key features in the **Neck** section, combines features of various scales, and predicts bounding boxes and classes in the **Head** section. The model is trained on large datasets and can be fine-tuned for specific applications.

3. **Edge Detection with Hat Kernel:**  
   A **Hat Kernel** is applied to enhance contour detection by highlighting the edges of lanes. The kernel has structural features with the middle row set to a positive value (+1) and the last row to a negative value (-1), effectively amplifying road boundary detection while suppressing unnecessary background.

4. **Pixel Classification Based on Size:**  
   Pixels are classified based on size:
   - **Pixel > 50:** Classified as lane pixels.

5. **Feature Extraction:**  
   Pixel values of detected lanes are analyzed to extract features, helping distinguish lane pixels from other background elements.

6. **Lane Mask Enhancement and Noise Removal:**  
   The lane mask is strengthened by reducing noise and improving accuracy.

7. **Final Lane Mask Saving:**  
   The enhanced lane mask is saved as the final output.

## Methodology

### 1. Yolov5
Yolov5 is a state-of-the-art object detection model that uses a CNN-based backbone to extract features from input images. It combines multi-scale features in the **Neck** and makes predictions (bounding boxes and classes) in the **Head**. Non-Maximum Suppression (NMS) is used to eliminate duplicate detections, improving the model's precision. Yolov5 is trained on large datasets and can be further fine-tuned for specific tasks.

### 2. Hat Kernel
The **Hat Kernel** is designed with a structural feature where the middle row is set to a positive value (1) and the last row to a negative value (-1). This kernel leverages the horizontal properties of road boundaries, enhancing edge identification while suppressing unnecessary elements.

### 3. Biased Discriminant Analysis
**Biased Discriminant Analysis (BDA)** calculates the average grayscale value around each pixel to extract it as a feature vector. A covariance matrix is computed for both the target and non-target classes, and a bias-weighted decision boundary is derived to classify the target class (lane pixels) from other classes.


![image](https://github.com/user-attachments/assets/fdd360d0-9eef-4d26-ad22-613bf5ae6569)

## Installation

To get started with this project, you need Python 3.8+ and the required dependencies installed.

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/Biased Discriminant Analysis for Lane Detection in Adverse Weather Conditions.git
cd Biased Discriminant Analysis for Lane Detection in Adverse Weather Conditions
