import numpy as np
from .facedata import FaceBlendShape, FaceData
from .blendshape_config import BlendShapeConfig
from . import utils
from .calculate_head_pose import CalculateHeadPose


class CalculateEyePose:
    eye_close = False
    pupil_movement_isThreshold = True 
    eye_pupil_state = {
        "LEFT": False,
        "RIGHT": False,
        "UP": False,
        "DOWN": False
    }
    def __init__(self) -> None:
        self.blend_shape_config = BlendShapeConfig()

    def after_init(self, landmarks, normalized_landmarks, calculate_head_pose: CalculateHeadPose, face_data: FaceData):
        self.landmarks = landmarks
        self.normalized_landmarks = normalized_landmarks
        self._calculate_head_pose = calculate_head_pose
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
    def calculate_eye_landmarks(self):
        if not self.eye_close and self.pupil_movement_isThreshold:
            # Pupil Position
            self.calculate_pupil_positions()

            # Eye Pupil State
            self.calculate_eye_pupil_state()

            # Face BlendShape
            self.set_face_blendshape()

            # Eye Squint
            self.calculate_eye_squint()

            # Brow and Cheek Actions
            self.detect_brow_actions()
            self.detect_cheek()
            
    def calculate_pupil_positions(self):
        self.right_pupil_pos = self._pupil_position("RIGHT")
        self.left_pupil_pos = self._pupil_position("LEFT")
        
        self.eye_in_left = self.left_pupil_pos[0]
        self.eye_in_right = self._lerp(self.right_pupil_pos[0], 1.21, 2)
        
        self.eye_out_left = self._lerp(self.left_pupil_pos[0], 1.21, 2)
        self.eye_out_right = self.right_pupil_pos[0]
        
        self.eye_down_left = self.left_pupil_pos[1]
        self.eye_down_right = self.right_pupil_pos[1]
        
        self.eye_up_right = self._lerp(self.right_pupil_pos[1], 1.21, 1.5)
        self.eye_up_left = self._lerp(self.right_pupil_pos[1], 1.21, 1.5)

    def calculate_eye_pupil_state(self):
        self.eye_down_left, self.eye_down_right = self.adjust_eye_direction_levels(self.eye_down_left, self.eye_down_right)
        self.eye_up_right, self.eye_up_left = self.adjust_eye_direction_levels(self.eye_up_right, self.eye_up_left)

        self.eye_pupil_state = {
            "LEFT": self.eye_out_left > 3.25 and self.eye_in_right > 3.25,
            "RIGHT": self.eye_in_left > 1.00 and self.eye_out_right > 1.00,
            "DOWN": self.eye_down_left > -1.30 and self.eye_down_right > -1.30,
            "UP": self.eye_up_left > 3.20 and self.eye_up_right > 3.20,
        }

        if self.eye_pupil_state["DOWN"]:
            if self.eye_out_left > 2.80 and self.eye_in_right > 2.80:
                self.eye_out_left *= 1.2
                self.eye_in_right *= 1.2
    
    def adjust_eye_direction_levels(self, eye_direction_left, eye_direction_right):
        if abs(eye_direction_left - eye_direction_right) > 0.10:
            max_value = max(eye_direction_left, eye_direction_right)
            eye_direction_left = eye_direction_right = max_value
        
        return eye_direction_left, eye_direction_right

    def set_face_blendshape(self):
        self._face_data.set_blendshape(FaceBlendShape.EyeLookOutRight, utils._remap_blendshape(FaceBlendShape.EyeLookOutRight, self.eye_in_left))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookUpRight, utils._remap_blendshape(FaceBlendShape.EyeLookUpRight, self.eye_in_right))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookDownLeft, utils._remap_blendshape(FaceBlendShape.EyeLookDownLeft, self.eye_out_left))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookInLeft, utils._remap_blendshape(FaceBlendShape.EyeLookInLeft, self.eye_out_right))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookDownRight, utils._remap_blendshape(FaceBlendShape.EyeLookDownRight, self.eye_down_left))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookInRight, utils._remap_blendshape(FaceBlendShape.EyeLookInRight, self.eye_down_right))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookInRight, utils._remap_blendshape(FaceBlendShape.EyeLookInRight, self.eye_down_right))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookInRight, utils._remap_blendshape(FaceBlendShape.EyeLookInRight, self.eye_down_right))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookOutLeft, utils._remap_blendshape(FaceBlendShape.EyeLookOutLeft, self.eye_up_right))
        self._face_data.set_blendshape(FaceBlendShape.EyeLookUpLeft, utils._remap_blendshape(FaceBlendShape.EyeLookUpLeft, self.eye_up_left))

    def calculate_eye_squint(self):
        for eye_side in ['left', 'right']:
            squint = utils.dist(
                self._get_landmark(self.blend_shape_config.CanonicalPoints.__dict__['squint_'+eye_side][0]),
                self._get_landmark(self.blend_shape_config.CanonicalPoints.__dict__['squint_'+eye_side][1])
            )
            self._face_data.set_blendshape(
                eval('FaceBlendShape.EyeSquint'+eye_side.capitalize()),
                utils._remap_blendshape(eval('FaceBlendShape.EyeSquint'+eye_side.capitalize()), 1 - squint))
    
    def detect_blinks(self):
        # Eye Blink ---------------
                
        eye_open_ration = self.call_stabilize_blink()
        
        eye_open_ratio_left = eye_open_ration['l']
        eye_open_ratio_right = eye_open_ration['r']


        if(abs(eye_open_ratio_left - eye_open_ratio_right) < 0.25):
            max = eye_open_ratio_left if eye_open_ratio_left >= eye_open_ratio_right else eye_open_ratio_right
            eye_open_ratio_left = eye_open_ratio_right = max
        
        blink_left = 1 if eye_open_ratio_left < 0.25 else 0
        blink_right = 1 if eye_open_ratio_right < 0.25 else 0    
        
        if(self.eye_pupil_state["DOWN"]):
            blink_left = 1 if eye_open_ratio_left < 0.18 else 0
            blink_right = 1 if eye_open_ratio_right < 0.18 else 0 
            if(self.eye_pupil_state["LEFT"]):
                blink_right = 1 if eye_open_ratio_right < 0.13 else 0
            
        if(self.eye_pupil_state["UP"]):
            blink_left = 1 if eye_open_ratio_left < 0.35 else 0
            blink_right = 1 if eye_open_ratio_right < 0.35 else 0  
        
        self.eye_close = True if(blink_left == 1 and blink_right == 1) else False
        self.pupil_movement_isThreshold = True if(eye_open_ratio_left > 0.5 and eye_open_ratio_right > 0.5) else False

        self._face_data.set_blendshape(FaceBlendShape.EyeBlinkLeft, blink_left, True)
        self._face_data.set_blendshape(FaceBlendShape.EyeBlinkRight, blink_right, True)

        self._face_data.set_blendshape(FaceBlendShape.EyeWideLeft, utils._remap_blendshape(
            FaceBlendShape.EyeWideLeft, eye_open_ratio_left))
        self._face_data.set_blendshape(FaceBlendShape.EyeWideRight, utils._remap_blendshape(
            FaceBlendShape.EyeWideRight, eye_open_ratio_right))

        # ----------------------------------------

    def detect_brow_actions(self):
        #Brow up down

        right_brow_lower = (
                                   self._get_landmark(self.blend_shape_config.CanonicalPoints.right_brow_lower[0]) +
                                   self._get_landmark(self.blend_shape_config.CanonicalPoints.right_brow_lower[1]) +
                                   self._get_landmark(self.blend_shape_config.CanonicalPoints.right_brow_lower[2])
                           ) / 3
        right_brow_dist = utils.dist(self._get_landmark(self.blend_shape_config.CanonicalPoints.right_brow),
                                    right_brow_lower)

        left_brow_lower = (
                                  self._get_landmark(self.blend_shape_config.CanonicalPoints.left_brow_lower[0]) +
                                  self._get_landmark(self.blend_shape_config.CanonicalPoints.left_brow_lower[1]) +
                                  self._get_landmark(self.blend_shape_config.CanonicalPoints.left_brow_lower[2])
                          ) / 3
        left_brow_dist = utils.dist(self._get_landmark(self.blend_shape_config.CanonicalPoints.left_brow),
                                   left_brow_lower)

        brow_down_left =  utils._remap_blendshape(FaceBlendShape.BrowDownLeft, left_brow_dist)
        self._face_data.set_blendshape(FaceBlendShape.BrowDownLeft, brow_down_left)

        brow_outer_up_left = utils._remap_blendshape(FaceBlendShape.BrowOuterUpLeft, left_brow_dist)
        self._face_data.set_blendshape(FaceBlendShape.BrowOuterUpLeft, brow_outer_up_left)

        brow_down_right =  utils._remap_blendshape(FaceBlendShape.BrowDownRight, right_brow_dist)
        self._face_data.set_blendshape(FaceBlendShape.BrowDownRight, brow_down_right)

        brow_outer_up_right = utils._remap_blendshape(FaceBlendShape.BrowOuterUpRight, right_brow_dist)
        self._face_data.set_blendshape(FaceBlendShape.BrowOuterUpRight, brow_outer_up_right)
        # print(brow_outer_up_right)
        #-------------------------------------------------

        #Extra
        inner_brow = self._get_landmark(self.blend_shape_config.CanonicalPoints.inner_brow)
        upper_nose = self._get_landmark(self.blend_shape_config.CanonicalPoints.upper_nose)
        inner_brow_dist = utils.dist(upper_nose, inner_brow)

        brow_inner_up = utils._remap_blendshape(FaceBlendShape.BrowInnerUp, inner_brow_dist)
        self._face_data.set_blendshape(FaceBlendShape.BrowInnerUp, brow_inner_up)
        # print(brow_inner_up)

    def detect_cheek(self):
        # Cheek is turned over left or right (will be higher when goes right up or left up) (will be 1 when nose also turn over)

        cheek_squint_left = utils.dist(
            self._get_landmark(self.blend_shape_config.CanonicalPoints.cheek_squint_left[0]),
            self._get_landmark(self.blend_shape_config.CanonicalPoints.cheek_squint_left[1])
        )

        cheek_squint_right = utils.dist(
            self._get_landmark(self.blend_shape_config.CanonicalPoints.cheek_squint_right[0]),
            self._get_landmark(self.blend_shape_config.CanonicalPoints.cheek_squint_right[1])
        )

        cheek_squint_left_final = 1 - utils._remap_blendshape(FaceBlendShape.CheekSquintLeft, cheek_squint_left)
        self._face_data.set_blendshape(FaceBlendShape.CheekSquintLeft, cheek_squint_left_final)

        cheek_squint_right_final = 1 - utils._remap_blendshape(FaceBlendShape.CheekSquintRight, cheek_squint_right)
        self._face_data.set_blendshape(FaceBlendShape.CheekSquintRight, cheek_squint_right_final)

        # print(cheek_squint_right_final)

        # ----------------------------------------------

        # just use the same values for cheeksquint for nose sneer, mediapipe deosn't seem to have a separate value for nose sneer
        self._face_data.set_blendshape(
            FaceBlendShape.NoseSneerLeft, self._face_data.get_blendshape(FaceBlendShape.CheekSquintLeft))
        self._face_data.set_blendshape(
            FaceBlendShape.NoseSneerRight, self._face_data.get_blendshape(FaceBlendShape.CheekSquintRight))
    
    def _pupil_position(self, side=None):
        if side is None:
            side = "RIGHT"
        if side == "RIGHT":
            canonical_points_eye = self.blend_shape_config.CanonicalPoints.eye_right
            canonical_points_iris = self.blend_shape_config.CanonicalPoints.iris_right
        if side == "LEFT":
            canonical_points_eye = self.blend_shape_config.CanonicalPoints.eye_left
            canonical_points_iris = self.blend_shape_config.CanonicalPoints.iris_left
        
 
        # Get landmarks for eye's outer corner, inner corner, and pupil.
        eye_outer_corner = self._get_landmark(canonical_points_eye[0])
        eye_inner_corner = (self._get_landmark(canonical_points_eye[1]) + self._get_landmark(canonical_points_eye[8])) / 2
        pupil = self._get_landmark(canonical_points_iris["middle"])

        # Calculate eye width and midpoint
        eye_width = utils.dist(eye_outer_corner, eye_inner_corner)
        mid_point = [ 0.5 * (eye_outer_corner[0] + eye_inner_corner[0]), 0.5 * (eye_outer_corner[1] + eye_inner_corner[1]) ]

        # Compute distances from midpoint to the pupil
        dx = mid_point[0] - pupil[0]
        dy = mid_point[1] - 0.075 * eye_width - pupil[1]
    
        # Normalize distances with respect to eye width
        ratio_x = 4 * dx / (eye_width / 2)
        ratio_y = 4 * dy / (eye_width / 4)

        # Assuming you want to store the result in your _face_data.
        # self._face_data.set_pupil_position({ 'x': ratio_x, 'y': ratio_y })  # You might want to adjust this line depending on how your program is structured.
        
        return ratio_x, ratio_y
   
    # Using EAR(Eye Aspect Ratio) for detecting blinks
    def get_eye_open_ration(self,points):
        eye_distance = self._eye_lid_distance(points)
        max_ratio = 0.285
        ratio = np.clip(eye_distance / max_ratio, 0, 2)
        return ratio
    
    def calculation_blink(self):
        #Blinks
        self.detect_blinks()
        
    def _lerp(self, v0, v1, t):
        return (1 - t) * v0 + t * v1
    
    def call_stabilize_blink(self):
        eye_l_low, eye_l_high = self.blend_shape_config.config.get(FaceBlendShape.EyeBlinkLeft)
        eye_r_low, eye_r_high = self.blend_shape_config.config.get(FaceBlendShape.EyeBlinkRight)
        
        eye_l = self.get_eye_open_ration(self.blend_shape_config.CanonicalPoints.eye_left)
        #eye_l_normalized = utils._remap(eye_l,eye_l_low,eye_l_high)
        #eye_l_normalized = utils.map_value(eye_l,eye_l_low,eye_l_high,0,1)
        eye_r = self.get_eye_open_ration(self.blend_shape_config.CanonicalPoints.eye_right)
        #eye_r_normalized = utils._remap(eye_r,eye_r_low,eye_r_high)
        #eye_r_normalized = utils.map_value(eye_r,eye_r_low,eye_r_high,0,1)

        eye = {'l': (eye_l or 0), 'r': (eye_r or 0)}
        
        head =self.calculate_head_pose()
        return self.stabilize_blink(eye, head['y'], 0.5, True)

    def stabilize_blink(self, eye:dict, headY:float, maxRot:0.5, enableWink:True):
        # clip the eye values to the range [0, 1]
        # eye['r'] = np.clip(eye['r'], 0, 1)
        # eye['l'] = np.clip(eye['l'], 0, 1)
        # calculate the difference between the left and right eye values
        blinkDiff = abs(eye['l'] - eye['r'])
        # set the threshold for detecting a wink based on the enableWink flag
        blinkThresh = 0.8 if enableWink else 1.2
        # check if the eyes are closing or open
        isClosing = eye['l'] < 0.3 and eye['r'] < 0.3
        isOpen = eye['l'] > 0.6 and eye['r'] > 0.6
        
        ###After a certain rotation, the right eye should be equalized with the left eye or the left eye with the right eye. 
        ###Because it cannot detect the other eye because it comes out of the camera angle.
        
        # # if the head is tilted to the right, return the right eye value for both eyes
        # if headY > maxRot:
        #     return {'l': eye['r'], 'r': eye['r']}
        # # if the head is tilted to the left, return the left eye value for both eyes
        # if headY < -maxRot:
        #     return {'l': eye['l'], 'r': eye['l']}

        # otherwise, return a weighted average of the left and right eye values
        # depending on the blinkDiff and the isClosing and isOpen flags
        return {
            'l': self._lerp(eye['r'], eye['l'], 0.05) if blinkDiff < blinkThresh or isClosing or isOpen else eye['l'],
            'r': self._lerp(eye['r'], eye['l'], 0.95) if blinkDiff < blinkThresh or isClosing or isOpen else eye['r'],
        }

    def calculate_head_pose(self):
        
        head_coords = {
            "21": self._get_landmark(21),
            "251": self._get_landmark(251),
            "397": self._get_landmark(397),
            "172": self._get_landmark(172),
        }
        
        head_pose = self._calculate_head_pose.calcHead(head_coords)
        
        return head_pose

    def _eye_lid_distance(self, eye_points):
        eye_width = utils.dist(self._get_landmark(
            eye_points[0]), self._get_landmark(eye_points[1]))
        eye_outer_lid = utils.dist(self._get_landmark(
            eye_points[2]), self._get_landmark(eye_points[5]))
        eye_mid_lid = utils.dist(self._get_landmark(
            eye_points[3]), self._get_landmark(eye_points[6]))
        eye_inner_lid = utils.dist(self._get_landmark(
            eye_points[4]), self._get_landmark(eye_points[7]))
        eye_lid_avg = (eye_outer_lid + eye_mid_lid + eye_inner_lid) / 3
        ratio = eye_lid_avg / eye_width

        return ratio
