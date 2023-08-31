import numpy as np
from .facedata import FaceData, FaceBlendShape
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from .blendshape_config import BlendShapeConfig
from .calculate_head_pose import CalculateHeadPose
from .calculate_eye_pose import CalculateEyePose
from .calculate_mouth_pose import CalculateMouthPose

#Big Thanks to https://github.com/JimWest/MeFaMo for his great repository

class BlendshapeCalculator():
    """ BlendshapeCalculator class

    This class calculates the blendshapes from the given landmarks.
    """
    
    def __init__(self) -> None:
        self.blend_shape_config = BlendShapeConfig()
        
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

        self._calculate_mouth_pose.after_init(metric_landmarks, normalized_landmarks,face_data)
        self._calculate_mouth_landmarks()
        
        #self._calculate_eye_pose.after_init(metric_landmarks, normalized_landmarks,calculate_head_pose,face_data)
        #self._calculate_eye_landmarks()
     
    #  clamp value to 0 - 1 using the min and max values of the config

    def _calculate_mouth_landmarks(self):
        self._calculate_mouth_pose.calculate_mouth_landmarks()


    def _calculate_eye_landmarks(self):
        self._calculate_eye_pose.calculation_blink()
        self._calculate_eye_pose.calculate_eye_landmarks()


