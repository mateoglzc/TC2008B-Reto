using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class Car
{
    public float x;
    public float y;
    public float z;

    public void print()
    {
        Debug.Log(String.Format("{0} {1} {2}", x, y, z));
    }

    public int direction = 0;
}

[Serializable]
public class TrafficLight
{
    public float x;
    public float y;
    public float z;

    public string state; 
}

public class RetoAPI : MonoBehaviour
{

    [SerializeField] int numCars;
    [SerializeField] string url;
    [SerializeField] string getCarsEP;
    [SerializeField] string getTrafficLightsEP;
    [SerializeField] string configEP;
    [SerializeField] string stepEP;
    [SerializeField] string testEP;
    [SerializeField] GameObject car;
    [SerializeField] GameObject trafficLight;
    [SerializeField] float timeToWait;
    [SerializeField] float timeElapsed;

    int numTrafficLights = 28;
    bool gotCars;

    Car[] cars;
    GameObject[] carGroup;

    TrafficLight[] trafficLights;
    GameObject[] trafficLightGroup;

    List<Vector3> newPos;
    List<Vector3> oldPos;

    // Start is called before the first frame update
    void Start()
    {
        // Init variables
        gotCars = false;
        timeToWait = 1;
        newPos = new List<Vector3>();
        oldPos = new List<Vector3>();
        carGroup = new GameObject[numCars];
        trafficLightGroup = new GameObject[numTrafficLights];

        Debug.Log("Variables Init");

        // Test Connection
        // Send Configuration
        StartCoroutine(SendConfiguration());

        // Init Cars
        StartCoroutine(InitCars());
        StartCoroutine(InitTrafficLights());
        
    }

    // Update is called once per frame
    void Update()
    {
        timeElapsed += Time.deltaTime;
        if (gotCars){
            float t = timeElapsed/timeToWait;
            if (timeElapsed >= timeToWait)
            {
                timeElapsed = 0;
                StartCoroutine(MakeStep());
            }
            
            for (int i = 0; i < carGroup.Length; i++)
            {
                // carGroup[i].transform.position = Vector3.Lerp(carGroup[i].transform.position, newPos[i], t);
                // carGroup[i].transform.position = newPos[i];
                // Debug.Log(carGroup[i].transform.position);
            }
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("numCars", numCars);

        UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator InitCars()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + getCarsEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            cars = JsonHelper.FromJson<Car>(www.downloadHandler.text);
            for (int i = 0; i < numCars; i++)
            {
                Vector3 pos = new Vector3(cars[i].x, cars[i].y, cars[i].z);
                carGroup[i] = Instantiate(car, pos, Quaternion.identity);
                carGroup[i].transform.rotation = Quaternion.Euler(0, cars[i].direction, 0);
            }
            gotCars = true;
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator UpdateCars()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + getCarsEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            cars = JsonHelper.FromJson<Car>(www.downloadHandler.text);
            for (int i = 0; i < numCars; i++)
            {

                Vector3 pos = new Vector3(cars[i].x, cars[i].y, cars[i].z);
                carGroup[i].transform.rotation = Quaternion.Euler(0, cars[i].direction, 0);
                carGroup[i].transform.position = pos;
                oldPos.Add(carGroup[i].transform.position);
                newPos.Add(pos);
            }
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator InitTrafficLights()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + getTrafficLightsEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            trafficLights = JsonHelper.FromJson<TrafficLight>(www.downloadHandler.text);
            for (int i = 0; i < numTrafficLights; i++)
            {
                Vector3 pos = new Vector3(trafficLights[i].x, trafficLights[i].y, trafficLights[i].z);
                trafficLightGroup[i] = Instantiate(trafficLight, pos, Quaternion.identity);
            }
        }else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator UpdateLights()
    {
        UnityWebRequest www = UnityWebRequest.Get(url +  getTrafficLightsEP);
        yield return www.SendWebRequest();
        
        if (www.result == UnityWebRequest.Result.Success)
        {
            bool light;
            trafficLights = JsonHelper.FromJson<TrafficLight>(www.downloadHandler.text);
            for (int i = 0; i < numTrafficLights; i++)
            {

                light = (trafficLights[i].state == "green") ? true : false;
                // Traffic Light is supposes to be in green
                trafficLightGroup[i].transform.GetChild(0).GetChild(2).GetChild(0).gameObject.SetActive(light);
                trafficLightGroup[i].transform.GetChild(0).GetChild(2).GetChild(2).gameObject.SetActive(!light);

            }
        }else
        {
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
            yield return StartCoroutine(UpdateCars());
            yield return StartCoroutine(UpdateLights());
        }else
        {
            Debug.Log(www.error);
        }
    }
}
