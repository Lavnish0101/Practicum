using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Landmarks2 : MonoBehaviour
{
    public Listener2 listener;

    int num;

    // Start is called before the first frame update
    void Start()
    {
        num = int.Parse(gameObject.name.Split("(")[1].Split(")")[0]);
    }

    // Update is called once per frame
    void Update()
    {
         fetchHandLandmarks();
        //fetchFaceLandmarks();

    }

    void fetchHandLandmarks()
    {
        if (listener != null)
        {
            var pos = listener.landmarkList;
            if (pos.Capacity != 0 && num < pos.Capacity)
            {
                transform.position = pos[num] * -4.25;
            }
        }

    }

    
}
