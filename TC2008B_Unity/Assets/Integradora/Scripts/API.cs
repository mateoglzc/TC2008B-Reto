using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System;

[Serializable]
public class Agent
{
    public float x;
    public float y;
    public float z;

    public string direction;

    public bool carryBox;

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
    [SerializeField] GameObject catBoy;

    Agent[] agents;

    GameObject[] agentGroup;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(SendConfiguration());

        agentGroup = new GameObject[numAgents];

        StartCoroutine(GetAgents());

    }

    // Update is called once per frame
    void Update()
    {
        // Move 
        // Sleep
        // StartCoroutine(GetAgents());
        
        
    }

    IEnumerator GetAgents()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + testTP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            agents = JsonHelper.FromJson<Agent>(www.downloadHandler.text);
            for (int i = 0; i < numAgents; i++)
            {
                // Update direction
                Vector3 temp = new Vector3(agents[i].x, agents[i].y, agents[i].z);
                agentGroup[i] = Instantiate(catBoy, temp, Quaternion.identity);
                // Update Box and light
                agentGroup[i].transform.GetChild(8).gameObject.active = agents[i].carryBox;
                agentGroup[i].transform.GetChild(7).GetChild(2).GetComponent<Light>().color = (agents[i].carryBox) ? Color.green : Color.red;

                
            }
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("numAgents", numAgents);

        UnityWebRequest www = UnityWebRequest.Post(url + configTP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }
}
