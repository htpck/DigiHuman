using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class NetworkManager : MonoSingleton<NetworkManager>
{
    // Singleton instance
    private static NetworkManager instance;

    [Header("Dependencies")]
    [SerializeField] private FrameReader frameReader;

    [Header("Debug")]
    [SerializeField] private bool enableDebug;
    [SerializeField] private string filePath;

    // Get the instance of NetworkManager
    public static NetworkManager Instance
    {
        get
        {
            if (instance == null)
            {
                instance = FindObjectOfType<NetworkManager>();
                if (instance == null)
                {
                    GameObject obj = new GameObject();
                    obj.name = typeof(NetworkManager).Name;
                    instance = obj.AddComponent<NetworkManager>();
                }
            }
            return instance;
        }
    }

    [Serializable]
    public struct UploadResponse
    {
        public string file;
        public int totalFrames;
        public float aspectRatio;
    }

    [Serializable]
    public struct PoseRequest
    {
        public string fileName;
        public int index;
    }

    private void Awake()
    {
        // Ensure only one instance exists
        if (instance != null && instance != this)
        {
            Destroy(this.gameObject);
        }
        else
        {
            instance = this;
            DontDestroyOnLoad(this.gameObject);
        }
    }

    private void Start()
    {
        if (enableDebug)
        {
            StartCoroutine(LoadJSONFileAndProcess(filePath));
        }
    }

    // Load a JSON file from the computer and process its data
    public IEnumerator LoadJSONFileAndProcess(string jsonFilePath)
    {
        if (!File.Exists(jsonFilePath))
        {
            Debug.LogError("JSON file does not exist at path: " + jsonFilePath);
            yield break;
        }

        string jsonContent = File.ReadAllText(jsonFilePath);

        // INS!! JSON file contains FullPoseJson data
        FullPoseJson[] fullPoseData = JsonUtility.FromJson<FullPoseJson[]>(jsonContent);

        List<HandJson> handJsons = new List<HandJson>();
        List<PoseJson> bodyJsons = new List<PoseJson>();

        UIManager.Instancce.CheckAndEnableWaitingModeUI(WaitingModeUI.ProgressBar, true);
        UIManager.Instancce.UpdateProgressBar(0);

        float totalFrames = fullPoseData.Length;

        for (int i = 0; i < fullPoseData.Length; i++)
        {
            FullPoseJson receivedJson = fullPoseData[i];
            bodyJsons.Add(receivedJson.bodyPose);
            HandJson handData = receivedJson.handsPose;
            handJsons.Add(handData);
            UIManager.Instancce.UpdateProgressBar((float)i / totalFrames);
        }

        UIManager.Instancce.UpdateProgressBar(1);
        frameReader.SetHandPoseList(handJsons);
        frameReader.SetPoseList(bodyJsons);
        UIManager.Instancce.OnFullPoseDataReceived();

        UIManager.Instancce.CheckAndEnableWaitingModeUI(WaitingModeUI.ProgressBar, false);

        yield break;
    }
    // Add this method to your NetworkManager class
    public void LoadJSONFileAndProcess(string filePath, Action onSuccess = null)
    {
        StartCoroutine(LoadJSONFileAndProcess(filePath));
        onSuccess?.Invoke();
    }

}
