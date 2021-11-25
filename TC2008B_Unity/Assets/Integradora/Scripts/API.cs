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

    public int direction = 0;

    public bool carryBox;
}

[Serializable]
public class Box
{
    public float x;
    public float y;
    public float z;

    public bool active;
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
    [SerializeField] string getAgentsEP;
    [SerializeField] string getBoxesEP;
    [SerializeField] string configEP;
    [SerializeField] string stepEP;
    [SerializeField] string updateAgentsEP;
    [SerializeField] string updateBoxesEP;
    [SerializeField] int numAgents;
    [SerializeField] int numBoxes;
    [SerializeField] GameObject catBoy;
    [SerializeField] GameObject happyMeal;

    Agent[] agents;
    Box[] boxes;

    GameObject[] agentGroup;
    GameObject[] boxGroup;

    bool gotAgents = false;
    bool gotBoxes = false;
    [SerializeField] float timeToWait = 1;
    [SerializeField] float timeElapsed;
    List <Vector3> newPositions;
    List <Vector3> ogPositions;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(SendConfiguration());

        newPositions = new List<Vector3>();
        ogPositions = new List<Vector3>();

        agentGroup = new GameObject[numAgents];
        boxGroup = new GameObject[numBoxes];


        StartCoroutine(GetAgents());
        StartCoroutine(GetBoxes());

    }

    // Update is called once per frame
    void Update()
    {
        
        timeElapsed += Time.deltaTime;
        if (gotAgents && gotBoxes){
            float t = timeElapsed/timeToWait;
            if (timeElapsed >= timeToWait)
            {
                timeElapsed = 0;
                StartCoroutine(MakeStep());
            }
            
            for (int i = 0; i < agentGroup.Length; i++)
            {
                agentGroup[i].transform.position = Vector3.Lerp(agentGroup[i].transform.position, newPositions[i], t);
            }
            
        }


    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("numAgents", numAgents);
        form.AddField("numBoxes", numBoxes);

        UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator MakeStep()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + stepEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            yield return StartCoroutine(UpdateAgents());
            yield return StartCoroutine(UpdateBoxes());
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator GetAgents()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + getAgentsEP);
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
                agentGroup[i].transform.rotation = Quaternion.Euler(0, agents[i].direction, 0);
                // Update Box and light
                agentGroup[i].transform.GetChild(8).gameObject.SetActive(false);
                agentGroup[i].transform.GetChild(7).GetChild(2).GetComponent<Light>().color = new Color(246f/255f, 31f/255f, 29f/255f);
            }
            gotAgents = true;
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator GetBoxes()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + getBoxesEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            boxes = JsonHelper.FromJson<Box>(www.downloadHandler.text);
            for (int i = 0; i < numBoxes; i++)
            {
                // Update direction
                Vector3 temp = new Vector3(boxes[i].x, boxes[i].y, boxes[i].z);
                boxGroup[i] = Instantiate(happyMeal, temp, Quaternion.identity);
            }
            gotBoxes = true;
        }else
        {
            Debug.Log(www.error);
        }
    }


    IEnumerator UpdateAgents()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateAgentsEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            agents = JsonHelper.FromJson<Agent>(www.downloadHandler.text);
            newPositions.Clear();
            ogPositions.Clear();
            for (int i = 0; i < numAgents; i++)
            {
                // Update direction
                agentGroup[i].transform.rotation = Quaternion.Euler(0, agents[i].direction, 0);
                Vector3 pos1 = new Vector3(agents[i].x, agents[i].y, agents[i].z);
                ogPositions.Add(agentGroup[i].transform.position);
                newPositions.Add(pos1);
                
                
                // Update Box and light
                agentGroup[i].transform.GetChild(8).gameObject.SetActive(agents[i].carryBox);
                agentGroup[i].transform.GetChild(7).GetChild(2).GetComponent<Light>().color = (agents[i].carryBox) ? new Color(33f/255f, 84f/255f, 25f/255f) : new Color(246f/255f, 31f/255f, 29f/255f);
            }
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator UpdateBoxes()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateBoxesEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            boxes = JsonHelper.FromJson<Box>(www.downloadHandler.text);
            for (int i = 0; i < numBoxes; i++)
            {
                // Update direction
                Vector3 pos1 = new Vector3(boxes[i].x, boxes[i].y, boxes[i].z);
                boxGroup[i].transform.position = pos1;  
                boxGroup[i].SetActive(boxes[i].active); 
            }
        }else
        {
            Debug.Log(www.error);
        }
    }

}