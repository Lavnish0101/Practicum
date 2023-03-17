using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Threading;
using System.Text.RegularExpressions;
using System.Collections.Generic;

public class MyListener : MonoBehaviour
{
    Thread thread;
    public int connectionPort = 25001;
    TcpListener server;
    TcpClient client;
    bool running;
    List<Vector3> landmarkList;


    void Start()
    {
        // Receive on a separate thread so Unity doesn't freeze waiting for data
        ThreadStart ts = new ThreadStart(GetData);
        thread = new Thread(ts);
        thread.IsBackground = true;
        thread.Start();

        landmarkList=new List<Vector3>();
    }

    void GetData()
    {
        // Create the server
        server = new TcpListener(IPAddress.Any, connectionPort);
        server.Start();
        // Create a client to get the data stream
        client = server.AcceptTcpClient();

        // Start listening
        running = true;
        while (running)
        {
            Connection();
        }
        server.Stop();
    }

    void Connection()
    {
        // Read data from the network stream
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

        // Decode the bytes into a string
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);


        // Create a regular expression pattern that matches the individual arrays
        string pattern = @"\[(.*?)\]";
        Regex regex = new Regex(pattern);

        MatchCollection matches = regex.Matches(dataReceived);
        int numRows = matches.Count;
        double[,] array2D = new double[numRows, 4];
        for (int i = 0; i < numRows; i++)
        {
            string arrayString = matches[i].Groups[1].Value;
            string[] floatStrings = arrayString.Split(',');
            double number;
            for (int j = 0; j < floatStrings.Length; j++)
            {
                if (double.TryParse(floatStrings[j], out number))
                {
                    array2D[i, j] = number;
                }
                else
                {
                    array2D[i, j] = 0.0;
                }
            }
        }
        

        for (int i = 0; i < numRows; i++)
        {
            landmarkList.Add(new Vector3(((float)array2D[i,1]),((float)array2D[i,2]),((float)array2D[i,3])));
            Debug.Log(array2D[i, 0] + ", " + array2D[i, 1] + ", " + array2D[i, 2] + ", " + array2D[i, 3]);
        }

        // Make sure we're not getting an empty string
        //dataReceived.Trim();
        // if (dataReceived != null && dataReceived != "")
        // {
        //     // Convert the received string of data to the format we are using
        //     position = ParseData(dataReceived);
        //     nwStream.Write(buffer, 0, bytesRead);
        // }
    }


    // Use-case specific function, need to re-write this to interpret whatever data is being sent
    public static Vector3 ParseData(string dataString)
    {
        Debug.Log(dataString);
        // Remove the parentheses
        if (dataString.StartsWith("(") && dataString.EndsWith(")"))
        {
            dataString = dataString.Substring(1, dataString.Length - 2);
        }

        // Split the elements into an array
        string[] stringArray = dataString.Split(',');

        // Store as a Vector3
        Vector3 result = new Vector3(
            float.Parse(stringArray[0]),
            float.Parse(stringArray[1]),
            float.Parse(stringArray[2]));

        return result;
    }

    // Position is the data being received in this example
    Vector3 position = Vector3.zero;

    void Update()
    {
        // Set this object's position in the scene according to the position received
        transform.position = position;
    }
}