
from .motion import ReturnValueFact ,Tree , angle_L_sholder,angle_L_elbow , angle_R_sholder,angle_R_elbow,Dist_Wrists_sholds,Dist_LSH_RW__LSH_LW,BodyPart_Lsh_Lw_x,BodyPart_Rsh_Rw_x,Dist_N_LW_LSH,\
Dist_N_RW_RSH,Dist_N_LW_LSH,Y_RW_POS ,Y_LW_POS,direction_type ,OUT_BOX,Dist_RSH_Rw__RSH_RH ,Dist_LSH_Lw__LSH_LH,motion

import math
import cv2
import mediapipe as mp
import numpy as np
from experta import *
from enum import Enum
# import mysql.connector
# import pymssql
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import procrustes
from fastdtw import fastdtw

class in_out(Enum):
    inside_box = 0 
    outside_box = 1 
    half_inside_box= 2 
 
class more_functions : 

    def draw_img(self,image,text,position):
        # cv2.putText(image,text,(position[0],position[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        return image


    # حساب الزوايا
    def angle_between_points(self ,p1, p2, p3):
        # calculate vectors
        v1 = (p1[0] - p2[0] , p1[1] - p2[1])
        v2 = (p3[0] - p2[0] , p3[1] - p2[1] )
        # calculate angle between vectors
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        mag_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
        mag_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)
        try:
            cos_angle = dot_product / (mag_v1 * mag_v2)
            rad_angle = math.acos(cos_angle)
        except:
            rad_angle=0
        # convert to degrees
        deg_angle = math.degrees(rad_angle)
        return deg_angle





    def is_sin_signal(self,points, threshold=0.95):
        # Convert x and y coordinates
        x = np.array([point[0] for point in points])
        y = np.array([point[1] for point in points])

        # Compute the differences between consecutive x coordinates
        dx = np.diff(x)

        # Compute the differences between consecutive y coordinates
        dy = np.diff(y)

        # Calculate the Euclidean distances between consecutive points
        distances = np.sqrt(dx**2 + dy**2)

        # Compute the mean distance
        mean_distance = np.mean(distances)

        # Compute the standard deviation of the distances
        std_distance = np.std(distances)

        # Compute the coefficient of variation (ratio of standard deviation to mean)
        cv = std_distance / mean_distance

        # Determine if the coefficient of variation is below the threshold
        if cv < threshold:
            return True
        else:
            return False


    def plot_periodic_signal(self, point_positions, time_step=0.0001):
        # Convert x and y coordinates
        x = [point[1] for point in point_positions]
        y = [point[0] for point in point_positions]

  
        
        new_positions = [[x[i] + time_step, y[i] + time_step] for i in range(len(point_positions))]
        return new_positions





    def turnR_L(self,img,L_sholder,R_sholder,R_hip):
        
        ang=self.angle_between_points(L_sholder,R_sholder,R_hip)
        # cv2.putText(img,str(ang),(50,50),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
        if ang < 77 :
            cv2.putText(img,"you turn right",(50,450),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
            
            return 1
        elif ang > 91 :   
            cv2.putText(img,"you turn left",(50,450),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
            return 2
        else :
            cv2.putText(img,"you are straight",(50,450),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
            return 0

   
    def calculate_hand_strike_zone(self,img,x_R, y_R,x_L,y_L,strike_zone_x, strike_zone_y):
        """
        Calculates if hand movements are within the defined strike zone.

        Args:
            x (float): X-coordinate of hand movement.
            y (float): Y-coordinate of hand movement.
            z (float): Z-coordinate of hand movement.
            strike_zone_x (tuple): Tuple of minimum and maximum values for x-coordinate of the strike zone.
            strike_zone_y (tuple): Tuple of minimum and maximum values for y-coordinate of the strike zone.
            strike_zone_z (tuple): Tuple of minimum and maximum values for z-coordinate of the strike zone.

        Returns:
            bool: True if hand movement is within the strike zone, False otherwise.
        """
        
        # Check if the hand movement is within the strike zone
        if strike_zone_x[0] <= x_R <= strike_zone_x[1] and \
        strike_zone_y[0] <= y_R <= strike_zone_y[1]and \
        strike_zone_x[0] <= x_L <= strike_zone_x[1] and \
        strike_zone_y[0] <= y_L <= strike_zone_y[1]: 
            value = in_out.inside_box
            return cv2.putText(img,"you are in the zone",(400,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2),value

        elif (strike_zone_x[0] <= x_R <= strike_zone_x[1] and \
        strike_zone_y[0] <= y_R <= strike_zone_y[1]) or \
        (strike_zone_x[0] <= x_L <= strike_zone_x[1] and \
        strike_zone_y[0] <= y_L <= strike_zone_y[1]): 
            value = in_out.half_inside_box
            return cv2.putText(img,"you are partialy in the zone",(400,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2),value

        else:
            value = in_out.outside_box
            return cv2.putText(img,"you are not in the zone",(400,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2),value
    

    def strike_zone(self,imgRGB,L_sholder,R_sholder,R_wrist,L_wrist,x):
        
        dist = math.sqrt((L_sholder[0] - R_sholder[0]) ** 2 + (L_sholder[1] - R_sholder[1]) ** 2)
        dist1=dist * (1/2)
        dist2=dist * (1/4)

        
        if x==0:

        
            p0=int(R_sholder[0]-dist1)
            p1=int(R_sholder[1]+dist2)
            p2=int(L_sholder[0]+dist1)
            p3=int(R_sholder[1]+dist*1.3)
            
            
            cv2.putText(imgRGB,"*",(p0,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p0,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            
            return self.calculate_hand_strike_zone(imgRGB,R_wrist[0],R_wrist[1],L_wrist[0],L_wrist[1] ,(p0,p2),(p1,p3))


        elif x==1:
            
            p0=int(R_sholder[0])
            p1=int(R_sholder[1]+dist2)
            p2=int(L_sholder[0]+1.5*dist)
            p3=int(R_sholder[1]+dist*1.8)

            
            cv2.putText(imgRGB,"*",(p0,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p0,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            
            return self.calculate_hand_strike_zone(imgRGB,R_wrist[0],R_wrist[1],L_wrist[0],L_wrist[1] ,(p0,p2),(p1,p3))
            
            
        elif x==2:
            
            p0=int(R_sholder[0]-(1.5*dist))
            p1=int(R_sholder[1]+dist2)
            p2=int(L_sholder[0])
            p3=int(R_sholder[1]+dist*1.8)

            
            cv2.putText(imgRGB,"*",(p0,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p0,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            
            return self.calculate_hand_strike_zone(imgRGB,R_wrist[0],R_wrist[1],L_wrist[0],L_wrist[1] ,(p0,p2),(p1,p3))



    def destances(self , detector) : 
                    diatance_sholders = math.dist(detector.R_sholder, detector.L_sholder)
                    diatance_wrist = math.dist(detector.R_wrist, detector.L_wrist)
                    
                    distance_RSH_LW =math.dist(detector.R_wrist, detector.L_sholder)
                    distance_LSH_RW =math.dist(detector.L_wrist, detector.R_sholder)
                    
                    distance_REL_LW =math.dist(detector.L_wrist, detector.R_elbow)
                    distance_LEL_RW =math.dist(detector.R_wrist, detector.L_elbow)
                    
                    distance_LEL_LW =math.dist(detector.L_wrist, detector.L_elbow)
                    distance_REL_RW =math.dist(detector.R_wrist, detector.R_elbow)

                    distance_RSH_RW =math.dist(detector.R_wrist, detector.R_sholder)
                    distance_LSH_LW =math.dist(detector.L_wrist, detector.L_sholder)

                    distance_nose_RW =math.dist(detector.R_wrist, detector.Nose)
                    distance_nose_LW =math.dist(detector.L_wrist, detector.Nose)
                    
                    distance_RSH_Nose =math.dist(detector.R_sholder, detector.Nose)
                    distance_LSH_Nose =math.dist(detector.L_sholder, detector.Nose)
                    
                    return diatance_sholders,diatance_wrist,distance_RSH_LW,distance_LSH_RW,distance_REL_LW,distance_LEL_RW  
                    return  distance_LEL_LW,distance_REL_RW,distance_RSH_RW,distance_LSH_LW,distance_nose_RW,distance_nose_LW 
                    return distance_RSH_Nose ,distance_LSH_Nose


    def general_motion_in_secound(self,motion_array):
        counts = {}
        for elem in motion_array:
            if elem in counts:
                counts[elem] += 1
            else:
                counts[elem] = 1        
        # for key, value in counts.items():
        #     if value > 1:
        #         print(f"{key} appears {value} times in the array.")
        max_key = max(counts, key=counts.get)
        return max_key


    # def check_state(self , arra):
    #     thresh = 8
    #     array = arra[-9:]
    #     length = len(array)
    #     newest_80_percent = int(length * 0.8)

    #     # if length == 0:
    #     #     return False

    #     # Check if all elements are the same using set()
    #     if len(set(array)) == 1:
    #         return True

    #     # Check if the newest 80% of elements are the same using set()
    #     if len(set(array[-newest_80_percent:])) == 1:
    #         return True

    #     return False
    def check_state(self, arra):
        thresh = 8
        array = arra[-9:]
        length = len(array)
        newest_60_percent = int(length * 0.6)

        # Check if length is less than 2, return False
        if length < 2:
            return False

        # Check if the last two elements are the same
        if array[-1] == array[-2]:
            # Count the occurrences of the most common element
            most_common_element_count = array.count(array[-1])
            
            # Check if the most common element appears at least 60% of the time
            if most_common_element_count / length >= 0.6:
                return True
        
        return False


    def get_repeated_parts(self , arr, threshold):
        repeated_parts = []
        non_repeated_count = 0  # Count of non-repeated elements
        current_part = [arr[0]]
        count = 1

        for i in range(1, len(arr)):
            if arr[i] == arr[i - 1]:
                count += 1
                current_part.append(arr[i])
            else:
                if count >= threshold:
                    repeated_parts.extend(current_part)
                else:
                    non_repeated_count += len(current_part)  # Increment non-repeated count
                current_part = [arr[i]]
                count = 1
        
        if count >= threshold:
            repeated_parts.extend(current_part)
        else:
            non_repeated_count += len(current_part)  # Increment non-repeated count

        return repeated_parts, non_repeated_count
    


    def motions_evaluations (self ,motion_array , thresh):
        counts = {}
        log_counts = {}
        counts[motion.CORRECT_MOTION.name] = 0

        # print (" befor log log log " + str (motion_array))
        motion_array,correct_element =self.get_repeated_parts(motion_array ,thresh)
        for elem in motion_array:
            if elem in counts:
                counts[elem] += 1
            else:
                counts[elem] = 1
                
        counts[motion.CORRECT_MOTION.name] += correct_element 

                
        for key, value in counts.items():
            if value > 0:  # Check if the value is valid for logarithm
                log_counts[key] = math.log(value * 10)
            else:
                log_counts[key] = float('-inf')  # Handle invalid case (e.g., log of 0 or negative)
        # print (" after  log log log " + str (motion_array))
        # print (" the logarithem " + str (log_counts)  +str(motion_array))

        return log_counts   
    
    

    def spatial_analysis(self , frames_landmarks):
        # Calculate the Euclidean distance between all pairs of keypoints for each frame
        distances = []
        
        for tupl in frames_landmarks:
            variable, keypoints = tupl
            keypoints = np.array(keypoints)
            
            # Calculate the Euclidean distance between all pairs of keypoints
            n = len(keypoints)
            pairwise_distances = []
            
            for i in range(n):
                for j in range(i + 1, n):
                    distance = np.linalg.norm(keypoints[i] - keypoints[j])
                    pairwise_distances.append(distance)
            
            # Calculate the average distance for the frame
            frame_distance = np.mean(pairwise_distances)
            distances.append(frame_distance)
        
        # Determine the frame with the lowest distance
        if not distances:
            raise ValueError("No distances calculated")
        
        lowest_distance_index = np.argmin(distances)
        correct_var = frames_landmarks[lowest_distance_index][0]
        
        return correct_var



    def calculate_similarity(self,landmarks1, landmarks2):
    # Normalize the landmark arrays to have zero mean and unit variance
        landmarks1_normalized = (landmarks1 - landmarks1.mean(axis=0)) / landmarks1.std(axis=0)
        landmarks2_normalized = (landmarks2 - landmarks2.mean(axis=0)) / landmarks2.std(axis=0)

        # Align the landmark arrays using Procrustes analysis
        _, _, disparity = procrustes(landmarks1_normalized, landmarks2_normalized)

        # Calculate the similarity as the negative Procrustes disparity
        similarity = -disparity

        return similarity

    def find_most_similar_landmarks(self,landmark_tuples):
        num_tuples = len(landmark_tuples)
        similarity_scores = np.zeros((num_tuples, num_tuples))

        # Calculate similarity score between each pair of landmark tuples
        for i in range(num_tuples):
            for j in range(i, num_tuples):
                landmarks1 = np.array(landmark_tuples[i][1])
                landmarks2 = np.array(landmark_tuples[j][1])
                similarity = self.calculate_similarity(landmarks1, landmarks2)
                similarity_scores[i, j] = similarity
                similarity_scores[j, i] = similarity

        # Find the index of the landmark tuple with the highest similarity score
        most_similar_index = np.argmax(np.sum(similarity_scores, axis=1))

        return landmark_tuples[most_similar_index]

# Example usage
# landmark_tuples = [("frame1", landmark_array1), ("frame2", landmark_array2), ..., ("frameN", landmark_arrayN)]

    def calculate_dtw_distance(self , landmarks_sequence):
        best_element = None
        best_distance = float('inf')

        for i in range(len(landmarks_sequence)):
            element = landmarks_sequence[i][1]  # Extract the keypoints from the tuple
            current_distance = 0

            for j in range(len(landmarks_sequence)):
                if i != j:
                    other_element = landmarks_sequence[j][1]  # Extract the keypoints from the other tuple
                    distance, _ = fastdtw(element, other_element)  # Calculate DTW distance
                    current_distance += distance

            if current_distance < best_distance:
                best_element = landmarks_sequence[i]  # Store the entire tuple
                best_distance = current_distance

        return best_element




    def expertsys(self , image, blackie , detector) : 
                            #حساب المسافات لاستخدامها في القوانين
                    
        diatance_sholders = math.dist(detector.R_sholder, detector.L_sholder)
        diatance_wrist = math.dist(detector.R_wrist, detector.L_wrist)

        distance_RSH_LW =math.dist(detector.R_wrist, detector.L_sholder)
        distance_LSH_RW =math.dist(detector.L_wrist, detector.R_sholder)

        distance_REL_LW =math.dist(detector.L_wrist, detector.R_elbow)
        distance_LEL_RW =math.dist(detector.R_wrist, detector.L_elbow)

        distance_LEL_LW =math.dist(detector.L_wrist, detector.L_elbow)
        distance_REL_RW =math.dist(detector.R_wrist, detector.R_elbow)

        distance_RSH_RW =math.dist(detector.R_wrist, detector.R_sholder)
        distance_LSH_LW =math.dist(detector.L_wrist, detector.L_sholder)

        distance_RSH_RH = math.dist(detector.R_hip, detector.R_sholder)
        distance_LSH_LH = math.dist(detector.L_hip, detector.L_sholder)

        distance_nose_RW =math.dist(detector.R_wrist, detector.Nose)
        distance_nose_LW =math.dist(detector.L_wrist, detector.Nose)

        distance_RSH_Nose =math.dist(detector.R_sholder, detector.Nose)
        distance_LSH_Nose =math.dist(detector.L_sholder, detector.Nose)
                
                
        R_Wrist_angle = self.angle_between_points(detector.R_sholder, detector.R_elbow, detector.R_wrist)
        L_Wrist_angle = self.angle_between_points(detector.L_sholder, detector.L_elbow, detector.L_wrist)

        R_sholder_angle = self.angle_between_points(detector.R_hip,detector.R_sholder, detector.R_elbow)
        L_sholder_angle = self.angle_between_points(detector.L_hip, detector.L_sholder, detector.L_elbow)


        #استدعاء الاكسبيرت سيستم                 
        instance_of_my_class = ReturnValueFact()                
        engine = Tree(instance_of_my_class)
        engine.set_normalize_destance(diatance_sholders)                
        # var = more.turnR_L(image,detector.L_sholder,detector.R_sholder,detector.R_hip) 
        var=self.turnR_L(image,detector.L_sholder,detector.R_sholder,detector.R_hip)
        _ ,outside_box = self.strike_zone(blackie,detector.L_sholder,detector.R_sholder,detector.R_wrist,detector.L_wrist,var)                    
        # print( "the out box " + str (outside_box))
        # _ ,Head = more.strike_zone(blackie,detector.LEFT_EAR,detector.RIGHT_EAR,detector.R_wrist,detector.L_wrist,var)                    

        # print ( "vaaaaaaaaaa " + str(var))
        # print("the out side isisisisisisisisiiisi" + str(outside_box))
        
        # cv2.putText(image , str(var) ,(50,450),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)


        #مكتف وعلى جنب 
        engine.reset()
        engine.declare(
                OUT_BOX(out = str (outside_box)),
                angle_L_sholder(angle1=L_sholder_angle),
                angle_L_elbow(angle2=L_Wrist_angle),
                angle_R_sholder(angle3=R_sholder_angle),
                angle_R_elbow(angle4=R_Wrist_angle),
                Dist_Wrists_sholds (dist1=diatance_wrist,dist2=diatance_sholders),
                Dist_LSH_RW__LSH_LW(dist3=distance_LSH_RW,dist4=distance_LSH_LW),
                BodyPart_Lsh_Lw_x(Lsh_x_pos=detector.L_sholder[0],Lw_x_pos = detector.L_wrist[0]),
                BodyPart_Rsh_Rw_x(Rsh_x_pos=detector.R_sholder[0],Rw_x_pos = detector.R_wrist[0]),
                Dist_N_LW_LSH(dist1 = distance_nose_LW,dist2 = distance_LSH_Nose),
                Dist_N_RW_RSH(dist3 = distance_nose_RW,dist4 = distance_RSH_Nose),
                Dist_RSH_Rw__RSH_RH(dist1=distance_RSH_RH,dist2=distance_RSH_RW),
                Dist_LSH_Lw__LSH_LH(dist3=distance_LSH_LH,dist4=distance_LSH_LW),
                Y_LW_POS(y_lw =detector.L_wrist[1] ,y_lsh = detector.L_sholder[1]),
                Y_RW_POS(y_rw = detector.R_wrist[1],y_rsh = detector.R_sholder[1]),
                direction_type(direct = var ),


            #  motion.BodyPart_L(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
                
                )
        engine.run()   




        variable = engine.instance_of_my_class.my_variable

        return variable ,image , blackie




        
# import numpy as np
# from scipy.spatial.distance import euclidean
# from fastdtw import fastdtw

# # Initialize empty reference patterns
# reference_A = []
# reference_B = []
# reference_C = []

# # Define the sequence of standing cases
# standing_cases = ["A", "A", "A", "A", "A", "B", "B", "C", "C", "C", "B", "A", "B"]

# # Function to calculate the DTW distance between two sequences
# def dtw_distance(sequence1, sequence2):
#     # Use fastdtw to calculate the DTW distance
#     distance, _ = fastdtw(sequence1, sequence2, dist=euclidean)
#     return distance

# # Update the reference patterns based on the observed standing cases
# for case in standing_cases:
#     if case == "A":
#         # Append the current case to reference_A
#         reference_A.append(case)
#     elif case == "B":
#         # Append the current case to reference_B
#         reference_B.append(case)
#     elif case == "C":
#         # Append the current case to reference_C
#         reference_C.append(case)

# # Calculate the DTW distance between each standing case and the reference patterns
# dist_A = dtw_distance(standing_cases, reference_A)
# dist_B = dtw_distance(standing_cases, reference_B)
# dist_C = dtw_distance(standing_cases, reference_C)

# # Determine the correct standing case based on the DTW distances
# if dist_A < dist_B and dist_A < dist_C:
#     correct_case = "A"
# elif dist_B < dist_A and dist_B < dist_C:
#     correct_case = "B"
# else:
#     correct_case = "C"

# print("Correct standing case:", correct_case)
         
         
         ##########################333


# import numpy as np



# import mediapipe as mp
# import cv2

# # Initialize MediaPipe Pose model
# mp_pose = mp.solutions.pose

# # Define the reference patterns for each standing case
# reference_A = ["A", "A", "A", "A", "A"]
# reference_B = ["B", "B"]
# reference_C = ["C", "C", "C"]

# # Create a dictionary to hold the references for each case
# references = {"A": reference_A, "B": reference_B, "C": reference_C}

# # Initialize the video capture (Replace '0' with the path to your video file if needed)
# cap = cv2.VideoCapture(0)

# # Define a function for spatial analysis
# def spatial_analysis(keypoints, reference):
#     # Implement your spatial analysis code here
#     # Calculate relative distances or angles between keypoints and reference
#     # Return a similarity score or classification result

# # Process frames from the video
# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Convert the frame to RGB (MediaPipe requires RGB format)
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Detect pose landmarks
#         results = pose.process(frame_rgb)

#         if results.pose_landmarks:
#             # Get the list of keypoints (landmarks)
#             keypoints = [(lm.x, lm.y) for lm in results.pose_landmarks.landmark]

#             # Determine the standing case using spatial analysis
#             best_match = None
#             best_score = float('inf')
#             for case, reference in references.items():
#                 score = spatial_analysis(keypoints, reference)
#                 if score < best_score:
#                     best_score = score
#                     best_match = case

#             # Display the standing case on the frame
#             cv2.putText(frame, f"Standing Case: {best_match}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#         # Show the frame
#         cv2.imshow('Frame', frame)

#         if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
#             break

# # Release the video capture and close the windows
# cap.release()
# cv2.destroyAllWindows()








# #################################
# import cv2
# import numpy as np

# # Define the reference patterns for each standing case
# reference_A = ["A", "A", "A", "A", "A"]
# reference_B = ["B", "B"]
# reference_C = ["C", "C", "C"]

# # Create a dictionary to hold the references for each case
# references = {"A": reference_A, "B": reference_B, "C": reference_C}

# # Process frames with detected landmarks and perform spatial analysis
# def analyze_frames(frames, keypoints):
#     # Perform spatial analysis for each frame
#     scores = []
#     for frame_kps in keypoints:
#         # Determine the standing case using spatial analysis
#         best_match = spatial_analysis(frame_kps, references)
#         scores.append(best_match)

#     # Determine the correct standing case based on the majority vote
#     correct_case = max(set(scores), key=scores.count)

#     # Find the index of the frame corresponding to the correct case
#     correct_frame_index = scores.index(correct_case)

#     # Return the frame of the correct case
#     return frames[correct_frame_index]

# # Example usage
# frames = [...]  # Your list of frames
# keypoints = [...]  # Your list of detected keypoints for each frame

# correct_frame = analyze_frames(frames, keypoints)
# cv2.imshow("Correct Frame", correct_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()






