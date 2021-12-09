/**
 * Class to handle operation of the grace_dp database.
 * run javac -d . classname.java 
 * to compile
 */

 //Declare package name.
package com.gracedp.operation;

//Import useful java built in packages.
import java.sql.Connection;
import java.sql.Statement;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Map;
import java.util.Scanner;
import java.util.HashMap;

public class GraceDatabaseOperator 
{
    private String dbUrl;
    private String tableName;
    private String dbUsername;
    private String dbPassword;
    private Connection connection;

    //Declaration of the constructor.
    public GraceDatabaseOperator (String url, String username, String password, String table)
    {
        this.dbUrl = url;
        this.dbUsername = username;
        this.dbPassword = password;
        this.tableName = table;
        
        try
        {
            this.connection = DriverManager.getConnection(dbUrl, dbUsername, password);
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void queryTable ()
    {
        Statement queryStatement;
        ResultSet resultSet;

        try 
        {
            queryStatement = connection.createStatement();
            resultSet = queryStatement.executeQuery(
                "SELECT * FROM " + tableName);

            while ( resultSet.next() )
            {
                for ( int i = 1; i <= 5; i++)
                    System.out.printf("%-8s\t", resultSet.getObject(i));
                System.out.println();
            }

            queryStatement.close();
            resultSet.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        
    }

    public int updateTable (Map< String, String > mapCollection)
    {
        /**
         * Function to execute an update query which adds new row to a table and returns an integer giving the total number of rows added.
         */
        
        PreparedStatement updateStatement;
        int result = 0;

        try
        {
            //updateStatement = connectedness.createStatement();
            updateStatement = connection.prepareStatement(
                "INSERT INTO " + tableName + " ( name, surname, email, password ) " + " VALUES (?, ?, ?, ?) ");
            
            updateStatement.setString(1, mapCollection.get("Name"));
            updateStatement.setString(2, mapCollection.get("Surname"));
            updateStatement.setString(3, mapCollection.get("Email"));
            updateStatement.setString(4, mapCollection.get("Password"));
            
            result = updateStatement.executeUpdate();
            
            updateStatement.close();

        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        
        return result;
    }
} 