using System;
using System.Collections;
using System.Collections.Generic;
using System.IO.Pipes;
using System.Linq;
using System.Reflection;
using Unity.Mathematics;
using UnityEditor.Experimental.GraphView;
using UnityEngine;


[Serializable]
public struct BlendShape
{
    public int num;
    [HideInInspector]public float weight;
    [Tooltip("Which skinned mesh should be affected")] public int skinnedMeshIndex;
}

public class BlendShapeController : MonoBehaviour
{
    [SerializeField] private SkinnedMeshRenderer[] skinnedMeshRenderers;

    [Header("Enable | Disable options")]
    [SerializeField] private bool enableEyeWide;
    [SerializeField] private bool enableDimple;
    [SerializeField] private bool enableCheekSquint;
    [SerializeField] private bool enableNose;
    [Tooltip("Enabling this option will open and close eyes together(you can not blink!)")]
    [SerializeField] private bool enableSimultaneouslyEyesOpenClose;
    [Tooltip("Enabling this option will frown your mouth together(you can not frown one side)")]
    [SerializeField] private bool enableSimultaneouslyFrown;




    [Header("Methods")]
    [Tooltip("How to deal with each blend weights")]
    [SerializeField] private int eyeWideMethod;
    [SerializeField] private int mouthOpenMethod = 1;
    [SerializeField] private int mouthSmileFrownMethod;

    [Header("Blend Shapes")]
    public BlendShape EyeBlinkLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape EyeBlinkRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape EyeSquintLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape EyeSquintRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape EyeWideLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape EyeWideRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthSmileRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthSmileLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthFrownRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthFrownLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape LipLowerDownLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape LipLowerDownRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape LipUpperUpLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape LipUpperUpRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthStretchLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthStretchRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthLowerDownRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthLowerDownLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthPressLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthPressRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthOpen = new BlendShape()
    { //fdgfg
        num = -1,
        weight = 0
    };
    public BlendShape MouthPucker = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthShrugUpper = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthShrugLower = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape JawOpen = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape JawLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape JawRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape BrowDownLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape BrowOuterUpLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape BrowDownRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape BrowOuterUpRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape CheekSquintRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape CheekSquintLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthDimpleLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthDimpleRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthRollLower = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthRollUpper = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape NoseSneerLeft = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape NoseSneerRight = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthOpenLowerTeeth = new BlendShape()
    {
        num = -1, // Set the blend shape index of the mouth opening for the lower teeth
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape MouthRightLowerTeeth = new BlendShape()
    {
        num = -1, // Set the blend shape index of the mouth opening for the lower teeth
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape MouthLeftLowerTeeth = new BlendShape()
    {
        num = -1, // Set the blend shape index of the mouth opening for the lower teeth
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyeLookDownLeft = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookDownLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyeLookDownRight = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookDownRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyeLookInLeft = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookInLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyeLookInRight = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookInRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyeLookOutLeft = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyeLookOutRight = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyeLookUpLeft = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyeLookUpRight = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape TongueOut = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape TongueMouthOpen = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape TongueMouthRight = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape TongueMouthLeft = new BlendShape()
    {

        num = -1, // Set the blend shape index for eye_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceEyeLookDownLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookDownLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceEyeLookDownRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookDownLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceEyeLookUpLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceEyeLookUpRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceEyeLookInLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookInLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceEyeLookInRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookInRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceEyeLookOutLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceEyeLookOutRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeLookDownLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookDownLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeLookDownRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookDownLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeLookUpLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeLookUpRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeLookInLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookInLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeLookInRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookInRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeLookOutLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeLookOutRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeSquintLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeSquintRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeWideLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeWideRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeBlinkLeft = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutLeft (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape EyelashesEyeBlinkRight = new BlendShape()
    {
        num = -1, // Set the blend shape index for face_eyeLookOutRight (find it in Unity editor or through code)
        weight = 0 // Set the initial weight as desired
    };
    public BlendShape FaceSuprise = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape LowerTeethSuprise = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape TongueSuprise = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape CheekPuff = new BlendShape()
    {
        num = -1,
        weight = 0
    };
    public BlendShape MouthFunnel = new BlendShape()
    {
        num = -1,
        weight = 0
    };


    public void UpdateBlendShape()
    {
        // Apply deformation weights

        // Apply Eye values
        UpdateEyes();

        // Apply mouth smile and frown values
        UpdateMouthSmileFrownWeights();

        // Lips
        LipsDirection();


        // Update the first SkinnedMeshRenderer (index 0) with the new eye blend shapes


        UpdateBlendShapeWeight(MouthLeft);
        UpdateBlendShapeWeight(MouthRight);

        UpdateBlendShapeWeight(MouthStretchLeft);
        UpdateBlendShapeWeight(MouthStretchRight);

        UpdateBlendShapeWeight(MouthLowerDownRight);
        UpdateBlendShapeWeight(MouthLowerDownLeft);

        UpdateBlendShapeWeight(MouthPressLeft);
        UpdateBlendShapeWeight(MouthPressRight);

        if (mouthOpenMethod == 1)
        {
            MouthOpen.weight *= 4;
        }
        else if (mouthOpenMethod == 2)
        {
            if (MouthOpen.weight > 80)
                MouthOpen.weight = 100;
            if (MouthOpen.weight > 1)
            {
                MouthOpen.weight = MappingEffect(MouthOpen.weight, 80, 120, 0);
            }
        }
        UpdateBlendShapeWeight(MouthOpen);
        UpdateBlendShapeWeight(MouthPucker);
        UpdateBlendShapeWeight(MouthFunnel);

        UpdateBlendShapeWeight(MouthShrugUpper);
        UpdateBlendShapeWeight(MouthShrugLower);
        UpdateBlendShapeWeight(JawOpen);
        UpdateBlendShapeWeight(JawLeft);
        UpdateBlendShapeWeight(JawRight);


        UpdateBlendShapeWeight(TongueOut);
        TongueMouthOpen.weight = MouthOpen.weight;
        UpdateBlendShapeWeight(TongueMouthOpen);
        UpdateBlendShapeWeight(TongueMouthRight);
        UpdateBlendShapeWeight(TongueMouthLeft);

        // Update the second SkinnedMeshRenderer (index 1) with the mouth opening blend shape for the lower teeth
        MouthOpenLowerTeeth.weight = MouthOpen.weight;
        UpdateBlendShapeWeight(MouthOpenLowerTeeth);
        UpdateBlendShapeWeight(MouthRightLowerTeeth);
        UpdateBlendShapeWeight(MouthLeftLowerTeeth);

        UpdateBlendShapeWeight(BrowDownLeft);
        UpdateBlendShapeWeight(BrowOuterUpLeft);
        UpdateBlendShapeWeight(BrowDownRight);
        UpdateBlendShapeWeight(BrowOuterUpRight);


        if (enableCheekSquint)
        {
            UpdateBlendShapeWeight(CheekSquintRight);
            UpdateBlendShapeWeight(CheekSquintLeft);
        }

        UpdateBlendShapeWeight(MouthRollLower);
        UpdateBlendShapeWeight(MouthRollUpper);

        if (enableNose)
        {
            UpdateBlendShapeWeight(NoseSneerLeft);
            UpdateBlendShapeWeight(NoseSneerRight);
        }

        UpdateBlendShapeWeight(CheekPuff);
        if (CheekPuff.weight > 0)
        {
            MouthPucker.weight = 0;
            MouthFunnel.weight = 0;
            MouthSmileRight.weight = 0;
            MouthSmileLeft.weight = 0;
            MouthDimpleLeft.weight = 0;
            MouthDimpleRight.weight = 0;
            LipUpperUpLeft.weight = 0;
            LipUpperUpRight.weight = 0;
            LipsDirection();
            UpdateMouthSmileFrownWeights();
            UpdateBlendShapeWeight(MouthPucker);
            UpdateBlendShapeWeight(MouthFunnel);
        }

        ActiveSupriseEmojis();
    }

    private void UpdateEyes()
    {
        if (enableSimultaneouslyEyesOpenClose)
        {
            EyeBlinkLeft.weight = (EyeBlinkLeft.weight + EyeBlinkRight.weight) / 2.0f;
            EyeBlinkRight.weight = EyeBlinkLeft.weight;
        }
        UpdateBlendShapeWeight(EyeBlinkLeft);
        UpdateBlendShapeWeight(EyeBlinkRight);
        UpdateBlendShapeWeight(EyeSquintLeft);
        UpdateBlendShapeWeight(EyeSquintRight);

        UpdateBlendShapeWeight(EyeLookDownLeft);
        UpdateBlendShapeWeight(EyeLookDownRight);
        UpdateBlendShapeWeight(EyeLookInLeft);
        UpdateBlendShapeWeight(EyeLookInRight);
        UpdateBlendShapeWeight(EyeLookOutLeft);
        UpdateBlendShapeWeight(EyeLookOutRight);
        UpdateBlendShapeWeight(EyeLookUpRight);
        UpdateBlendShapeWeight(EyeLookUpLeft);
        UpdateBlendShapeWeight(FaceEyeLookDownLeft);
        UpdateBlendShapeWeight(FaceEyeLookDownRight);
        UpdateBlendShapeWeight(FaceEyeLookUpLeft);
        UpdateBlendShapeWeight(FaceEyeLookUpRight);
        UpdateBlendShapeWeight(FaceEyeLookInLeft);
        UpdateBlendShapeWeight(FaceEyeLookInRight);
        UpdateBlendShapeWeight(FaceEyeLookOutLeft);
        UpdateBlendShapeWeight(FaceEyeLookOutRight);
        UpdateBlendShapeWeight(EyelashesEyeLookDownLeft);
        UpdateBlendShapeWeight(EyelashesEyeLookDownRight);
        UpdateBlendShapeWeight(EyelashesEyeLookUpLeft);
        UpdateBlendShapeWeight(EyelashesEyeLookUpRight);
        UpdateBlendShapeWeight(EyelashesEyeLookInLeft);
        UpdateBlendShapeWeight(EyelashesEyeLookInRight);
        UpdateBlendShapeWeight(EyelashesEyeLookOutLeft);
        UpdateBlendShapeWeight(EyelashesEyeLookOutRight);
        UpdateBlendShapeWeight(EyelashesEyeSquintLeft);
        UpdateBlendShapeWeight(EyelashesEyeSquintRight);
        UpdateBlendShapeWeight(EyelashesEyeBlinkLeft);
        UpdateBlendShapeWeight(EyelashesEyeBlinkRight);


        if (enableEyeWide)
        {
            if (eyeWideMethod == 1)
            {
                EyeWideLeft.weight = MappingEffect(EyeWideLeft.weight - 80, 20, 100, -40);
                EyeWideRight.weight = MappingEffect(EyeWideRight.weight - 80, 20, 100, -40);
            }
            else if (eyeWideMethod == 2)
            {
                if (EyeWideLeft.weight < 90)
                {
                    EyeWideLeft.weight = 0;
                }

                if (EyeWideRight.weight < 90)
                {
                    EyeWideRight.weight = 0;
                }
            }


            UpdateBlendShapeWeight(EyeWideLeft);
            UpdateBlendShapeWeight(EyeWideRight);
            UpdateBlendShapeWeight(EyelashesEyeWideLeft);
            UpdateBlendShapeWeight(EyelashesEyeWideRight);

        }
    }

    private void LipsDirection()
    {
        UpdateBlendShapeWeight(LipLowerDownLeft);
        UpdateBlendShapeWeight(LipLowerDownRight);
        UpdateBlendShapeWeight(LipUpperUpLeft);
        UpdateBlendShapeWeight(LipUpperUpRight);

    }

    private void UpdateMouthSmileFrownWeights()
    {
        if (mouthSmileFrownMethod == 1)
        {
            MouthSmileRight.weight = MappingEffect(MouthSmileRight.weight - 40, 60, 100, 0);
            MouthSmileLeft.weight = MappingEffect(MouthSmileLeft.weight - 40, 60, 100, 0);
            MouthDimpleLeft.weight = MappingEffect(MouthDimpleLeft.weight - 40, 60, 100, 0);
            MouthDimpleRight.weight = MappingEffect(MouthDimpleRight.weight - 40, 60, 100, 0);

        }

        if (enableSimultaneouslyFrown)
        {
            MouthFrownRight.weight = (MouthFrownLeft.weight + MouthFrownRight.weight) / 2.0f;
            MouthFrownLeft.weight = MouthFrownRight.weight;
        }

        if (MouthOpen.weight > 25)
        {
            var maxNum = math.max(MouthSmileLeft.weight, MouthSmileRight.weight);

            MouthSmileRight.weight = MouthSmileLeft.weight = maxNum;
        }


        UpdateBlendShapeWeight(MouthSmileRight);
        UpdateBlendShapeWeight(MouthSmileLeft);
        if (enableDimple)
        {
            UpdateBlendShapeWeight(MouthDimpleLeft);
            UpdateBlendShapeWeight(MouthDimpleRight);
        }

        UpdateBlendShapeWeight(MouthFrownRight);
        UpdateBlendShapeWeight(MouthFrownLeft);
    }

    private void UpdateBlendShapeWeight(BlendShape blend)
    {

        UpdateBlendShapeWeight(blend.skinnedMeshIndex, blend.num, blend.weight);

    }

    private void UpdateBlendShapeWeight(int skinnedMeshIndex, int blendNum, float blendWeight)
    {
        // Check if the blend number is valid
        if (blendNum == -1)
        {
            //Debug.Log("nbr");
            return;
        }

        // Clamp the blend weight to a range of 0 to 100
        var clamValue = Mathf.Clamp(blendWeight, 0, 100);

        // Apply some special rules for different skinned mesh and blend number combinations
        switch (skinnedMeshIndex)
        {
            case 0:
                if (blendNum == 6 || blendNum == 7 || blendNum == 16 || blendNum == 61)
                {
                    // Adjust the clam value by a factor of 1.2 or 0.5 depending on the blend number
                    var factor = (blendNum == 16 || blendNum == 61) ? 0.5f : 1.2f;
                    clamValue = Mathf.Clamp(blendWeight * factor, 0, factor * 100);
                }
                break;
            case 2:
                if (blendNum == 12 || blendNum == 13 || blendNum == 14 || blendNum == 15)
                {
                    // Double the clam value for these blend numbers
                    clamValue = Mathf.Clamp(blendWeight * 2, 0, 200);
                }
                else if (blendNum == 16 || blendNum == 17)
                {
                    // Increase the clam value by 20% if it is greater than 70
                    clamValue = clamValue > 70 ? clamValue * 1.2f : clamValue;
                }
                break;
            case 4:
                if (blendNum == 9 || blendNum == 10 || blendNum == 15 || blendNum == 16)
                {
                    // Adjust the clam value by a factor of 1.2 or 0.5 depending on the blend number
                    var factor = (blendNum == 9 || blendNum == 10) ? 1.2f : 0.5f;
                    clamValue = Mathf.Clamp(blendWeight * factor, 0, factor * 100);
                }
                else if (blendNum == 19 || blendNum == 61)
                {
                    // Halve the clam value for these blend numbers
                    clamValue = Mathf.Clamp(blendWeight * 0.5f, 0, 50);
                }
                break;
        }

        // Set the blend shape weight for the skinned mesh renderer
        skinnedMeshRenderers[skinnedMeshIndex].SetBlendShapeWeight(blendNum, clamValue);
    }
    //change the value between 0 upto effectOrder
    private float MappingEffect(float value, float maxValue, float effectOrder, float offset)
    {
        return (value / maxValue) * effectOrder + offset;
    }

    private void ActiveSupriseEmojis()
    {
        // Reset the weights of the surprise blend shapes if they are below a threshold
        if (FaceSuprise.weight < 70)
        {
            FaceSuprise.weight = 0;
            TongueSuprise.weight = 0;
            LowerTeethSuprise.weight = 0;
        }
        // Update the blend shape weights of the surprise features
        UpdateBlendShapeWeight(FaceSuprise);
        UpdateBlendShapeWeight(TongueSuprise);
        UpdateBlendShapeWeight(LowerTeethSuprise);

        // Check if the face is in a surprise expression and the mouth is not smiling
        var activeConditions = FaceSuprise.weight >= 70 && (MouthSmileLeft.weight < 25 || MouthSmileRight.weight < 25);

        // If the conditions are met, reduce the weights of all other blend shapes except the ones related to surprise
        if (activeConditions)
        {
            // Get all the blend shape enums and structs
            var enumList = (BlendShapes[])Enum.GetValues(typeof(BlendShapes));
            var structListBlendShapes = typeof(BlendShapeController).GetFields(BindingFlags.Public | BindingFlags.Instance).Where(x => x.FieldType == typeof(BlendShape)).ToList();

            // Loop through all the blend shape structs
            foreach (var item in structListBlendShapes)
            {
                // Get the blend shape object from the struct
                var blendShape = (BlendShape)item.GetValue(this);

                // If the blend shape is valid and has a non-zero weight
                if (blendShape.num != -1 && blendShape.weight != 0)
                {
                    // Skip the blend shapes related to surprise
                    if (blendShape.num == 43 && blendShape.skinnedMeshIndex == 0) continue;
                    if (blendShape.num == 52 && blendShape.skinnedMeshIndex == 1) continue;
                    if (blendShape.num == 53 && blendShape.skinnedMeshIndex == 2) continue;
                    if ((blendShape.num == 16 || blendShape.num == 61) && blendShape.skinnedMeshIndex == 0) continue;
                    if ((blendShape.num == 19 || blendShape.num == 61) && blendShape.skinnedMeshIndex == 4) continue;

                    // Reduce the weight of the blend shape by half and clamp it to non-negative values
                    blendShape.weight = math.max(blendShape.weight * 0.5f, 0);

                    // Set the new weight to the corresponding skinned mesh renderer
                    skinnedMeshRenderers[blendShape.skinnedMeshIndex].SetBlendShapeWeight(blendShape.num, blendShape.weight);
                }
            }
        }
    }
}