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

    public int direction = 0;
}

public class RetoAPI : MonoBehaviour
{

    [SerializeField] int numCars;
    [SerializeField] string url;
    [SerializeField] string getCarsEP;
    [SerializeField] string configEP;
    [SerializeField] string testEP;
    [SerializeField] GameObject donkey;
    [SerializeField] float timeToWait;
    [SerializeField] float timeElapsed;

    bool gotCars;

    Car[] cars;
    GameObject[] carGroup;

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

        // Test Connection
        // Send Configuration
        StartCoroutine(SendConfiguration());

        // Init Cars
        StartCoroutine(InitCars());
        
    }

    // Update is called once per frame
    void Update()
    {
        
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
            Debug.Log(www.downloadHandler.text);
            cars = JsonHelper.FromJson<Car>(www.downloadHandler.text);
            for (int i = 0; i < numCars; i++)
            {
                // Update direction
                Vector3 temp = new Vector3(cars[i].x, cars[i].y, cars[i].z);
                carGroup[i] = Instantiate(donkey, temp, Quaternion.identity);
                carGroup[i].transform.rotation = Quaternion.Euler(0, cars[i].direction, 0);
            }
            gotCars = true;
        }else
        {
            Debug.Log(www.error);
        }
    }
}
