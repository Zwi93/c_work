import java.net.*;
import java.io.*;

/**
 * Partner script to the DateServer program; this is the client endpoint of the network communication.
 */

 public class DateClient
 {
    public static final int PORT = 32007;

    public static void main (String[] args)
    {
        String hostName;
        Socket connection;
        BufferedReader incoming;

        if (args.length > 0)
        {
            hostName = args[0];
        }
        else
        {
            System.out.println("Usage: java DateClient <server_host_name>");
            return;
        }

        try
        {
            connection = new Socket(hostName, PORT);
            incoming = new BufferedReader(new InputStreamReader(connection.getInputStream()));

            String lineFromServer = incoming.readLine();

            if (lineFromServer == null)
            {
                throw new IOException("Connection was opened, " + "but server did not send any data");
            }

            System.out.println();
            System.out.println(lineFromServer);
            System.out.println();
            incoming.close();
        }
        catch(Exception e)
        {
            System.out.println("Error: " + e);
        }
    }
 }