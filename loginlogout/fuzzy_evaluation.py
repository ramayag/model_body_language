import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def total_evaluation_using_fuzzy_sys(array) : 
    # Define fuzzy variables
    #input
    HAND_ON_HIP = ctrl.Antecedent(np.arange(0, 11, 1), 'HAND_ON_HIP')
    HAND_CROSSED  = ctrl.Antecedent(np.arange(0, 11, 1), 'HAND_CROSSED')
    STRAIGHT_DOWN = ctrl.Antecedent(np.arange(0, 11, 1), 'STRAIGHT_DOWN')
    HAND_ON_HEAD = ctrl.Antecedent(np.arange(0, 11, 1), 'HAND_ON_HEAD')
    CLOSED_U_HANDS = ctrl.Antecedent(np.arange(0, 11, 1), 'CLOSED_U_HANDS')
    CLOSED_D_HANDS = ctrl.Antecedent(np.arange(0, 11, 1), 'CLOSED_D_HANDS')
    HANDS_OUT_BOX = ctrl.Antecedent(np.arange(0, 11, 1),'HANDS_OUT_BOX')
    ON_SIDE = ctrl.Antecedent(np.arange(0, 11, 1), 'ON_SIDE')
    CORRECT_MOTION  = ctrl.Antecedent(np.arange(0, 11, 1), 'CORRECT_MOTION')
    VIBRATING_MOTION =ctrl.Antecedent(np.arange(0, 11, 1), 'VIBRATING_MOTION')

    #output
    RESULT = ctrl.Consequent(np.arange(0, 11, 1), 'RESULT')


    # membership functions for each input variable

    HAND_ON_HIP['low'] = fuzz.trimf(HAND_ON_HIP.universe, [0, 0, 4])
    HAND_ON_HIP['medium'] = fuzz.trimf(HAND_ON_HIP.universe, [3, 5, 7])
    HAND_ON_HIP['high'] = fuzz.trimf(HAND_ON_HIP.universe, [6, 10, 10])

    HAND_CROSSED['low'] = fuzz.trimf(HAND_CROSSED.universe, [0, 0, 4])
    HAND_CROSSED['medium'] = fuzz.trimf(HAND_CROSSED.universe, [3, 5, 7])
    HAND_CROSSED['high'] = fuzz.trimf(HAND_CROSSED.universe, [6, 10, 10])

    STRAIGHT_DOWN['low'] = fuzz.trimf(STRAIGHT_DOWN.universe, [0, 0, 4])
    STRAIGHT_DOWN['medium'] = fuzz.trimf(STRAIGHT_DOWN.universe, [3, 5, 7])
    STRAIGHT_DOWN['high'] = fuzz.trimf(STRAIGHT_DOWN.universe, [6, 10, 10])

    HAND_ON_HEAD['low'] = fuzz.trimf(HAND_ON_HEAD.universe, [0, 0, 4])
    HAND_ON_HEAD['medium'] = fuzz.trimf(HAND_ON_HEAD.universe, [3, 5, 7])
    HAND_ON_HEAD['high'] = fuzz.trimf(HAND_ON_HEAD.universe, [6, 10, 10])

    CLOSED_U_HANDS['low'] = fuzz.trimf(CLOSED_U_HANDS.universe, [0, 0, 4])
    CLOSED_U_HANDS['medium'] = fuzz.trimf(CLOSED_U_HANDS.universe, [3, 5, 7])
    CLOSED_U_HANDS['high'] = fuzz.trimf(CLOSED_U_HANDS.universe, [6, 10, 10])

    CLOSED_D_HANDS['low'] = fuzz.trimf(CLOSED_D_HANDS.universe, [0, 0, 4])
    CLOSED_D_HANDS['medium'] = fuzz.trimf(CLOSED_D_HANDS.universe, [3, 5, 7])
    CLOSED_D_HANDS['high'] = fuzz.trimf(CLOSED_D_HANDS.universe, [6, 10, 10])

    HANDS_OUT_BOX['low'] = fuzz.trimf(HANDS_OUT_BOX.universe, [0, 0, 4])
    HANDS_OUT_BOX['medium'] = fuzz.trimf(HANDS_OUT_BOX.universe, [3, 5, 7])
    HANDS_OUT_BOX['high'] = fuzz.trimf(HANDS_OUT_BOX.universe, [6, 10, 10])

    ON_SIDE['low'] = fuzz.trimf(ON_SIDE.universe, [0, 0, 4])
    ON_SIDE['medium'] = fuzz.trimf(ON_SIDE.universe, [3, 5, 7])
    ON_SIDE['high'] = fuzz.trimf(ON_SIDE.universe, [6, 10, 10])

    CORRECT_MOTION['low'] = fuzz.trimf(CORRECT_MOTION.universe, [0, 0, 4])
    CORRECT_MOTION['medium'] = fuzz.trimf(CORRECT_MOTION.universe, [3, 5, 7])
    CORRECT_MOTION['high'] = fuzz.trimf(CORRECT_MOTION.universe, [6, 10, 10])

    VIBRATING_MOTION['low'] = fuzz.trimf(HAND_ON_HIP.universe, [0, 0, 4])
    VIBRATING_MOTION['medium'] = fuzz.trimf(HAND_ON_HIP.universe, [3, 5, 7])
    VIBRATING_MOTION['high'] = fuzz.trimf(HAND_ON_HIP.universe, [6, 10, 10])


    # output membership
    RESULT['bad'] = fuzz.trimf(RESULT.universe, [0, 0, 2])
    RESULT['accept'] = fuzz.trimf(RESULT.universe, [1, 2, 4])
    RESULT['good'] = fuzz.trimf(RESULT.universe, [2, 4, 6])
    RESULT['very_good'] = fuzz.trimf(RESULT.universe, [5, 7, 8])
    RESULT['excellent'] = fuzz.trimf(RESULT.universe, [7, 10, 10])

    # Define fuzzy rules

    rule1 = ctrl.Rule(CORRECT_MOTION['high'], RESULT['excellent'])

    # #rule2 = ctrl.Rule(CORRECT_MOTION['high'] & 
    #                   (HAND_ON_HEAD['medium'] | 
    #                   CLOSED_D_HANDS['medium'] |
    #                   HANDS_OUT_BOX['medium']  |
    #                   HAND_ON_HIP['medium'] )       
    #                   , RESULT['very_good'])

    rule3 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['low']) & 
                    (CLOSED_D_HANDS['low']) &
                    (HANDS_OUT_BOX['low'] ) &
                    (HAND_ON_HIP['low'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )       
                    , RESULT['very_good'])
    ############################
    rule4 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['good'])

    rule5 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['good'])

    rule6 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['good'])

    rule7 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['good'])
    ###########################

    rule8 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['high']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['accept'])

    rule9 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['high'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['accept'])

    rule10 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['high'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['accept'])

    rule11 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['high'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['accept'])
    ##############################

    rule12 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['low'] ) &  
                    (CLOSED_D_HANDS['low'] ) &
                    (HANDS_OUT_BOX['low'] ) &
                    (HAND_ON_HIP['low'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['good'])
    #######################

    rule13 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['accept'])

    rule14 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['accept'])

    rule15 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['accept'])

    rule16 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) &  
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['accept'])
    ############################


    rule17 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['high']) & 
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['bad'])

    rule18 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) & 
                    (CLOSED_D_HANDS['high']) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['bad'])

    rule19 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) & 
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['high'] ) &
                    (HAND_ON_HIP['low'] | HAND_ON_HIP['medium'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['bad'])

    rule20 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (HAND_ON_HEAD['low'] | HAND_ON_HEAD['medium']) & 
                    (CLOSED_D_HANDS['low'] | CLOSED_D_HANDS['medium'] ) &
                    (HANDS_OUT_BOX['low'] | HANDS_OUT_BOX['medium'] ) &
                    (HAND_ON_HIP['high'] ) &
                    (VIBRATING_MOTION['low'] | VIBRATING_MOTION['medium'] )&
                    (ON_SIDE['low'] | ON_SIDE['medium'] ) &
                    (HAND_CROSSED['low'] | HAND_CROSSED['medium'] ) &
                    (STRAIGHT_DOWN['low'] | STRAIGHT_DOWN['medium'] ) &
                    (CLOSED_U_HANDS['low'] | CLOSED_U_HANDS['medium'] )
                    
                    , RESULT['bad'])


    ############################

    rule21 = ctrl.Rule(CORRECT_MOTION['low'] & 
                    (ON_SIDE['high'] | 
                    HAND_CROSSED['high'] | 
                    STRAIGHT_DOWN['high'] |
                    VIBRATING_MOTION['high'] | 
                    CLOSED_U_HANDS['high'] )
                    
                    , RESULT['bad'])

    rule22 = ctrl.Rule(CORRECT_MOTION['medium'] & 
                    (ON_SIDE['high'] | 
                    HAND_CROSSED['high'] | 
                    STRAIGHT_DOWN['high'] |
                    VIBRATING_MOTION['high'] | 
                    CLOSED_U_HANDS['high']) 
                    
                    , RESULT['accept'])
                    
    ###################################################
    # Create control system and attach rules

    default_prediction_ctrl = ctrl.ControlSystem([
        rule1,rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
        rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19,
        rule20, rule21, rule22,
    ])

    res = ctrl.ControlSystemSimulation(default_prediction_ctrl)


    # Set input values
    # res.input['CORRECT_MOTION'] = array['CORRECT_MOTION']
    # res.input['HAND_ON_HIP'] = array['HAND_ON_HIP']
    # res.input['HAND_CROSSED'] = array['HAND_CROSSED']
    # res.input['STRAIGHT_DOWN'] =array['STRAIGHT_DOWN']
    # res.input['HAND_ON_HEAD'] = array['HAND_ON_HEAD']
    # res.input['CLOSED_U_HANDS'] = array['CLOSED_U_HANDS']
    # res.input['CLOSED_D_HANDS'] = array['CLOSED_D_HANDS']
    # res.input['HANDS_OUT_BOX'] = array['HANDS_OUT_BOX']
    # res.input['ON_SIDE'] = array['HAND_ON_HIP']
    # res.input['VIBRATING_MOTION'] = array['PERIODICAL']

    # Set input values
    for motion, count in array.items():
            res.input[motion] = count
            # print(motion)
                    
    # Compute the result
    res.compute()
    result = res.output['RESULT']
    # print("RESULT: ", result)
    return result


# RESULT.view(sim=res)