import java.net.*;
import java.io.*;
import java.util.Date;

/**
 * Program to perform rudimentary network programming to familiarise one with the concepts; this covers server side of the network.
 */

 public class DateServer
 {
    public static final int PORT = 32007;

    public static void main (String[] args)
    {
        ServerSocket listener;
        Socket connection;

        try
        {
            listener = new ServerSocket(PORT);
            System.out.println("Listening on port " + PORT);

            while (true)
            {
                connection = listener.accept();
                sendDate(connection);
            }
        }

        catch (Exception e)
        {
            System.out.println("Sorry, the server has shut down.");
            System.out.println("Error: " + e);
            return;
        }
    }

    private static void sendDate (Socket client)
    {
        try
        {
            System.out.println("Connection from " + client.getInetAddress().toString());

            Date now = new Date();

            PrintWriter outgoing;
            outgoing = new PrintWriter(client.getOutputStream());

            outgoing.println(now.toString());

            outgoing.flush();

            client.close();
        }

        catch (Exception e)
        {
            System.out.println("Error: " + e);
        }
    }
 }