import cv2
import numpy as np

# 1. Preprocessing using the provided hat-shaped kernel structure
def preprocess_image(image, a):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Create a hat-shaped kernel: horizontal proportions of a/2a/a and vertical scaling
    kernel_width = 4 * a  # Total width is 4a
    kernel_height = 3  # 3 rows total: one for -1, two for 1
    
    # Initialize kernel with 0s
    kernel = np.zeros((kernel_height, kernel_width), dtype=np.float32)
    
    # Define the -1 region in the first row (width = 4a)
    kernel[0, :] = -1  # Entire first row filled with -1

    # Define the 1 region for the middle 2a width in the second and third rows
    kernel[1:, a:3*a] = 1  # Only the central 2a section filled with 1 in second and third rows

    # Apply convolution with the kernel
    filtered_image = cv2.filter2D(gray, -1, kernel)
    
    # Apply thresholding to enhance the contour lines
    _, contour_image = cv2.threshold(filtered_image, 50, 255, cv2.THRESH_BINARY)
    
    return contour_image

# 2. Apply RANSAC algorithm to fit lines
def ransac_line_detection(image, top, bottom, l, min_inliers=50):
    # Find coordinates of the white pixels (edges)
    points = np.column_stack(np.where(image > 0))
    
    best_line = None
    max_cost = 0
    best_cost = 0

    # RANSAC parameters
    iterations = 1000  # Number of iterations

    for _ in range(iterations):
        # Randomly select one point from the top and one from the bottom line
        if len(points) < 2:
            break
        sample_indices = np.random.choice(points.shape[0], 2, replace=False)
        sample_points = points[sample_indices]
        
        # Get coordinates from sample points
        y_top = sample_points[0][0]  # y-coordinate of the top point
        x_top = sample_points[0][1]  # x-coordinate of the top point
        y_bottom = sample_points[1][0]  # y-coordinate of the bottom point
        x_bottom = sample_points[1][1]  # x-coordinate of the bottom point
        
        # Calculate the slope (m) and intercept (b) of the line
        if x_bottom != x_top:  # Avoid division by zero
            m = (y_bottom - y_top) / (x_bottom - x_top)  # Slope
            b = y_top - m * x_top  # Intercept

            # Calculate cost function
            cost = 0
            for y in range(top, bottom + 1):
                # Calculate x value for given y using line equation: y = mx + b => x = (y - b) / m
                if m != 0:  # Avoid division by zero
                    x = (y - b) / m
                    # Define the width around the line
                    lower_bound = int(x - l / 2)
                    upper_bound = int(x + l / 2)
                    
                    # Sum pixel values in the defined width around the line
                    for x_i in range(lower_bound, upper_bound + 1):
                        if 0 <= x_i < image.shape[1] and 0 <= y < image.shape[0]:
                            cost += image[y, x_i]

            # Update the best line if it has the maximum cost
            if cost > max_cost:
                max_cost = cost
                best_cost = cost
                best_line = (m, b)

    # Filter out lines with cost <= 80% of maximum cost
    if best_line is not None and best_cost > 0.8 * max_cost:
        return best_line
    else:
        return None

# 3. Draw the detected line on the image
def draw_line(image, slope, intercept):
    height, width = image.shape[:2]
    y1 = int(intercept)
    y2 = int(slope * width + intercept)
    
    # Draw the line on the original image
    line_image = np.zeros_like(image)
    cv2.line(line_image, (0, y1), (width, y2), (255, 0, 0), 2)
    return line_image

# Main workflow
if __name__ == '__main__':
    # Load the input video
    input_video_path = "C:\\Users\\User_PC\\Desktop\\video.mp4"  # 비디오 파일 경로
    output_video_path = "C:\\Users\\User_PC\\Desktop\\output_video.avi"  # 출력 비디오 파일 경로
    
    # Video capture and writer setup
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec 설정
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # 원본 비디오 FPS 가져오기
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
    
    # Define parameter 'a' for the kernel size
    a = 10  # Example: a = 10 pixels
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Preprocessing to get contour image
        contour_image = preprocess_image(frame, a)
        
        # Define the top and bottom y-coordinates for lane detection
        top = int(contour_image.shape[0] * 0.1)  # Example top line (10% height)
        bottom = int(contour_image.shape[0] * 0.9)  # Example bottom line (90% height)
        
        # Define the width (l) to consider around the line
        l = 20  # Width around the detected line

        # Apply RANSAC to find the best fitting line
        best_line = ransac_line_detection(contour_image, top, bottom, l)
        
        # If a line was found, draw it
        if best_line is not None:
            slope, intercept = best_line
            line_image = draw_line(frame, slope, intercept)
            
            # Display the original image with the detected line
            cv2.imshow('Detected Line', line_image)
        else:
            print("No line detected")
            line_image = frame  # No line detected, show original frame
        
        # Write the frame to the output video
        out.write(line_image)

        # Display the contour image (optional)
        cv2.imshow('Contour Image', contour_image)
        
        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
