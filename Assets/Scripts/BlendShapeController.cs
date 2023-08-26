using System;
using System.Collections;
using System.Collections.Generic;
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

    

    
    [Header("Methods")][Tooltip("How to deal with each blend weights")]
    [SerializeField] private int eyeWideMethod;
    [SerializeField] private int mouthOpenMethod = 1; 
    [SerializeField] private int mouthSmileFrownMethod;

    [Header("Blend Shapes")]
    public BlendShape EyeBlinkLeft = new BlendShape(){
        num = -1,
        weight = 0
    };
    public BlendShape EyeBlinkRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape EyeSquintLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape EyeSquintRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape EyeWideLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape EyeWideRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthSmileRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthSmileLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthFrownRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthFrownLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape LipLowerDownLeft = new BlendShape() {
    num = -1,
    weight = 0
    };
    public BlendShape LipLowerDownRight = new BlendShape() {
    num = -1,
    weight = 0
    };
    
    public BlendShape LipUpperUpLeft = new BlendShape() {
    num = -1,
    weight = 0
    };
    
    public BlendShape LipUpperUpRight = new BlendShape() {
    num = -1,
    weight = 0
    };
    
    public BlendShape MouthLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthStretchLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthStretchRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthLowerDownRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthLowerDownLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthPressLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthPressRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthOpen = new BlendShape(){ //fdgfg
    num = -1,
    weight = 0
    };

    public BlendShape MouthPucker = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthShrugUpper = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthShrugLower = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape JawOpen = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape JawLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape JawRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape BrowDownLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape BrowOuterUpLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape BrowDownRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape BrowOuterUpRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape CheekSquintRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape CheekSquintLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthDimpleLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthDimpleRight = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthRollLower = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape MouthRollUpper = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape NoseSneerLeft = new BlendShape(){
    num = -1,
    weight = 0
    };

    public BlendShape NoseSneerRight = new BlendShape(){
    num = -1,
    weight = 0
    };
    public BlendShape MouthOpenLowerTeeth = new BlendShape()
    {    
        num = 1, // Set the blend shape index of the mouth opening for the lower teeth
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



    public void UpdateBlendShape()
    {
        // Apply deformation weights
        
        // Apply Eye values
        UpdateEyes();

        // Apply mouth smile and frown values
        UpdateMouthSmileFrownWeights();
        
        // Lips
        LipsDirection();


        // Update the second SkinnedMeshRenderer (index 1) with the mouth opening blend shape for the lower teeth
        MouthOpenLowerTeeth.weight = JawOpen.weight;
        UpdateBlendShapeWeight(MouthOpenLowerTeeth);

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
        else if(mouthOpenMethod == 2)
        {
            if (MouthOpen.weight > 80)
                MouthOpen.weight = 100;
            if(MouthOpen.weight > 1)
            {
                MouthOpen.weight = MappingEffect(MouthOpen.weight, 80, 120, 0);
            }
        }
        UpdateBlendShapeWeight(MouthOpen);
        UpdateBlendShapeWeight(MouthPucker);
        
        UpdateBlendShapeWeight(MouthShrugUpper);
        UpdateBlendShapeWeight(MouthShrugLower);
        UpdateBlendShapeWeight(JawOpen);
        UpdateBlendShapeWeight(JawLeft);
        UpdateBlendShapeWeight(JawRight);
        
        UpdateBlendShapeWeight(BrowDownLeft);
        UpdateBlendShapeWeight(BrowOuterUpLeft);
        UpdateBlendShapeWeight(BrowDownRight);
        UpdateBlendShapeWeight(BrowOuterUpRight);

        UpdateBlendShapeWeight(MouthOpenLowerTeeth);

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

        UpdateBlendShapeWeight(TongueOut);

        if (enableEyeWide)
        {
            if (eyeWideMethod == 1)
            {
                EyeWideLeft.weight = MappingEffect(EyeWideLeft.weight - 80, 20, 100, -40);
                EyeWideRight.weight = MappingEffect(EyeWideRight.weight - 80, 20, 100, -40);
            }
            else if(eyeWideMethod == 2)
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
            MouthSmileRight.weight = MappingEffect(MouthSmileRight.weight - 40,60,100,0);
            MouthSmileLeft.weight = MappingEffect(MouthSmileLeft.weight - 40,60,100,0);
            MouthDimpleLeft.weight = MappingEffect(MouthDimpleLeft.weight - 40,60,100,0);
            MouthDimpleRight.weight = MappingEffect(MouthDimpleRight.weight - 40,60,100,0);
            
        }

        if (enableSimultaneouslyFrown)
        {
            MouthFrownRight.weight = (MouthFrownLeft.weight + MouthFrownRight.weight) / 2.0f;
            MouthFrownLeft.weight = MouthFrownRight.weight;
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
        
        UpdateBlendShapeWeight(blend.skinnedMeshIndex,blend.num,blend.weight);
        
    }
    private void UpdateBlendShapeWeight(int skinnedMeshIndex, int blendNum, float blendWeight)
    {
        

        if (blendNum != -1) 
        {
            var clamValue = Mathf.Clamp(blendWeight, 0, 100);
            if(skinnedMeshIndex == 2 && (blendNum == 14 || blendNum == 13 || blendNum == 15 || blendNum == 12)) {
                clamValue = Mathf.Clamp(blendWeight*2, 0, 200);
            }
            if (skinnedMeshIndex == 2 && (blendNum == 16 || blendNum == 17))
            {
                clamValue = clamValue > 70 ? clamValue * 1.2f : clamValue;
            }
            if (skinnedMeshIndex == 4 && (blendNum == 15 || blendNum == 16))
            {
                clamValue = clamValue > 70 ? clamValue * 1.2f : clamValue;
            }
            if (skinnedMeshIndex == 0 && (blendNum == 6 || blendNum == 7))
            {
                clamValue = Mathf.Clamp(blendWeight * 1.2f, 0, 120);
            }
            if (skinnedMeshIndex == 4 && (blendNum == 9 || blendNum == 10))
            {
                clamValue = Mathf.Clamp(blendWeight * 1.2f, 0, 120);
            }
            if(skinnedMeshIndex == 0 && (blendNum == 16 || blendNum == 61))
            {
                clamValue = Mathf.Clamp(blendWeight * 0.5f, 0, 50);
            }
            if (skinnedMeshIndex == 4 && (blendNum == 19|| blendNum == 61))
            {
                clamValue = Mathf.Clamp(blendWeight * 0.5f, 0, 50);
            }
            //if (skinnedMeshIndex == 0 && (blendNum == 4 || blendNum == 5))
            //{
            //    if (clamValue >= 95) clamValue = 100;
            //    if (clamValue >= 50 && clamValue < 95) clamValue = 35;
            //    if (clamValue < 35) clamValue = 0;
            //}
            skinnedMeshRenderers[skinnedMeshIndex].SetBlendShapeWeight(blendNum, clamValue);
        }
        else
        {
            //Debug.Log("nbr");
        }
        
    }
    

    //change the value between 0 upto effectOrder
    private float MappingEffect(float value, float maxValue, float effectOrder, float offset)
    {
        return (value / maxValue) * effectOrder + offset;
    }
    
}