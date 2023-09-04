
from .facedata import FaceBlendShape


class BlendShapeConfig:
        class CanonicalPoints:
            # Canonical points mapped from the canonical face model
            # for better understanding of the points, see the canonical face model from mediaPipe
            # https://github.com/google/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png

            eye_right = [33, 133, 160, 159, 158, 144, 145, 153, 173]
            eye_left = [263, 362, 387, 386, 385, 373, 374, 380, 398]
            head = [10, 152]
            nose_tip = 1
            upper_lip = 13
            lower_lip = 14
            upper_outer_lip = 12
            mouth_corner_left = 291
            mouth_corner_right = 61
            lowest_chin = 152
            upper_head = 10
            mouth_frown_left = 422
            mouth_frown_right = 202
            mouth_left_stretch = 287
            mouth_right_stretch = 57
            uppest_lip = 0
            lowest_lip = 17
            under_lip = 18
            over_upper_lip = 164
            left_upper_press = [40, 80]
            left_lower_press = [88, 91]
            right_upper_press = [270, 310]
            right_lower_press = [318, 321]
            squint_left = [253, 450]
            squint_right = [23, 230]            
            right_brow = 27
            right_brow_lower = [53, 52, 65]
            left_brow = 257
            left_brow_lower = [283, 282, 295]
            inner_brow = 9
            upper_nose = 6
            cheek_squint_left = [359, 342]
            cheek_squint_right = [130, 113]
            iris_right = {
                "middle":468,
                "right":469,
                "upper":470,
                "left":471,
                "lower":472
            }
            iris_left = {
                "middle":473,
                "left":474,
                "upper":475,
                "right":476,
                "lower":477
            }
            tongue_out = 52
            
        # blend shape type, min and max value
        config = {
            FaceBlendShape.EyeBlinkLeft : (0.16, 1.213),
            FaceBlendShape.EyeLookOutLeft : (2.675, 3.585), #EyeLookUpRight
            FaceBlendShape.EyeLookOutRight : (0, 2.00), #EyeLookInLeft
            FaceBlendShape.EyeLookUpRight : (2.3, 3.7), #EyeLookInRight
            FaceBlendShape.EyeLookUpLeft : (2.675, 3.585), #EyeLookUpLeft
            FaceBlendShape.EyeSquintLeft : (0.45, 0.65),
            FaceBlendShape.EyeWideLeft : (0.9, 1.2),
            FaceBlendShape.EyeBlinkRight : (0.175, 1.22),
            FaceBlendShape.EyeLookDownLeft : (2.7, 4.20), #EyeLookOutLeft
            FaceBlendShape.EyeLookDownRight : (-1.50, -1.00), #EyeLookDownLeft
            FaceBlendShape.EyeLookInLeft : (0.40, 2.10), #EyeLookOutRight
            FaceBlendShape.EyeLookInRight : (-1.60, -1.10), #EyeLookDownRight
            FaceBlendShape.EyeSquintRight : (0.45, 0.65),
            FaceBlendShape.EyeWideRight : (0.9, 1.2),
            # FaceBlendShape.JawForward : (-0.4, 0.0),
            FaceBlendShape.JawLeft : (-0.4, 0.0),
            FaceBlendShape.JawRight : (0.05, 0.4),
            FaceBlendShape.JawOpen : (0.50, 0.55),
            FaceBlendShape.MouthClose : (3.0, 4.5),
            FaceBlendShape.MouthOpen : (0.02, 0.62),
            FaceBlendShape.MouthFunnel : (15, 46),
            # FaceBlendShape.MouthPucker : (3.46, 4.92),
            FaceBlendShape.MouthPucker : (0, 1.1),
            # FaceBlendShape.MouthLeft : (-3.4, -2.3),
            # FaceBlendShape.MouthRight : ( 1.5, 3.0),
            FaceBlendShape.MouthLeft: (0.4, 1.2),
            FaceBlendShape.MouthRight: (-1.2, -0.4),
            FaceBlendShape.MouthSmileLeft : (-0.25, 0.2),
            FaceBlendShape.MouthSmileRight : (-0.25, 0.0),
            FaceBlendShape.MouthFrownLeft : (0.4, 0.9),
            FaceBlendShape.MouthFrownRight : (0.4, 0.9),
            # FaceBlendShape.MouthDimpleLeft : (-0.4, 0.0),
            # FaceBlendShape.MouthDimpleRight : (-0.4, 0.0),
            FaceBlendShape.MouthStretchLeft : (-0.4, 0.0),
            FaceBlendShape.MouthStretchRight : (-0.4, 0.0),
            FaceBlendShape.MouthRollLower : (0.5, 1.0),
            FaceBlendShape.MouthRollUpper : (0.5,0.95),
            FaceBlendShape.MouthShrugLower : (1.9, 2.3),
            FaceBlendShape.MouthShrugUpper : (1.4, 2.4),
            FaceBlendShape.MouthPressLeft : (0.4, 0.5),
            
            FaceBlendShape.MouthPressRight : (0.4, 0.5),
            FaceBlendShape.MouthLowerDownLeft : (1.7, 2),
            FaceBlendShape.MouthLowerDownRight : (1.7, 2),
            # FaceBlendShape.MouthUpperUpLeft : (-0.4, 0.0),
            # FaceBlendShape.MouthUpperUpRight : (-0.4, 0.0),
            FaceBlendShape.BrowDownLeft : (0.7, 1.2),
            FaceBlendShape.BrowDownRight : (0.7, 1.2),
            FaceBlendShape.BrowInnerUp : (2.2, 2.6),
            FaceBlendShape.BrowOuterUpLeft : (1.25, 1.5),
            FaceBlendShape.BrowOuterUpRight : (1.25, 1.5),
            FaceBlendShape.CheekPuff : (2.9, 3.16),
            FaceBlendShape.CheekSquintLeft : (0.55, 0.63),
            FaceBlendShape.CheekSquintRight : (0.55, 0.63),
            # FaceBlendShape.NoseSneerLeft : (-0.4, 0.0),
            # FaceBlendShape.NoseSneerRight : (-0.4, 0.0),
            FaceBlendShape.TongueOut : (0.0, 1.0),
            # FaceBlendShape.HeadYaw : (-0.4, 0.0),
            # FaceBlendShape.HeadPitch : (-0.4, 0.0),
            # FaceBlendShape.HeadRoll : (-0.4, 0.0),
            # FaceBlendShape.LeftEyeYaw : (-0.4, 0.0),
            # FaceBlendShape.LeftEyePitch : (-0.4, 0.0),
            # FaceBlendShape.LeftEyeRoll : (-0.4, 0.0),
            # FaceBlendShape.RightEyeYaw : (-0.4, 0.0),
            # FaceBlendShape.RightEyePitch : (-0.4, 0.0),
            # FaceBlendShape.RightEyeRoll : (-0.4, 0.0),
            FaceBlendShape.LipLowerDownLeft: (3.45, 3.8),
            FaceBlendShape.LipLowerDownRight: (3.45, 3.8),
            FaceBlendShape.LipUpperUpLeft: (2.8, 3.45),
            FaceBlendShape.LipUpperUpRight: (2.8, 3.45),
            FaceBlendShape.FaceSuprise: (2.73, 3.55),
            
        }

       
