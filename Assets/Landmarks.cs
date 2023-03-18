using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Landmarks : MonoBehaviour
{
    public MyListener listener;

    int num;

    // Start is called before the first frame update
    void Start()
    {
        num = int.Parse(gameObject.name.Split("(")[1].Split(")")[0]);
    }

    // Update is called once per frame
    void Update()
    {
        if (gameObject.name.Contains("hand")) fetchHandLandmarks();
        if (gameObject.name.Contains("f(")) fetchFaceLandmarks();

    }

    void fetchHandLandmarks()
    {
        if (listener != null)
        {
            var pos = listener.landmarkList;
            if (pos.Capacity != 0 && num < pos.Capacity)
            {
                transform.position = pos[(pos.Capacity <= 21 && (num > 21)) ? num - 21 : num] * -5;
            }
        }

    }

    void fetchFaceLandmarks()
    {
        if (listener != null)
        {
            var pos = listener.landmarkList;
            if (pos.Capacity != 0 && num < pos.Capacity)
            {
                transform.position = pos[num];
            }
        }

    }
}
