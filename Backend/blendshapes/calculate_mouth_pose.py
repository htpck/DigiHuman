import numpy as np
from . import utils
from .facedata import FaceBlendShape, FaceData
from .blendshape_config import BlendShapeConfig
import random
import json



class CalculateMouthPose:

    mouth_pucker_state = True
    mouth_open_close_state = True
    jaw_open_state = True
    mouth_smile_state = True
    mouth_frown_state = True
    mouth_stretch_state = True
    tongue_out_state = False
    jaw_direction_state = True
    mouth_roll_state = True
    mouth_shrug_state = False
    mouth_lower_direction_state = False
    lip_direction_state = True
    mouth_press_state = False
    
    def __init__(self) -> None:
        self.blend_shape_config = BlendShapeConfig()

    def after_init(self, landmarks, normalized_landmarks, face_data: FaceData):
        self.landmarks = landmarks
        self.normalized_landmarks = normalized_landmarks
        self._face_data = face_data
        
    def _get_landmark(self, index: int, use_normalized: bool = False) -> np.array: 
        """ Get the stored landmark from the given index.

        This function converts both the metric and normalized landmarks to a numpy array.

        Parameters
        ----------
        index : int
            Index of the point to get the landmark from.
        use_normalized: bool
            If true, the normalized landmarks are used. Otherwise the metric landmarks are used.

        Returns
        ----------
        np.array
            The landmark in a 3d numpy array.
        """

        landmarks = self.landmarks
        if use_normalized:
            landmarks = self.normalized_landmarks

        if type(landmarks) == np.ndarray:
            # is a 3d landmark
            x = landmarks[index][0]
            y = landmarks[index][1]
            z = landmarks[index][2]
            return np.array([x, y, z])
        else:
            # is a normalized landmark
            x = landmarks[index].x  # * self.image_width
            y = landmarks[index].y  # * self.image_height
            z = landmarks[index].z  # * self.image_height
            return np.array([x, y, z])

    
    PUCKER_THRESHOLD = 0.5

    def calculate_mouth_landmarks(self):
        self.calculate_initial_mouth_landmarks()
        
        if self.mouth_open_close_state:
            self.calculate_mouth_open_close()

        if self.jaw_open_state:
            self.calculate_jaw_open()

        if self.mouth_smile_state:
            self.calculate_mouth_smile()

        if self.mouth_frown_state:
            self.detect_mouth_frown()

        if self.mouth_stretch_state:
            self.calculate_mouth_stretch()
        
        if self.tongue_out_state:
            self.calculate_tongue_out()

        if self.jaw_direction_state:
            self.detect_Jaw_direction(self.nose_tip, self.lowest_chin)

        if self.mouth_roll_state:         
            uppest_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.uppest_lip)
            lowest_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.lowest_lip)
            under_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.under_lip)

            self.detect_Mouth_Roll(self.lower_lip, self.upper_lip, uppest_lip, lowest_lip)
            
        if self.mouth_shrug_state:
            self.calculate_mouth_shrug()

        if self.mouth_lower_direction_state:
            self.detect_mouth_lower_direction(self.mouth_open_dist)

        if self.lip_direction_state:
            self.calculate_lip_direction()
            
        if self.mouth_pucker_state: 
            self.calculate_pucker_ratio()

        if self.mouth_press_state:
            self.detect_mouth_press()
            
        self.cheek_puff_detect()
    
    #################CALCULATE-SIDE#####################
   
    def calculate_initial_mouth_landmarks(self):
        self.upper_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.upper_lip)
        self.upper_outer_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.upper_outer_lip)
        self.lower_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.lower_lip)
        self.mouth_corner_left = self._get_landmark(self.blend_shape_config.CanonicalPoints.mouth_corner_left)
        self.mouth_corner_right = self._get_landmark(self.blend_shape_config.CanonicalPoints.mouth_corner_right)
        self.lowest_chin = self._get_landmark(self.blend_shape_config.CanonicalPoints.lowest_chin)
        self.nose_tip = self._get_landmark(self.blend_shape_config.CanonicalPoints.nose_tip)
        self.upper_head = self._get_landmark(self.blend_shape_config.CanonicalPoints.upper_head)
        self.tongue_out = self._get_landmark(self.blend_shape_config.CanonicalPoints.tongue_out)
        


        self.mouth_width = utils.dist(self.mouth_corner_left, self.mouth_corner_right)
        self.mouth_center = (self.upper_lip + self.lower_lip) / 2
        self.mouth_open_dist = utils.dist(self.upper_lip, self.lower_lip)
        self.mouth_center_nose_dist = utils.dist(self.mouth_center, self.nose_tip)
        self.jaw_open_dist = utils.dist(self.lowest_chin, self.nose_tip)
        
        # with open('jaw_open_dist.json', 'a') as f:
        #     json.dump(
                
        #         {'jaw_open_dist':self.jaw_open_dist }
                
        #         , f)
        #     f.write('\n')
            
        
        #utils.dist(self.nose_tip, self._get_landmark(152))
    
    def calculate_pucker_ratio(self):
        self.detect_mouth_pucker(self.mouth_width, self.mouth_open_dist * 18)   
    
    def calculate_mouth_open_close(self):
        mouth_open = 0
        # with open('mouth_position.json', 'a') as f:
        #     json.dump(
                
        #         {'mouth_width':self.mouth_width, "mouth_open_dist": self.mouth_open_dist,'mouth_center_nose_dist': self.mouth_center_nose_dist }
                
        #         , f)
        #     f.write('\n')
        #mouth_close = utils._remap_blendshape(FaceBlendShape.MouthClose, self.mouth_center_nose_dist - self.mouth_open_dist)
        if self.jaw_open_dist > 9.15:
            mouth_open = utils._remap_blendshape(FaceBlendShape.MouthOpen, self.mouth_open_dist/self.mouth_width) #mouth aspect ratio
            if((self.mouth_width <= 4.5 and self.mouth_open_dist <= 0.5)):
                mouth_open *= 0.01
                
        self._face_data.set_blendshape(FaceBlendShape.MouthOpen, mouth_open)
        #self._face_data.set_blendshape(FaceBlendShape.MouthClose, mouth_close)
        #write json file data here
        
    def calculate_jaw_open(self):
        jaw_nose_dist = utils.dist(self.lowest_chin, self.nose_tip)
        head_height = utils.dist(self.upper_head, self.lowest_chin)
        jaw_open_ratio = jaw_nose_dist / head_height

        jaw_open = utils._remap_blendshape(FaceBlendShape.JawOpen, jaw_open_ratio)

        # if(self.pucker_ratio > self.PUCKER_THRESHOLD):
        #     jaw_open *= 0.2

        self._face_data.set_blendshape(FaceBlendShape.JawOpen, jaw_open)

    def calculate_mouth_smile(self):
        self.mouth_smile_left, self.mouth_smile_right = self.detect_smile(
            self.upper_lip, self.mouth_corner_left, self.mouth_corner_right)

    def calculate_mouth_stretch(self):
        self.mouth_left, self.mouth_right = self.detect_mouth_Stretch(
            self.mouth_center, self.mouth_corner_left, self.mouth_corner_right,
            self.mouth_smile_left, self.mouth_smile_right)
  
    def calculate_tongue_out(self):  
        tongue_out_value = random.uniform(0, 1) 
        self._face_data.set_blendshape(FaceBlendShape.TongueOut, tongue_out_value)

    def calculate_mouth_shrug(self):
        uppest_lip = self._get_landmark(0)
        lowest_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.lowest_lip)
        under_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.under_lip)
        self.detect_mouth_shrug(self.nose_tip, uppest_lip, lowest_lip)

    def calculate_lip_direction(self):
        # lower lip direction
        self.calculate_lip_direction_helper("lower")
        # upper lip direction
        self.calculate_lip_direction_helper("upper")

    def calculate_lip_direction_helper(self, lip_side, state=True): 
        #detect corners lip direction
        # self.detect_lip_direction(mouth_open,mouth_left,mouth_right)
        
        if state == False:
            self._face_data.set_blendshape(FaceBlendShape.LipLowerDownLeft, 0)
            self._face_data.set_blendshape(FaceBlendShape.LipLowerDownRight, 0)
            return
        
        write_json = {
            "lower_lip_dist_left_f": 0,
            "lower_lip_dist_right_f": 0,
            "upper_lip_dist_left_f": 0,
            "upper_lip_dist_right_f": 0,
        }
        
        #lower lip
        if lip_side == "lower":
            lower_down_left = utils.dist(self._get_landmark(
                321), self._get_landmark(395))
            lower_down_left2 = utils.dist(self._get_landmark(
                321), self._get_landmark(364))

            lower_down_right = utils.dist(self._get_landmark(
                91), self._get_landmark(170))
            lower_down_right2 = utils.dist(self._get_landmark(
                91), self._get_landmark(135))


            lower_down_left_final = 1 - utils._remap_blendshape(FaceBlendShape.LipLowerDownLeft, (lower_down_left + lower_down_left2)/2.0)
            lower_down_right_final = 1 - utils._remap_blendshape(FaceBlendShape.LipLowerDownRight,(lower_down_right + lower_down_right2)/2.0)
            self._face_data.set_blendshape(FaceBlendShape.LipLowerDownLeft, lower_down_left_final)
            self._face_data.set_blendshape(FaceBlendShape.LipLowerDownRight, lower_down_right_final)
            
            write_json["lower_lip_dist_left_f"] = (lower_down_left + lower_down_left2)/2.0
            write_json["lower_lip_dist_right_f"] = (lower_down_right + lower_down_right2)/2.0
            

        # upper lip
        if lip_side == "upper":
            upper_up_left = utils.dist(self._get_landmark(
                270), self._get_landmark(425))
            upper_up_left2 = utils.dist(self._get_landmark(
                270), self._get_landmark(266))

            upper_up_right = utils.dist(self._get_landmark(
                40), self._get_landmark(205))
            upper_up_right2 = utils.dist(self._get_landmark(
                40), self._get_landmark(36))

            upper_up_left_final = 1 - utils._remap_blendshape(FaceBlendShape.LipUpperUpLeft, (upper_up_left + upper_up_left2)/2.0)
            upper_up_right_final = 1 - utils._remap_blendshape(FaceBlendShape.LipUpperUpRight,(upper_up_right + upper_up_right2)/2.0)
            self._face_data.set_blendshape(FaceBlendShape.LipUpperUpLeft, upper_up_left_final)
            self._face_data.set_blendshape(FaceBlendShape.LipUpperUpRight, upper_up_right_final)
            
            write_json["upper_lip_dist_left_f"] = (upper_up_left + upper_up_left2)/2.0
            write_json["upper_lip_dist_right_f"] = (upper_up_right + upper_up_right2)/2.0
            
        
        with open('lip_direction.json', 'a') as f:
            json.dump(write_json, f)
            f.write('\n')


        # really hard to do this, mediapipe is not really moving here
        # right_under_eye = self._get_landmark(350)
        # nose_sneer_right_dist = utils.dist(nose_tip, right_under_eye)
        # print(nose_sneer_right_dist)
        # same with cheek puff
    
    ###################DETECT-SIDE#####################
    
    def detect_smile(self,upper_lip,mouth_corner_left,mouth_corner_right):
        # Smile
        # TODO mouth open but teeth closed
        smile_left = upper_lip[1] - mouth_corner_left[1]
        smile_right = upper_lip[1] - mouth_corner_right[1]

        mouth_smile_left = 1 - \
                            utils._remap_blendshape(FaceBlendShape.MouthSmileLeft, smile_left)
        mouth_smile_right = 1 - \
                            utils._remap_blendshape(FaceBlendShape.MouthSmileRight, smile_right)

        # print(mouth_smile_right)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthSmileLeft, mouth_smile_left)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthSmileRight, mouth_smile_right)
        # ------------------------------------------------

        #Extra
        self._face_data.set_blendshape(
            FaceBlendShape.MouthDimpleLeft, mouth_smile_left / 2)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthDimpleRight, mouth_smile_right / 2)

        return mouth_smile_left,mouth_smile_right

    def detect_mouth_frown(self):
        #mouth frown
        mouth_frown_left = \
        (self.mouth_corner_left - self._get_landmark(self.blend_shape_config.CanonicalPoints.mouth_frown_left))[1]
        mouth_frown_right = \
        (self.mouth_corner_right - self._get_landmark(self.blend_shape_config.CanonicalPoints.mouth_frown_right))[1]

        mouth_frown_left_final = 1 - utils._remap_blendshape(FaceBlendShape.MouthFrownLeft, mouth_frown_left)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthFrownLeft, mouth_frown_left_final)

        mouth_frown_right_final = 1 - utils._remap_blendshape(FaceBlendShape.MouthFrownRight, mouth_frown_right)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthFrownRight,
            mouth_frown_right_final)
        #-------------------------------------------------

    def detect_mouth_Stretch(self,mouth_center,mouth_corner_left,mouth_corner_right,mouth_smile_left,mouth_smile_right):
        #mouth is stretched left or right

        # todo: also strech when laughing, need to be fixed


        upper_nose = self._get_landmark(self.blend_shape_config.CanonicalPoints.upper_nose)

        # only interested in the axis coordinates here

        # mouth_center_left_stretch = mouth_center[0] - mouth_left_stretch_point[0]
        # mouth_center_right_stretch = mouth_center[0] - mouth_right_stretch_point[0]

        stretch = mouth_center[0] - upper_nose[0]

        mouth_left = utils._remap_blendshape(
            FaceBlendShape.MouthLeft, stretch)
        mouth_right = 1 - \
                      utils._remap_blendshape(FaceBlendShape.MouthRight,
                                             stretch)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthLeft, mouth_left)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthRight, mouth_right)

        print(mouth_left)

        # self._live_link_face.set_blendshape(ARKitFace.MouthRight, 1 -7 remap(mouth_left_right, -1.5, 0.0))
        #-------------------------------------------------------

        #Extra
        mouth_left_stretch_point = self._get_landmark(self.blend_shape_config.CanonicalPoints.mouth_left_stretch)
        mouth_right_stretch_point = self._get_landmark(self.blend_shape_config.CanonicalPoints.mouth_right_stretch)

        # only interested in the axis coordinates here
        mouth_left_stretch = mouth_corner_left[0] - mouth_left_stretch_point[0]
        mouth_right_stretch = mouth_right_stretch_point[0] - mouth_corner_right[0]

        stretch_normal_left = -0.7 + \
                              (0.42 * mouth_smile_left) + (0.36 * mouth_left)
        stretch_max_left = -0.45 + \
                           (0.45 * mouth_smile_left) + (0.36 * mouth_left)

        stretch_normal_right = -0.7 + 0.42 * \
                               mouth_smile_right + (0.36 * mouth_right)
        stretch_max_right = -0.45 + \
                            (0.45 * mouth_smile_right) + (0.36 * mouth_right)


        mouth_left_stretch_final = utils._remap(mouth_left_stretch, stretch_normal_left, stretch_max_left)
        self._face_data.set_blendshape(FaceBlendShape.MouthStretchLeft, mouth_left_stretch_final)

        mouth_right_stretch_final = utils._remap(mouth_right_stretch, stretch_normal_right, stretch_max_right)
        self._face_data.set_blendshape(FaceBlendShape.MouthStretchRight, mouth_right_stretch_final)

        return mouth_left, mouth_right
    # when your mouth roll and shrink this will be near to 1
    def detect_Mouth_Roll(self,lower_lip,upper_lip,upper_outer_lip,lowest_lip):

        lower_lip_dist = utils.dist(lower_lip, lowest_lip)
        upper_lip_dist = utils.dist(upper_lip, upper_outer_lip)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthRollLower, 1 - utils._remap_blendshape(FaceBlendShape.MouthRollLower, lower_lip_dist))
        self._face_data.set_blendshape(
            FaceBlendShape.MouthRollUpper, 1 - utils._remap_blendshape(FaceBlendShape.MouthRollUpper, upper_lip_dist))

        # with open('mouth_roll_position.json', 'a') as f:
        #     json.dump(
                
        #         {
        #             'lower_lip_dist':lower_lip_dist,
        #             "reel_lower_lip_dist": 1 - utils._remap_blendshape(FaceBlendShape.MouthRollLower, lower_lip_dist),
        #             "upper_lip_dist": upper_lip_dist,
        #             "reel_upper_lip_dist": 1 - utils._remap_blendshape(FaceBlendShape.MouthRollUpper, upper_lip_dist),
        #         }
                
        #         , f)
        #     f.write('\n')

    def detect_Jaw_direction(self,nose_tip,lowest_chin):
        #Jaw left right
        # jaw only interesting on x yxis
        jaw_right_left = nose_tip[0] - lowest_chin[0]

        # TODO: this is not face rotation resistant
        jaw_left = 1 - utils._remap_blendshape(FaceBlendShape.JawLeft, jaw_right_left)
        self._face_data.set_blendshape(
            FaceBlendShape.JawLeft, jaw_left)

        jaw_right = utils._remap_blendshape(FaceBlendShape.JawRight, jaw_right_left)
        self._face_data.set_blendshape(FaceBlendShape.JawRight, jaw_right)
        #-------------------------------

    # will appear in the time of mouth press(when you hide your lips by pulling it inside your mouth!)
    def detect_mouth_press(self):
        left_upper_press = utils.dist(
            self._get_landmark(self.blend_shape_config.CanonicalPoints.left_upper_press[0]),
            self._get_landmark(self.blend_shape_config.CanonicalPoints.left_upper_press[1])
        )
        left_lower_press = utils.dist(
            self._get_landmark(self.blend_shape_config.CanonicalPoints.left_lower_press[0]),
            self._get_landmark(self.blend_shape_config.CanonicalPoints.left_lower_press[1])
        )
        mouth_press_left = (left_upper_press + left_lower_press) / 2

        right_upper_press = utils.dist(
            self._get_landmark(self.blend_shape_config.CanonicalPoints.right_upper_press[0]),
            self._get_landmark(self.blend_shape_config.CanonicalPoints.right_upper_press[1])
        )
        right_lower_press = utils.dist(
            self._get_landmark(self.blend_shape_config.CanonicalPoints.right_lower_press[0]),
            self._get_landmark(self.blend_shape_config.CanonicalPoints.right_lower_press[1])
        )
        mouth_press_right = (right_upper_press + right_lower_press) / 2

        mouth_press_left_final = 1 - utils._remap_blendshape(FaceBlendShape.MouthPressLeft, mouth_press_left)
        mouth_press_right_final = 1 - utils._remap_blendshape(FaceBlendShape.MouthPressRight, mouth_press_right)

        # print(mouth_press_left_final)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthPressLeft, mouth_press_left_final)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthPressRight,
            mouth_press_right_final
            )

    #will appear when your whole mouth goes to corner left down or right direction
    def detect_mouth_lower_direction(self,mouth_open_dist):
        lower_down_left = utils.dist(self._get_landmark(
            424), self._get_landmark(319)) + mouth_open_dist * 0.5
        lower_down_right = utils.dist(self._get_landmark(
            204), self._get_landmark(89)) + mouth_open_dist * 0.5

        lower_down_left_final = 1 - utils._remap_blendshape(FaceBlendShape.MouthLowerDownLeft, lower_down_left)
        lower_down_right_final = 1 -utils._remap_blendshape(FaceBlendShape.MouthLowerDownRight,lower_down_right)
        # print(utils.dist(self._get_landmark(
        #     424), self._get_landmark(319)))
        self._face_data.set_blendshape(FaceBlendShape.MouthLowerDownLeft, lower_down_left_final)
        self._face_data.set_blendshape(FaceBlendShape.MouthLowerDownRight, lower_down_right_final)
    
    #will appear when your quarter of your mouth(left_up_lip, left _down_lip,right_up_lip,right_down_lip) turns more to its corner
    def detect_lip_direction(self,mouth_open_dist,mouth_left,mouth_right):
        lower_down_left = utils.dist(self._get_landmark(
            424), self._get_landmark(319))
        lower_down_right = utils.dist(self._get_landmark(
            204), self._get_landmark(89, self._metric_landmarks, self._normalized_landmarks))

        lower_down_left_lip = 1 - utils._remap_blendshape(FaceBlendShape.LipLowerDownLeft, lower_down_left)
        lower_down_right_final = 1 -utils._remap_blendshape(FaceBlendShape.LipLowerDownRight,lower_down_right)
        # print(lower_down_left + (mouth_open_dist - mouth_left))
        self._face_data.set_blendshape(FaceBlendShape.LipLowerDownLeft, lower_down_left_lip)
        self._face_data.set_blendshape(FaceBlendShape.LipLowerDownRight, lower_down_right_final)

    def detect_mouth_shrug(self,nose_tip,uppest_lip,lowest_lip):
        #mouth shrug up will be near 1 if upper mouth is near nose!
        upper_lip_nose_dist = nose_tip[1] - uppest_lip[1]
        mouth_shrug_upper = 1 - utils._remap_blendshape(FaceBlendShape.MouthShrugUpper, upper_lip_nose_dist)
        self._face_data.set_blendshape(FaceBlendShape.MouthShrugUpper,mouth_shrug_upper)

        over_upper_lip = self._get_landmark(self.blend_shape_config.CanonicalPoints.over_upper_lip)
        mouth_shrug_lower = utils.dist(lowest_lip, over_upper_lip)

        #not good
        mouth_shrug_lower_final = 1 - utils._remap_blendshape(FaceBlendShape.MouthShrugLower, mouth_shrug_lower)
        self._face_data.set_blendshape(
            FaceBlendShape.MouthShrugLower,mouth_shrug_lower_final)

        #------------------------------------------------------------------

    def detect_mouth_pucker(self, mouth_width, mouth_open_dist):
        # Use descriptive variable names and avoid magic numbers
        min_mouth_width = 4.6
        min_mouth_open_dist = 25
        min_mouth_pucker_width = 4.5
        min_mouth_pucker_open_dist = 5

        # Initialize the mouth pucker value to zero
        mouth_pucker = 0.0
        
        # Check if the mouth is funneling (narrow and open)
        if mouth_width <= min_mouth_width and mouth_open_dist > min_mouth_open_dist:
            # Remap the mouth width to a value between 0 and 1
            mapped_value = 1 - utils._remap_blendshape(FaceBlendShape.MouthFunnel, mouth_width)
            
            # Calculate the average of the mapped value and the mouth open distance
            average = np.average([mapped_value, mouth_open_dist])
            
            # Remap the average to a value between 0 and 1
            mapped_value_funnel = utils._remap_blendshape(FaceBlendShape.MouthFunnel, average)
            
            # Set the blendshape for the mouth funnel to the mapped value
            self._face_data.set_blendshape(FaceBlendShape.MouthFunnel, mapped_value_funnel)
            
            # Set the blendshape for the mouth pucker to zero
            self._face_data.set_blendshape(FaceBlendShape.MouthPucker, 0.0)
            
            # Return from the function
            return
        else:
            # Set the blendshape for the mouth funnel to zero
            self._face_data.set_blendshape(FaceBlendShape.MouthFunnel, 0)
        
        # Check if the mouth is not puckering (wide and open)
        if mouth_width > min_mouth_pucker_width and mouth_open_dist > min_mouth_pucker_open_dist:
            # Set the blendshape for the mouth pucker to zero
            self._face_data.set_blendshape(FaceBlendShape.MouthPucker, 0.0)
        else:
            # Remap the ratio of the mouth open distance and width to a value between 0 and 1
            mouth_pucker = utils._remap_blendshape(
                FaceBlendShape.MouthPucker, mouth_open_dist / mouth_width)
            
            # Set the blendshape for the mouth pucker to the remapped value
            self._face_data.set_blendshape(
                FaceBlendShape.MouthPucker, mouth_pucker)
            
            # If the mouth pucker is more than half, calculate the lip direction for upper and lower lips
            if mouth_pucker > 0.5:
                self.calculate_lip_direction_helper("lower", False)
                self.calculate_lip_direction_helper("upper", False)  

    def cheek_puff_detect(self):
            # Use descriptive variable names and avoid magic numbers
            left_cheek_index = 213
            right_cheek_index = 433
            upper_lip_index = 13
            lower_lip_index = 14
            left_mouth_corner_index = 61
            right_mouth_corner_index = 291
            nose_tip_index = 1
            chin_index = 17
            

            # The minimum and maximum distance between the left and right cheeks
            min_cheek_distance = 2.50
            max_cheek_distance = 3.45

            # The minimum and maximum distance between the upper and lower lips
            min_lip_distance = 0
            max_lip_distance = 2

            # The minimum and maximum distance between the mouth corners
            min_mouth_corner_distance = 4.2
            max_mouth_corner_distance = 5.7
            
            # The minimum and maximum distance between the nose tip and the chin
            min_nose_chin_distance = 3.5
            max_nose_chin_distance = 5.5


            # Get the landmarks for the left and right cheeks, upper and lower lips, and mouth corners
            left_cheek = self._get_landmark(left_cheek_index)        
            right_cheek = self._get_landmark(right_cheek_index)
            upper_lip = self._get_landmark(upper_lip_index)
            lower_lip = self._get_landmark(lower_lip_index)
            left_mouth_corner = self._get_landmark(left_mouth_corner_index)
            right_mouth_corner = self._get_landmark(right_mouth_corner_index)
            nose_tip = self._get_landmark(nose_tip_index)
            chin = self._get_landmark(chin_index)

            # Calculate the distance between the cheeks, lips, and mouth corners
            cheek_distance = utils.dist(left_cheek, right_cheek)
            lip_distance = utils.dist(upper_lip, lower_lip)
            mouth_corner_distance = utils.dist(left_mouth_corner, right_mouth_corner)
            nose_chin_distance = utils.dist(nose_tip, chin)


            
            # Map the distances to values between 0 and 1
            cheek_value = utils.map_value(cheek_distance, min_cheek_distance, max_cheek_distance, 0, 1)
            lip_value = 1 - utils.map_value(lip_distance * 9, min_lip_distance, max_lip_distance, 0, 1) if lip_distance < 0.05 else 0
            mouth_corner_value = 1 - utils.map_value(mouth_corner_distance, min_mouth_corner_distance, max_mouth_corner_distance, 0, 1) if mouth_corner_distance < 5.5 else 0
            nose_chin_value =  1 - utils.map_value(nose_chin_distance, min_nose_chin_distance, max_nose_chin_distance, 0, 1)

            
            #Actually I use different purpose _lerp function just for cheek puff
            #jaw_open_dist_interp = utils._lerp(jaw_open_dist, min_jaw_open_dist, max_jaw_open_dist)
            
            # Calculate the cheek puff value as a weighted average of the three values
            cheek_puff_value_avg = (cheek_value *0.5 + mouth_corner_value  + nose_chin_value * 5 if cheek_distance > 12.70 and nose_chin_value > 0.58 else nose_chin_value * 8  ) / 3
            
            if lip_distance > 0.2:
                cheek_puff_value_avg = 0
            
            # Map the cheek puff value to a blendshape value
            cheek_puff_value = utils._remap_blendshape(FaceBlendShape.CheekPuff, cheek_puff_value_avg)
            
            # Set the blendshape for the cheek puff
            self._face_data.set_blendshape(FaceBlendShape.CheekPuff, cheek_puff_value)
            
            
            with open('deneme3.json', 'a') as f:
                json.dump(
                    
                    {
                        'cheek_distance': cheek_distance,
                        'mouth_corner_distance': mouth_corner_distance,
                        'mouth_corner_value': mouth_corner_value,
                        'nose_chin_distance': nose_chin_distance,
                        'nose_chin_value': nose_chin_value,
                        'lip_distance': lip_distance,
                        'avarage': cheek_puff_value,
                        # 'is_cheek_movement': True if cheek_puff_value > 0 else False,
                    }
                    
                    , f)
                f.write('\n')
