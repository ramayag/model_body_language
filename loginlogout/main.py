from .PoseDetector import PoseDetector
from .more_functions import more_functions
# import motion
import math
import cv2
import mediapipe as mp
import numpy as np
from experta import *
from enum import Enum
# import mysql.connector
# import pymssql
from sqlalchemy import create_engine
from .connection_database import DataBase
import time
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .views import store 
# import django

# # Set the DJANGO_SETTINGS_MODULE environment variable
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.projectapp.settings')

# # Configure Django settings
# django.setup()


# from connection_database import user_id

# var = 5
path = r'C:\Users\USER\Desktop\proj\proj\db.sqlite3'

class Globals:
    var = 5




# @csrf_exempt
# def set_global(request):
#     global var
#     if request.method == 'POST':
#         Globals.var = request.POST.get('var')
#         print (Globals.var)
#         return JsonResponse({'message': 'Variable set successfully.'})
#     else:
#         return JsonResponse({'message': 'Invalid request method.'})
        


class Main : 

    @csrf_exempt
    def main(request):
        detector = PoseDetector()

        cap = cv2.VideoCapture(0)
        frame_count=0

        #تعريف متغير مصفوفة الحركات : 
        motion_in_secound_array= [] 
        motions_array = []
        start_time = time.time()
        sholder_points = []
        # con_time = time.time()
        is_sin = False
        correct_var =None
        prev_frame = None
        frames_landmarks = []


        
        keypoints = []
        while cap.isOpened():
            try : 
                frame_count=frame_count+1
                if frame_count%1==0:
                    # frame_count=0
                    success, image = cap.read()

                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    
                    image = cv2.flip(image,1)
                    blackie = np.zeros(image.shape) # Black image
                    image,blackie = detector.find_pose(image ,blackie)
                    h, w = image.shape[:2]
                    detector.Landmark_pos(w,h)
                    more = more_functions()
            #         if detector.results



                    image = more.draw_img(image,
                                str(more.angle_between_points(detector.R_sholder, detector.R_elbow, detector.R_wrist)),
                                    [100,100])
                    more.draw_img(blackie,
                                str(more.angle_between_points(detector.R_sholder, detector.R_elbow, detector.R_wrist)),
                                    [100,100])

            #         destance = destances(detector)        
            #         diatance_sholders,diatance_wrist,distance_RSH_LW,distance_LSH_RW,distance_REL_LW,distance_LEL_RW , distance_LEL_LW,distance_REL_RW,distance_RSH_RW,distance_LSH_LW,distance_nose_RW,distance_nose_LW,distance_RSH_Nose ,distance_LSH_Nose   = destance
                                        #اخذ نقاط الكتف لاستخدامها في كشف الاهتزاز 
                    if detector.R_sholder is None :
                         print ('NONEEE')
                    else : 
                       sholder_points.append(detector.R_sholder)


                   
                    variable ,image , blackie =more.expertsys(image, blackie , detector)

                    tupl = (variable ,detector.return_keypoints() )
                    frames_landmarks.append(tupl)

                    #اضافة الحركة الى المصفوفة تبع الحركات 
                    try :
                        par_time = time.time() 
                        partly_time = par_time - start_time
                        
                        if variable is not None :  
                            motion_in_secound_array.append(variable.name)
                            
                            

                            if int(partly_time)%3 ==0 and prevent_repeate != int(partly_time):
                                par_time = time.time() 
                                partly_time = par_time - start_time
                                general_motion = more.general_motion_in_secound(motion_in_secound_array)
                                print(str(partly_time) + "the motion in secound  : : : "+ str(general_motion))
                                motions_array.append(general_motion)
                                motion_in_secound_array=[]
                                # try : 
                                most_similar_landmark_tuple = more.find_most_similar_landmarks(frames_landmarks)
                                correct_var, most_similar_landmarks = most_similar_landmark_tuple
                                
                                
                                # correct_var = more.spatial_analysis(frames_landmarks)
                                cv2.putText(blackie ,"co var" + str(correct_var) ,(25,100),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)
                                # except : 
                                #      print ('in thiss')
                                frames_landmarks = []




                            if int(partly_time)%5 ==0 and prevent_repeate != int(partly_time): 
                                motion_eval=more.motions_evaluations(motions_array[-5:-1])
                                print("you still on your motion for long time !!!!!!!!!!!!" + str(motion_eval)) 
                                print (frames_landmarks) 
                                                                                                                        
                        if int(partly_time)%5 ==0 and prevent_repeate != int(partly_time): 
                            con_time = int(partly_time)
                            newPoint_sholder = more.plot_periodic_signal(sholder_points, time_step=0.0001)
                            # print("ssssnewPoint_sholder")
                            # print(newPoint_sholder)
                            newPoint_sholder = more.plot_periodic_signal(newPoint_sholder, time_step=0.0001)
                            # print("ssssnewPoint_sholder222")
                            # print(newPoint_sholder)
                            is_sin =  more.is_sin_signal(newPoint_sholder)
                            print("isssssss sin ?   " )
                            print (is_sin)
                            cv2.putText(blackie ,"isssssss periodic ?   " + str(is_sin) ,(25,25),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)
                            sholder_points = []
                            

                        cv2.putText(blackie, "isssssss periodic ?   " + str(is_sin), (25, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 99, 0), 2)
                        cv2.putText(blackie ,"co var" + str(correct_var) ,(25,100),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)



    
                        prevent_repeate = int(partly_time)
                    except Exception as e:
                        print('error:', e)


                    cv2.putText(blackie,str(variable),(100,400),cv2.FONT_HERSHEY_PLAIN,2,(255,99,0),2)
                    
                    cv2.imshow("blackie", blackie)
                    cv2.imshow("Image", image)
                    cv2.waitKey(1)
                    if not success:
                        break
                
                prev_frame = gray.copy()

                if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('×'):
                                break   
            except Exception as e:
                        print('Error:', e)    
        cap.release()
        cv2.destroyAllWindows()


        end_time = time.time()
        
        elapsed_time = end_time - start_time

        DataBase.get_tables(path)
        # global var 
        print ("var isisis" + str (Globals.var))
        DataBase.store_vedio_cols(path ,frame_count,int(elapsed_time),1 ,Globals.var)
        print(frame_count)
        print(elapsed_time)

        #حساب التقييم لكل حركة 
        motion_count = more.motions_evaluations(motions_array)
        print(motion_count)
        counter = 0
        for key, value in motion_count.items():
            if key == 'HAND_ON_HEAD' :
                counter += value 
        print(counter)
        # print('arrrrrrrrrrrray' + str ( motions_array))

        DataBase.store_Hands_cols(path,motion_count,elapsed_time) 

        print("the sholder_points is " + str (sholder_points))




        # DataBase.is_user_logged_in()

        # print(motion_count.get('<motion.HAND_ON_HEAD: 6>'))               



if __name__ == "__main__":
    # print("iddddd" +str(connection_database.user_id))
    Main.main()
    # connection_database.DataBase.get_cols_name(path)
    
