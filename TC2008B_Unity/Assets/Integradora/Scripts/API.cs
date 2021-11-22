using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System;

[Serializable]
public class Agent
{
    public int x;
    public int y;
    public int z;

    public void print()
    {
        Debug.Log(x);
        Debug.Log(y);
        Debug.Log(z);
    }
}

public static class JsonHelper
{
    public static T[] FromJson<T>(string json)
    {
        Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
        return wrapper.Items;
    }

    public static string ToJson<T>(T[] array)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return JsonUtility.ToJson(wrapper);
    }

    public static string ToJson<T>(T[] array, bool prettyPrint)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return JsonUtility.ToJson(wrapper, prettyPrint);
    }

    [Serializable]
    private class Wrapper<T>
    {
        public T[] Items;
    }
}

public class API : MonoBehaviour
{
    [SerializeField] string url;
    [SerializeField] string testTP;
    [SerializeField] string configTP;
    [SerializeField] string updateTP;
    [SerializeField] int numAgents;

    Agent[] agents;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(GetAgents());
        StartCoroutine(SendConfiguration());
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    IEnumerator GetAgents()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + testTP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            agents = JsonHelper.FromJson<Agent>(www.downloadHandler.text);
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("Confimation", "Good");

        UnityWebRequest www = UnityWebRequest.Post(url + configTP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }
}
