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

[Serializable]
public class Box
{
    public float x;
    public float y;
    public float z;
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
    [SerializeField] string agentTP;
    [SerializeField] string boxTP;
    [SerializeField] string configTP;
    [SerializeField] string updateTP;
    [SerializeField] int numAgents;
    [SerializeField] int numBoxes;
    [SerializeField] GameObject catBoy;
    [SerializeField] GameObject happyMeal;

    Agent[] agents;
    Box[] boxes;

    GameObject[] agentGroup;
    GameObject[] boxGroup;

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
        // StartoutCorine(GetAgents());
        
        
    }

    IEnumerator GetAgents()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + agentTP);
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
                agentGroup[i].transform.GetChild(8).gameObject.SetActive(agents[i].carryBox);
                agentGroup[i].transform.GetChild(7).GetChild(2).GetComponent<Light>().color = (agents[i].carryBox) ? Color.green : Color.red;

            }
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator GetBoxes()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + boxTP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            boxes = JsonHelper.FromJson<Box>(www.downloadHandler.text);
            for (int i = 0; i < numAgents; i++)
            {
                // Update direction
                Vector3 temp = new Vector3(boxes[i].x, boxes[i].y, boxes[i].z);
                boxGroup[i] = Instantiate(happyMeal, temp, Quaternion.identity);
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
        form.AddField("numBoxes", numBoxes);

        UnityWebRequest www = UnityWebRequest.Post(url + configTP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }

    // IEnumerator UpdateAgents()
    // {
        // UnityWebRequest www = UnityWebRequest.Get(url + testTP);
        // yield return www.SendWebRequest();

        // if (www.result == UnityWebRequest.Result.Success)
        // {

        //     agents = JsonHelper.FromJson<Agent>(www.downloadHandler.text);
        //     for (int i = 0; i < numAgents; i++)
        //     {
        //         // Update direction
        //         Vector3 pos1 = new Vector3(agents[i].x, agents[i].y, agents[i].z);
        //         // Make translation
        //         Vector4 homoVect = Transform.MakeHomogenousVectors(temp);
        //         // agentGroup[i].transform.position = Transform.MakeTranslation(agent)
        //         // Update Box and light
        //         agentGroup[i].transform.GetChild(8).gameObject.SetActive(agents[i].carryBox);
        //         agentGroup[i].transform.GetChild(7).GetChild(2).GetComponent<Light>().color = (agents[i].carryBox) ? Color.green : Color.red;

                
        //     }
        // }else
        // {
        //     Debug.Log(www.error);
        // }
    // }

}
