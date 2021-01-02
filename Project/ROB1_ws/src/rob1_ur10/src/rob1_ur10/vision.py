#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math
from cv_bridge import CvBridge, CvBridgeError

cvb = CvBridge()

def numpy_to_msg(img):
    """Builds a Image message from a NumPy array.
    Args:
        img (np.array): A NumPy array containing the RGB image data.
    Returns:
        A sensor_msgs/Image containing the image data.
    """
    return cvb.cv2_to_imgmsg(img, "bgr8")



# --- Select HSV color ranges ---
def hsv_threshold(image,box_color):

    # Blue color range
    if box_color == "blue":
        # Set minimum and maximum HSV values to display
        hMin = 85
        sMin = 139
        vMin = 0
        lower = np.array([hMin, sMin, vMin])

        hMax = 135
        sMax = 255
        vMax = 255
        upper = np.array([hMax, sMax, vMax])

        # Convert Image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv)

        # plt.imshow(h,cmap='gray', vmin=0, vmax=255)
        # plt.xlabel('Pixels')
        # plt.ylabel('Pixels')
        # #plt.title('Hue')
        # plt.show()
        #
        # plt.imshow(s,cmap='gray', vmin=0, vmax=255)
        # plt.xlabel('Pixels')
        # plt.ylabel('Pixels')
        # #plt.title('Saturation')
        # plt.show()
        #
        # plt.imshow(v,cmap='gray', vmin=0, vmax=255)
        # plt.xlabel('Pixels')
        # plt.ylabel('Pixels')
        # #plt.title('Value')
        # plt.show()

        mask = cv2.inRange(hsv, lower, upper) # HSV threshold blue range
        result = cv2.bitwise_and(image, image, mask=mask) # Apply threshold to original image


#       plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
#       plt.xlabel('Pixels')
#       plt.ylabel('Pixels')
#       plt.title('HSV Blue Range')
#       plt.show()
        return result

    # Red color range
    if box_color == "red":
        # 1st half
        hMin1 = 150
        sMin1 = 0
        vMin1 = 50 #0
        lower1 = np.array([hMin1, sMin1, vMin1])

        hMax1 = 179
        sMax1 = 255
        vMax1 = 255
        upper1 = np.array([hMax1, sMax1, vMax1])

        # 2nd half
        hMin2 = 0
        sMin2 = 0
        vMin2 = 50 #
        lower2 = np.array([hMin2, sMin2, vMin2])

        hMax2 = 10
        sMax2 = 255
        vMax2 = 255
        upper2 = np.array([hMax2, sMax2, vMax2])

        # Convert to HSV colorspace
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.max(mask1, mask2)

#        result1 = cv2.bitwise_and(image, image, mask=mask1) #
#        result2 = cv2.bitwise_and(image, image, mask=mask2) #

        result = cv2.bitwise_and(image, image, mask=mask)

#        plt.imshow(cv2.cvtColor(result1, cv2.COLOR_BGR2RGB))
#        plt.xlabel('Pixels')
#        plt.ylabel('Pixels')
#        plt.title('HSV Red Range 1')
#        plt.show()

#        plt.imshow(cv2.cvtColor(result2, cv2.COLOR_BGR2RGB))
#        plt.xlabel('Pixels')
#        plt.ylabel('Pixels')
#        plt.title('HSV Red Range 2')
#        plt.show()

#        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
#        plt.xlabel('Pixels')
#        plt.ylabel('Pixels')
#        plt.title('HSV Red Range')
#        plt.show()

        return result

# --- Extract Box Contours from Raw Image ---
def contour_extraction_pipeline(image, box_color):

    # Select color range
    result = hsv_threshold(image, box_color)

    # Convert to Greyscale to facilitate thresholding
    img_grey = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)

    # Display image
#   plt.imshow(cv2.cvtColor(img_grey, cv2.COLOR_BGR2RGB))
#   plt.xlabel('Pixels')
#   plt.ylabel('Pixels')
#   plt.title('Greyscale')
#   plt.show()

    # Threshold to segment the selected color of boxes and the background
    ret,img_thres = cv2.threshold(img_grey,20, 255, 0)

    # Display image
#   plt.imshow(cv2.cvtColor(img_thres, cv2.COLOR_BGR2RGB))
#   plt.xlabel('Pixels')
#   plt.ylabel('Pixels')
#   plt.title('Threshold')
#   plt.show()

    # Morphological Opening to clean segmentation (remove false positives)
    kernel = np.ones((5,5),np.uint8) # Structuring element is 5x5
    img_open = cv2.morphologyEx(img_thres, cv2.MORPH_OPEN, kernel)

    # Display image
#   plt.imshow(cv2.cvtColor(img_open, cv2.COLOR_BGR2RGB))
#   plt.xlabel('Pixels')
#   plt.ylabel('Pixels')
#   plt.title('Morphological Opening')
#   plt.show()

    # Calculate Contours
    im2, contours, hierarchy = cv2.findContours(img_open, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #RETR_EXTERNAL

    # Select contours larger than a specified area
    minimum_area = 2000
    selected_contours = []

    img_contour_draw = image.copy()

    for i in range(0,len(contours)): # Iterate through all contours in pictures
        if cv2.contourArea(contours[i])>minimum_area: # Select only contours above the specified area
            selected_contours.append(contours[i])

             # Draw contour on image
#            cv2.drawContours(img_contour_draw, contours,i, (0,255,0),3) # #Draw each contours on the original image
#
#            # Calculate contour center of mass
#            M = cv2.moments(contours[i])
#            cX = int(M["m10"] / M["m00"])
#            cY = int(M["m01"] / M["m00"])

             # Marks contour index on image
#            font = cv2.FONT_HERSHEY_SIMPLEX
#            org = (cX, cY)
#            fontScale = 1
#            text_color = (255, 255, 255)
#            thickness = 3
#            cv2.putText(img_contour_draw, str(i), org, font, fontScale, text_color, thickness, cv2.LINE_AA)

    # Display image
#   plt.imshow(cv2.cvtColor(img_contour_draw, cv2.COLOR_BGR2RGB))
#   plt.xlabel('Pixels')
#   plt.ylabel('Pixels')
#   plt.title('Contours')
#   plt.show()

    return selected_contours

# --- EMain program ---
def vision_main(image):
    # Load Image
    # image = image_acquisition(2)

    # Display image
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.xlabel('Pixels')
    # plt.ylabel('Pixels')
    # #plt.title('RGB')
    # plt.show()

    # Get all contours with contour extraction pipeline
    contours_blue = contour_extraction_pipeline(image,"blue")
    contours_red = contour_extraction_pipeline(image,"red")

    # Append contours to one list
    appended_contours = list(contours_blue)

    for i in range(0,len(contours_red)):
        appended_contours.append(contours_red[i])

    # Return zeros and empty image if no contours were found
    img_msg = numpy_to_msg(image)
    if len(appended_contours)==0:
        return 0., 0., 0., 0, img_msg # Failed
        # return 0., 0., 0., 0 # Failed

    # Calculate Image Center
    image_center_x = int(image.shape[1]/2)
    image_center_y = int(image.shape[0]/2)

    # Define Empty Lists
    center_distance = []
    rect = []
    box = []

    # Draw Oriented Bounding Boxes
    for i in range(0,len(appended_contours)):
        # Calculate Oriented Bounding Box (OBB) of the selected contours
        rect.append(cv2.minAreaRect(appended_contours[i]))

        # Find the corner coordinates of OBB     # Convert corner coordinates to integer
        box.append(np.int0(cv2.boxPoints(rect[i])))

        # Draw OBB on image
        img_obb = cv2.drawContours(image,[box[i]],0,(255,255,255),3)

        # Calculate Euclidean distance between the center of every OBB and the image center
        center_distance.append(math.sqrt((((rect[i][0][0])-image_center_x) ** 2) + (((rect[i][0][1])-image_center_y) ** 2)))

        # Mark distance to Center
        img_obb = cv2.line(img_obb,
                               (image_center_x,image_center_y),
                               (int(rect[i][0][0]),int(rect[i][0][1])),
                               (0,255,255),3)

        # OBB index
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (int(rect[i][0][0]), int(rect[i][0][1]))
        fontScale = 1
        text_color = (255, 255, 255)
        thickness = 3
        img_obb = cv2.putText(img_obb, str(i), org, font, fontScale, text_color, thickness, cv2.LINE_AA)

    # Display image
#   plt.imshow(cv2.cvtColor(img_obb, cv2.COLOR_BGR2RGB))
#   plt.xlabel('Pixels')
#   plt.ylabel('Pixels')
#   plt.title('Contours')
#   plt.show()

    # Sort based on center_distance list from closest to furthest from center
    center_distance_sorted = sorted(center_distance)

    # List of possible gripper orientations
    rotation_list = [0,90]

    # Find the location and gripper orientation for picking the closest possible box
    for distance in center_distance_sorted: # Iterate through all boxes
        for rotation in rotation_list: # Iterate through all rotation angles

            # Find the index of the selected index in the original center_distance list
            # The is the same index as in the OBB features array "rect"
            index = center_distance.index(distance)
#           print("Selected index: "+str(index))

            # Create black frame with the dimensions of the original image
            black_frame = np.zeros((image.shape[0],image.shape[1],1), np.uint8)

            # Draw a mask on seperate copies of the black frame for every box
            mask_list = []
            for i in range(0,len(box)):
                mask_list.append(cv2.fillPoly(black_frame.copy(), [box[i]], (255, 255, 255)))

                # Display image
#               plt.imshow(mask_list[i],cmap='gray')
#               plt.title('Mask'+str(i))
#               plt.show()

            # Draw gripper area on selected index
            tol = 60 # Gripper width (Pixels)

            mask_list[index] = cv2.line(mask_list[index],
                                   (int((rect[index][0][0])-tol*math.cos(math.radians(rect[index][2]-rotation))),int((rect[index][0][1])-tol*math.sin(math.radians(rect[index][2]-rotation)))),
                                   (int((rect[index][0][0])+tol*math.cos(math.radians(rect[index][2]-rotation))),int((rect[index][0][1])+tol*math.sin(math.radians(rect[index][2]-rotation)))),
                                   (255,255,255),40)

            #  # Display image (box area with gripper augmentation)
            # plt.title("Mask "+str(index))
            # plt.imshow(mask_list[index],cmap='gray')
            # plt.show()

            # List of collision flags is reset for each box iteration
            collision_flag_list = []

            # Find itersection between the mask of the selected box and all other boxes
            for i in [x for x in range(0,len(mask_list)) if x != index]: # Compare with all masks except it's own
                img_bwa = cv2.bitwise_and(mask_list[index],mask_list[i]) # Intersection is found by a bitwise and

                # # Display image (Mask intersection)
                # plt.title("Mask "+str(index)+" and Mask "+str(i))
                # plt.imshow(img_bwa,cmap='gray')
                # plt.show()

                if cv2.countNonZero(img_bwa) > 0:
                    #print("Gripper collision with index "+str(i)+", Overlap: "+str(cv2.countNonZero(img_bwa))+"pixels")
                    collision_flag_list.append(1) # Append a highflag if there is an intersection

                    break # Stop interation, if there is an intersection

                else:
                    collision_flag_list.append(0) # Append 0 if there is no intersection

            if 1 not in collision_flag_list: # if there are no flags, and thereby no collisions: Calculate the position and angle of the selected box for the robot,
#                print("No gripper collision", collision_flag_list)
                x_center_offset = rect[index][0][0] - image_center_x
                y_center_offset = rect[index][0][1]- image_center_y
                angle_offset = rect[index][2]+rotation

                # Determine the color of the seleted box from the length of the blue_contour list
                if index <= len(contours_blue)-1:
                    color = 1 # Blue

                elif index > len(contours_blue)-1:
                    color = 2 # Red

                else:
                    color = 0 # Fail

                #Mark Pick Angle on contour image
                img_obb = cv2.line(img_obb,
                                       (int((rect[index][0][0])-50*math.cos(math.radians(rect[index][2]+rotation))),int((rect[index][0][1])-50*math.sin(math.radians(rect[index][2]+rotation)))),
                                       (int((rect[index][0][0])+50*math.cos(math.radians(rect[index][2]+rotation))),int((rect[index][0][1])+50*math.sin(math.radians(rect[index][2]+rotation)))),
                                       (255,255,0),3)

                img_msg = numpy_to_msg(img_obb)
                return x_center_offset, y_center_offset, angle_offset, color, img_msg
                # return x_center_offset, y_center_offset, angle_offset, color


    # If there is still a collision flag after all iterations: no suitable pick can be found
    if 1 in collision_flag_list or collision_flag_list==[]:
#       print("No collision free pick found")
        black_frame = np.zeros((image.shape[0],image.shape[1],1), np.uint8)

        img_msg = numpy_to_msg(black_frame)
        return 0., 0., 0., 0, img_msg # Failed
        # return 0., 0., 0., 0 # Failed
