import math
import cv2
import mediapipe as mp
import numpy as np
from experta import *
from enum import Enum
# from .more_functions import more_functions

class in_out(Enum):
    inside_box = 0 
    outside_box = 1 
    half_inside_box= 2 

class motion(Enum):
    
    CLOSED_U_HANDS = 1
    CLOSED_D_HANDS = 2
    STRAIGHT_DOWN = 3 
    HAND_ON_HIP = 4 
    HAND_CROSSED = 5
    HAND_ON_HEAD = 6 
    HAND_CROSSED_LEFT =7 
    HAND_CROSSED_RIGHT = 8
    CLOSSED_HAND_LEFT = 9
    CLOSSED_HAND_RIGHT = 10
    STRAIGHT_DOWN_LEFT = 11
    STRAIGHT_DOWN_RIGHT = 12 
    HAND_ON_HEAD_right = 13 
    HAND_ON_HEAD_left = 14
    HAND_ON_HIP_Left = 15 
    HAND_ON_HIP_Right = 16 
    HANDS_OUT_BOX = 17
    CORRECT_MOTION = 18
    ON_SIDE = 19
        
############################# تعريف  enum خاصة بالاتجاهات  #####################################
class direction(Enum):
    straight = 0 
    right = 1 
    left = 2 
    
##############################        facts  تعريف ال  #######################################        
class destance(Fact):
    pass 

class angle(Fact):
    pass

class BodyPart(Fact):
    pass 

class direction_type (Fact): 
    pass 

class Out_Box(Fact): 
    pass

class Y_position(Fact): 
    pass

class angle_L_elbow(Fact) : 
    pass

class angle_R_elbow(Fact) : 
    pass

class angle_R_sholder(Fact) : 
    pass

class angle_L_sholder(Fact) : 
    pass

class Dist_Wrists_sholds(Fact) : 
    pass

class Dist_LSH_RW__LSH_LW(Fact) : 
    pass


class Dist_RSH_Rw__RSH_RH(Fact) : 
    pass

class Dist_LSH_Lw__LSH_LH(Fact) : 
    pass

class BodyPart_Lsh_Lw_x(Fact) : 
    pass

class BodyPart_Rsh_Rw_x(Fact) : 
    pass

class Dist_N_LW_LSH(Fact) : 
    pass

class Dist_N_RW_RSH(Fact) : 
    pass

class Y_RW_POS(Fact) : 
    pass

class Y_LW_POS(Fact) : 
    pass

class OUT_BOX (Fact):
    pass

class BodyPart_L (Fact):
    pass

class BodyPart_R (Fact):
    pass

class SuccessFact(Fact):
    pass

####################################      كلاس القواعد     ################################### 
class ReturnValueFact:
    my_variable = None 
    my_direction = None
    my_text = None
    normalize_destance = None
    def set_variable(self, value):
        if isinstance(value, motion):
            self.my_variable = value
   
    def set_direction(self, value):
        if isinstance(value, direction):
            self.my_direction = value
            
        
    def set_text(self, value):
        self.my_text = value     
    
    def set_normalize_destance(self, value):
        self.normalize_destance = value     


class Tree(KnowledgeEngine):
    def __init__(self, instance_of_my_class):
        super().__init__()
        self.instance_of_my_class = instance_of_my_class
        self.rule_matched = False
        
    def set_value_method(self, value):
        self.instance_of_my_class.set_variable(value)
        
    def set_direction_method(self, value):
        self.instance_of_my_class.set_direction(value)    

    def set_text_method(self, value):
        self.instance_of_my_class.set_text(value)        
        
    def set_normalize_destance(self, value):
        self.instance_of_my_class.set_normalize_destance(value)   


    @Rule(
    angle_L_elbow(angle2=P(lambda x: x >115)),
    angle_R_elbow(angle4=P(lambda x: x>115)),
    AS.fact1 << BodyPart_Rsh_Rw_x(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
    TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos < (Rsh_x_pos + 50)),
    TEST(lambda Rsh_x_pos,Rw_x_pos:( Rsh_x_pos - 50) < Rw_x_pos),
    AS.fact2 << BodyPart_Lsh_Lw_x(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
    TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos + 50)),
    TEST(lambda Lsh_x_pos,Lw_x_pos:( Lsh_x_pos - 50) < Lw_x_pos),
    # AS.fact3 << OUT_BOX(out= MATCH.out),
    # TEST(lambda out : out =='in_out.outside_box' ),
    # AS.fact3 << Dist_RSH_Rw__RSH_RH(dist1=MATCH.dist1, dist2=MATCH.dist2),
    # TEST(lambda dist1, dist2: dist2-10 < dist1 < dist2+10),
    # AS.fact4 << Dist_LSH_Lw__LSH_LH(dist3=MATCH.dist3, dist4=MATCH.dist4),
    # TEST(lambda dist3, dist4: dist4 -10 < dist3 < dist4 + 10),    
          
    # direction_type(direct = P(lambda x: x == 0))
    )
    def check5(self):
        value = motion.STRAIGHT_DOWN
        self.set_value_method(value) 
        self.rule_matched = True  

    @Rule(OR(AND(
          AND(AND(angle_L_sholder(angle1=P(lambda x: x <25)), angle_L_elbow(angle2=P(lambda x: x <40))),
          AS.fact1 <<  Dist_N_LW_LSH(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2)), 
          AS.fact3 <<  Y_LW_POS(y_lw = MATCH.y_lw,y_lsh =MATCH.y_lsh),TEST(lambda y_lw,y_lsh: y_lw < y_lsh)),

          
          AND(AND(angle_R_sholder(angle3=P(lambda x: x <25)), angle_R_elbow(angle4=P(lambda x: x <40))) ,
          AND (AS.fact2 <<  Dist_N_RW_RSH(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4)),
          AS.fact4 <<  Y_RW_POS(y_rw = MATCH.y_rw,y_rsh =MATCH.y_rsh),TEST(lambda y_rw,y_rsh: y_rw < y_rsh)) ,
          ),
          direction_type(direct = P(lambda x: x == 0))
           ) 
    def check10(self):        
        value =motion.HAND_ON_HEAD
        self.set_value_method(value) 
        self.rule_matched = True      


    @Rule(OR(AND(
          AND(AND(angle_L_sholder(angle1=P(lambda x: 25<x <40)), angle_L_elbow(angle2=P(lambda x: 30< x <60))),
          AS.fact1 <<  Dist_N_LW_LSH(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2)), 
          AS.fact3 <<  Y_LW_POS(y_lw = MATCH.y_lw,y_lsh =MATCH.y_lsh),TEST(lambda y_lw,y_lsh: y_lw < y_lsh)),

          
          AND(AND(angle_R_sholder(angle3=P(lambda x: 25<x <40)), angle_R_elbow(angle4=P(lambda x: 30< x <60))) ,
          AND (AS.fact2 <<  Dist_N_RW_RSH(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4)),
          AS.fact4 <<  Y_RW_POS(y_rw = MATCH.y_rw,y_rsh =MATCH.y_rsh),TEST(lambda y_rw,y_rsh: y_rw < y_rsh)) ,
          ),
          direction_type(direct = P(lambda x: x == 2))
           )  
    
    def check11(self):        
        value =motion.HAND_ON_HEAD
        self.set_value_method(value)
        self.rule_matched = True
  

        

    @Rule(OR(AND(
          AND(AND(angle_L_sholder(angle1=P(lambda x: 25<x <40)), angle_L_elbow(angle2=P(lambda x: 30< x <60))),
          AS.fact1 <<  Dist_N_LW_LSH(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2)), 
          AS.fact3 <<  Y_LW_POS(y_lw = MATCH.y_lw,y_lsh =MATCH.y_lsh),TEST(lambda y_lw,y_lsh: y_lw < y_lsh)),

          
          AND(AND(angle_R_sholder(angle3=P(lambda x: 25<x <40)), angle_R_elbow(angle4=P(lambda x: 30< x <60))) ,
          AND (AS.fact2 <<  Dist_N_RW_RSH(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4)),
          AS.fact4 <<  Y_RW_POS(y_rw = MATCH.y_rw,y_rsh =MATCH.y_rsh),TEST(lambda y_rw,y_rsh: y_rw < y_rsh)) ,
          ),
          direction_type(direct = P(lambda x: x == 1))
           )  
    def check12(self):        
        value =motion.HAND_ON_HEAD
        self.set_value_method(value)  
        self.rule_matched = True 
        

    @Rule (
    AS.fact1 << OUT_BOX(out= MATCH.out),
    TEST(lambda out : out =='in_out.outside_box' )    
    )
    def check18(self):        
        value =motion.HANDS_OUT_BOX
        self.set_value_method( value) 
        self.rule_matched = True


    @Rule( 
           angle_L_sholder(angle1=P(lambda x: x < 30)),
           angle_L_elbow(angle2=P(lambda x: 50 < x <100)),
           angle_R_sholder(angle3=P(lambda x: x < 30)),
           angle_R_elbow(angle4=P(lambda x: 50 < x <100)) ,
         AS.fact5 <<  Dist_Wrists_sholds(dist1 = MATCH.dist1,dist2 =MATCH.dist2),
         TEST(lambda dist1,dist2: dist1 <( dist2-(dist1*2))) ,
         AS.fact6 << Dist_LSH_RW__LSH_LW(dist3=MATCH.dist3, dist4=MATCH.dist4),
         TEST(lambda dist3, dist4: dist3 > dist4),
         direction_type(direct = P(lambda x: x == 0)) 
         )
    def check(self):        
        value =motion.CLOSED_U_HANDS
        self.set_value_method( value)
        self.rule_matched = True
    

    @Rule(angle_R_sholder(angle3=P(lambda x: x >30)), angle(angle4=P(lambda x:  135>x >80)),
         AS.fact2 << BodyPart_Rsh_Rw_x(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
         TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos > (Rsh_x_pos + 20)),
         direction_type(direct = P(lambda x: x == 2)))
    def check16(self):        
        value =motion.CLOSED_U_HANDS
        self.set_value_method( value)
        self.rule_matched = True
 

    @Rule(angle_L_sholder(angle1=P(lambda x: x >30)), angle_L_elbow(angle2=P(lambda x:  135>x >80)),
         AS.fact2 << BodyPart_Lsh_Lw_x(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
         TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos - 20)),
         direction_type(direct = P(lambda x: x == 1))
         )
    def check17(self):        
        value =motion.CLOSED_D_HANDS
        self.set_value_method( value) 
        self.rule_matched = True

    @Rule( angle_L_sholder(angle1=P(lambda x: x < 30)),
           angle_L_elbow(angle2=P(lambda x:  150>x >100)),
           angle_R_sholder(angle3=P(lambda x: x < 30)),
           angle_R_elbow(angle4=P(lambda x:  150>x >100)) ,
         AS.fact5 <<  Dist_Wrists_sholds(dist1 = MATCH.dist1,dist2 =MATCH.dist2),
         TEST(lambda dist1,dist2: dist1 < dist2),
         direction_type(direct = P(lambda x: x == 0)))
    def check2(self):        
        value =motion.CLOSED_D_HANDS
        self.set_value_method( value)
        self.rule_matched = True




    @Rule(
        angle_L_sholder(angle1=P(lambda x: x < 30)),
        angle_L_elbow(angle2=P(lambda x: x > 40)),
        angle_R_sholder(angle3=P(lambda x: x < 30)),
        angle_R_elbow(angle4=P(lambda x: x > 40)),
        AS.fact5 << Dist_Wrists_sholds(dist1=MATCH.dist1, dist2=MATCH.dist2),
        TEST(lambda dist1, dist2: dist1 < dist2),
        AS.fact6 << Dist_LSH_RW__LSH_LW(dist3=MATCH.dist3, dist4=MATCH.dist4),
        TEST(lambda dist3, dist4: dist3 < dist4),
        AS.fact7 << direction_type(direct=P(lambda x: x == 0))
    )
    def check4(self):
        # print("This is from the rule")
        value = motion.HAND_CROSSED
        self.set_value_method(value)
        self.rule_matched = True


    @Rule(angle_L_sholder(angle1=P(lambda x: x <40)), angle_L_elbow(angle2=P(lambda x: x >40)),
          angle_R_sholder(angle3=P(lambda x: x <40)), angle_R_elbow(angle4=P(lambda x: x >40)),
         AS.fact3 <<  Dist_Wrists_sholds(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2),
         AS.fact4 <<  Dist_LSH_RW__LSH_LW(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4),
         direction_type(direct = P(lambda x: x == 2 )))
    def check8(self):        
        value =motion.HAND_CROSSED
        self.set_value_method( value)
        self.rule_matched = True
        
        
        
    @Rule(angle_L_sholder(angle1=P(lambda x: x <40)), angle_L_elbow(angle2=P(lambda x: x >40)),
          angle_R_sholder(angle3=P(lambda x: x <40)), angle_R_elbow(angle4=P(lambda x: x >40)),
         AS.fact3 <<  Dist_Wrists_sholds(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2),
         AS.fact4 <<  Dist_LSH_RW__LSH_LW(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4),
         direction_type(direct = P(lambda x: x == 1 )))
    def check9(self):        
        value =motion.HAND_CROSSED
        self.set_value_method( value) 
        self.rule_matched = True





    @Rule( angle_L_sholder(angle1=P(lambda x: x >30)),
           angle_L_elbow(angle2=P(lambda x:  140>x >60)),
           angle_R_sholder(angle3=P(lambda x: x > 30)),
           angle_R_elbow(angle4=P(lambda x:  140>x >60)) ,
         AS.fact5 <<  Dist_Wrists_sholds(dist1 = MATCH.dist1,dist2 =MATCH.dist2),
         TEST(lambda dist1,dist2: dist1 >= dist2),
        #  AS.fact1 <<  Dist_N_LW_LSH(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 > dist2),
        #  AS.fact2 <<  Dist_N_RW_RSH(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 > dist4),
         direction_type(direct = P(lambda x: x == 0)))
    def check3(self):        
        value =motion.HAND_ON_HIP
        self.set_value_method( value)
        self.rule_matched = True

    @Rule(angle_R_sholder(angle3=P(lambda x: x >30)), angle_R_elbow(angle4=P(lambda x:  150>x >60)),
        #  AS.fact5 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 >= dist2),
         AS.fact2 << BodyPart_Rsh_Rw_x(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
         TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos < (Rsh_x_pos + 50)),
         TEST(lambda Rsh_x_pos,Rw_x_pos:( Rsh_x_pos - 50) < Rw_x_pos), 
         direction_type(direct = P(lambda x: x == 1)))
    def check14(self):        
        value =motion.HAND_ON_HIP
        self.set_value_method( value)
        self.rule_matched = True


    @Rule(angle_L_sholder(angle1=P(lambda x: x >30)), angle_L_elbow(angle2=P(lambda x:  150>x >60)),
#          AS.fact5 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 >= dist2),
            AS.fact2 << BodyPart_Lsh_Lw_x(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
            TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos + 20)),
            TEST(lambda Lsh_x_pos,Lw_x_pos:( Lsh_x_pos - 20) < Lw_x_pos), 

         direction_type(direct = P(lambda x: x == 2)))
    def check15(self):        
        value =motion.HAND_ON_HIP
        self.set_value_method( value)  
        self.rule_matched = True

    @Rule (
    direction_type( direct = P(lambda x: x == 1 or x == 2 )  )   
    )
    def check20(self):        
        value =motion.ON_SIDE
        self.set_value_method( value) 
        # print (value )
        self.rule_matched = True



    # @Rule(AS.fact1, NOT(SuccessFact()))    
    # def check19(self):        
    #     value =motion.CORRECT_MOTION
    #     self.set_value_method( value)
    #     self.rule_matched = False






############################################################################333333

    # @Rule(
    # angle(angle1=P(lambda x: x >115)), angle(angle2=P(lambda x: x>115)),
    # AS.fact1 << BodyPart(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
    # AS.fact2 << BodyPart(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
    # TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos < (Rsh_x_pos + 50)),
    # TEST(lambda Rsh_x_pos,Rw_x_pos:( Rsh_x_pos - 50) < Rw_x_pos),
    # TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos + 50)),
    # TEST(lambda Lsh_x_pos,Lw_x_pos:( Lsh_x_pos - 50) < Lw_x_pos),      
    # direction_type(direct = P(lambda x: x == 2)))
    # def check6(self):
    #     value = motion.STRAIGHT_DOWN_LEFT
    #     self.set_value_method(value)    
        
        
    # @Rule(
    # angle(angle1=P(lambda x: x >115)), angle(angle2=P(lambda x: x>115)),
    # AS.fact1 << BodyPart(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
    # AS.fact2 << BodyPart(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
    # TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos < (Rsh_x_pos + 50)),
    # TEST(lambda Rsh_x_pos,Rw_x_pos:( Rsh_x_pos - 50) < Rw_x_pos),
    # TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos + 50)),
    # TEST(lambda Lsh_x_pos,Lw_x_pos:( Lsh_x_pos - 50) < Lw_x_pos),      
    # direction_type(direct = P(lambda x: x == 1)))
    # def check7(self):
    #     value = motion.STRAIGHT_DOWN_RIGHT
    #     self.set_value_method(value)  
        
        
    
        
                

        
      

                


       