from calendar import c
import numpy as np
from .facedata import FaceData, FaceBlendShape
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from .blendshape_config import BlendShapeConfig
from .calculate_head_pose import CalculateHeadPose
from .calculate_eye_pose import CalculateEyePose
from .calculate_mouth_pose import CalculateMouthPose
from . import utils
import json

#Big Thanks to https://github.com/JimWest/MeFaMo for his great repository

class BlendshapeCalculator():
    """ BlendshapeCalculator class

    This class calculates the blendshapes from the given landmarks.
    """
    
    def __init__(self) -> None:
        self.blend_shape_config = BlendShapeConfig()
    
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

        landmarks = self._metric_landmarks
        if use_normalized:
            landmarks = self._normalized_landmarks

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
        
    def calculate_blendshapes(self, face_data: FaceData, metric_landmarks: np.ndarray,
                              normalized_landmarks: RepeatedCompositeFieldContainer, calculate_head_pose: CalculateHeadPose, 
                                calculate_eye_pose: CalculateEyePose, calculate_mouth_pose: CalculateMouthPose) -> None:
        """ Calculate the blendshapes from the given landmarks.

        This function calculates the blendshapes from the given landmarks and stores them in the given live_link_face.

        Parameters
        ----------
        face_data : FaceData
            Index of the BlendShape to get the value from.
        metric_landmarks: np.ndarray
            The metric landmarks of the face in 3d.
        normalized_landmarks: RepeatedCompositeFieldContainer
            Output from the mediapipe process function for each face.
        calculate_head_pose: CalculateHeadPose
            The head pose calculator.
        calculate_eye_pose: CalculateEyePose
            The eye pose calculator.
        calculate_mouth_pose: CalculateMouthPose
            The mouth pose calculator.

        Returns
        ----------
        None
        """

        self._face_data = face_data
        self._metric_landmarks = metric_landmarks
        self._normalized_landmarks = normalized_landmarks
        self._calculate_head_pose = calculate_head_pose
        self._calculate_eye_pose = calculate_eye_pose
        self._calculate_mouth_pose = calculate_mouth_pose

        self._calculate_eye_pose.after_init(metric_landmarks, normalized_landmarks,calculate_head_pose,face_data)
        self._calculate_eye_landmarks()
        
        self._calculate_mouth_pose.after_init(metric_landmarks, normalized_landmarks,face_data)
        self._calculate_mouth_landmarks()
        
        self._calculate_face_suprise()
     
    def _calculate_mouth_landmarks(self):
        self._calculate_mouth_pose.calculate_mouth_landmarks()

    def _calculate_eye_landmarks(self):
        self._calculate_eye_pose.calculation_blink()
        self._calculate_eye_pose.calculate_eye_landmarks()
        
    def _calculate_face_suprise(self):
        nose_right_brow_dist = utils.dist(self._get_landmark(self.blend_shape_config.CanonicalPoints.nose_tip), self._get_landmark(285))
        nose_left_brow_dist = utils.dist(self._get_landmark(self.blend_shape_config.CanonicalPoints.nose_tip), self._get_landmark(55))
        upper_and_lower_lip_dist = utils.dist(self._get_landmark(self.blend_shape_config.CanonicalPoints.upper_lip), self._get_landmark(self.blend_shape_config.CanonicalPoints.lower_lip))
        right_eye_lid_brow_dist = utils.dist(self._get_landmark(442), self._get_landmark(self.blend_shape_config.CanonicalPoints.left_brow_lower[2]))
        left_eye_lid_brow_dist = utils.dist(self._get_landmark(222), self._get_landmark(self.blend_shape_config.CanonicalPoints.right_brow_lower[2]))
        eye_open_ration = self._calculate_eye_pose.call_stabilize_blink()
        eye_open_ratio_left = eye_open_ration['l']
        eye_open_ratio_right = eye_open_ration['r']
        averageWithWeights = np.average([1.2 * nose_right_brow_dist, 1.2 * nose_left_brow_dist, 
                                                upper_and_lower_lip_dist * 0.5 , right_eye_lid_brow_dist * 1.2, 
                                                    left_eye_lid_brow_dist * 1.2, eye_open_ratio_left * 1.5, eye_open_ratio_right * 1.5])

        last_value = utils._remap_blendshape(FaceBlendShape.FaceSuprise, averageWithWeights)
        self._face_data.set_blendshape(FaceBlendShape.FaceSuprise, last_value)
        

        with open('deneme2.json', 'a') as f:
            json.dump(
                
                {
                    'nose_right_brow_dist': nose_right_brow_dist,
                    'nose_left_brow_dist': nose_left_brow_dist,
                    'upper_and_lower_lip_dist': upper_and_lower_lip_dist,
                    'right_eye_lid_brow_dist': right_eye_lid_brow_dist,
                    'left_eye_lid_brow_dist': left_eye_lid_brow_dist,
                    'eye_open_ratio_left': eye_open_ratio_left,
                    'eye_open_ratio_right': eye_open_ratio_right,
                    'Avarage': last_value,
                }
                
                , f)
            f.write('\n')
    
    


