import java.net.*;
import java.io.*;
import java.util.HashMap;
import java.util.Map;

//Import custom packages.
import com.gracedp.operation.GraceDatabaseOperator;

/**
 * Program to listen to client's connections and respond accordingly depending on information provided.
 * to run this program successfully, type 
 * java -classpath .:com:postgresql-42.3.1.jar FormValidator
 */

public class FormValidator
{
    public static final int PORT = 8000;
    static final String URL = "jdbc:postgresql://localhost/grace_dp";
    static final String USERNAME = "zwi";
    static final String PASSWORD = "Zwi";
    static final String TABLE = "tenants_details";
    

    public static void main (String[] args)
    {
        //Variables to handle socket communication
        ServerSocket listener;
        Socket connection;

        try
        {
            listener = new ServerSocket(PORT);
            System.out.println("Listening on port " + PORT);

            while (true)
            {
                connection = listener.accept();

                String messageIn = readMessage(connection);

                System.out.println("Sending message back to client now");
                
                sendMessage(connection, messageIn); // static methods can be called without prefix.
                connection.close();
                
            }    
        }


        catch (Exception e)
        {
            System.out.println("Error: " + e);
        }

    }

    private static String readMessage (Socket client)
    {
        BufferedReader incoming;
        String messageIn;
        
        System.out.println("Connection from " + client.getInetAddress().toString());

        try
        {
            incoming = new BufferedReader( new InputStreamReader(client.getInputStream() ) );
            messageIn = incoming.readLine();

        }
        catch (Exception e)
        {
            messageIn = "x";
            System.out.println("Server says: " + e);
            
        }
        
        return messageIn;
    }

    private static void sendMessage (Socket client, String messageIn)
    {
        PrintWriter outgoing;

        //Convert messageIn to a Map. 
        Map< String, String > userCredentials;
        userCredentials = stringToMap (messageIn);

        String formType = userCredentials.get("FormType");
        
        try
        {
            outgoing = new PrintWriter(client.getOutputStream());

            switch (formType)
            {
                case "SignIn":
                    //Verify that message contains required info before sending a response back to client.
                    if (userCredentials.get("Password").equals("Zwi") )
                    {
                        outgoing.println("1");
                        outgoing.flush();
                    }
                    else
                    {
                        outgoing.println("0");
                        outgoing.flush();
                    }
                    break;

                case "Register":
                    //User info to be pushed to the database here.
                    GraceDatabaseOperator dbOperator = new GraceDatabaseOperator(URL, USERNAME, PASSWORD, TABLE);
                    int result;
                    
                    result = dbOperator.updateTable(userCredentials);
                        
                    if (result == 1)
                    {
                        outgoing.println("1");
                        outgoing.flush();
                    }
                    else 
                    {
                        outgoing.println("0");
                        outgoing.flush();
                    }
            }        
        }
        catch (Exception e)
        {
            System.out.println("Server says: " + e);
        }
    }

    private static Map< String, String > stringToMap (String message)
    {
        /**
         * Function to convert a comma separated string to a HashMap 
         */

        Map< String, String > messageMap = new HashMap < String, String > ();

        String[] commaTokens = message.split(",");

        for (String pairs : commaTokens)
        {
            String[] keyValuePair = pairs.split(" ");

            messageMap.put(keyValuePair[0], keyValuePair[1]);
        }

        return messageMap;
    }
}