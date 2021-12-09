//import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'dart:io';

void main (){

  runApp(const MyApp());
}

class MyApp extends StatelessWidget{

  const MyApp({Key? key}) : super(key : key);

  @override
  Widget build(BuildContext context){
    const appTitle = '';

    return MaterialApp(
      title: appTitle,
      theme: ThemeData.dark(),
      home: MyHomePage(),
    );
  }
}

//Definition of the App landing page.
class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  MyHomePageState createState() {
    return MyHomePageState();
  }
}

class MyHomePageState extends State<MyHomePage> {

  @override
  Widget build(BuildContext context) {

    return Scaffold(
        appBar: AppBar(
        title: Center(child: Text(
          'Grace',
          style: TextStyle(fontSize: 40, ),),),
    ),
    body: Center(
      child: Padding(
        padding: EdgeInsets.symmetric(vertical: 160, horizontal: 0),
        child: Column(
          children: [
            Text(
              'Welcome',
              style: TextStyle(fontSize: 32, color: Colors.green),
            ),
            ElevatedButton(
                onPressed: () {Navigator.push(context, MaterialPageRoute(builder: (context) => SignInForm()));},
                child: Text('Sign In')
            ),
            ElevatedButton(onPressed: () {Navigator.push(context, MaterialPageRoute(builder: (context) => RegistrationForm()));},
                child: Text('Register')
            )
          ],
        ),
      )


    )
    );
  }
}

//Definition of the signIn form begins here.
class SignInForm extends StatefulWidget {
  const SignInForm({Key? key}) : super(key: key);

  @override
  SignInFormState createState() {
    return SignInFormState();
  }
}

//Definition of SignInFormState begins here.
class SignInFormState extends State<SignInForm> {
  final _formkey = GlobalKey<FormState>();
  final TextEditingController _controllerUsername = TextEditingController();
  final TextEditingController _controllerPassword = TextEditingController();

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: Center(child: Text(
            'Sign In',
            style: TextStyle(fontSize: 32),),),
      ),
      body: Form (
        key: _formkey,
        child: ListView(
          //crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(padding: EdgeInsets.symmetric(vertical: 16, horizontal: 8),
            child: TextFormField(
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              }, // validator ends
              controller: _controllerUsername,
              decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Username'),
            ),
            ),
            Padding(padding: EdgeInsets.symmetric(vertical: 16, horizontal: 8),
            child: TextFormField(
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
              obscureText: true,
              controller: _controllerPassword,
              decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Password'),
            ),
            ),

            Center(
              child: ElevatedButton(
                onPressed: _submitSignInForm,
                child: const Text("Submit"),
              ),
            ),
          ], // Children list
        ),
      ),
    );
  }

  void _submitSignInForm() async {
    if (_formkey.currentState!.validate()) {
      //Socket sock = await Socket.connect('3.16.36.117', 8000);
      Socket sock = await Socket.connect('10.0.0.109', 8000);
      //sock.write(_controllerUsername.text);

      sock.writeln("Username " +_controllerUsername.text + "," +
                    "Password " + _controllerPassword.text + "," +
                    "FormType SignIn");
      await sock.flush();

      sock.listen((Uint8List data) {
        var serverResponse = String.fromCharCodes(data);
        var successErrorResponse;

        if (serverResponse.contains("1")) {
          successErrorResponse = 'Success';
          Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => MainDashBoard(name: _controllerUsername.text,)));
              //MaterialPageRoute(builder: (context) => FormSubmissionResult(response: successErrorResponse,)));
        }
        else {
          successErrorResponse = 'Incorrect';
          Navigator.push(
              context,
              //MaterialPageRoute(builder: (context) => MainDashBoard()));
              MaterialPageRoute(builder: (context) => FormSubmissionResult(response: successErrorResponse,)));
        }

      },
          onError: (error) {print(error);}
      );

      sock.close();
    }
  }
}


//Definition of Registration form begins here.
class RegistrationForm extends StatefulWidget {
  const RegistrationForm({Key? key}) : super(key: key);

  @override
  RegistrationFormState createState () {
    return RegistrationFormState();
  }
}

class RegistrationFormState extends State<RegistrationForm> {
  final _formkey = GlobalKey<FormState>();
  final TextEditingController _controllerName = TextEditingController();
  final TextEditingController _controllerSurname = TextEditingController();
  final TextEditingController _controllerEmail = TextEditingController();
  final TextEditingController _controllerCell = TextEditingController();
  final TextEditingController _controllerPassword0 = TextEditingController();
  final TextEditingController _controllerPassword1 = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(child: Text('Registration'),),
      ),
      body: Form (
        key: _formkey,
        child: ListView(
          //Initially a Column Widget was used, but had issues with rendering on screen.
          //crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(padding: EdgeInsets.symmetric(vertical: 16, horizontal: 8),
              child: TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter some text';
                  }
                  return null;
                }, // validator ends
                controller: _controllerName,
                decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Name'),
              ),
            ),
            Padding(padding: EdgeInsets.symmetric(vertical: 16, horizontal: 8),
              child: TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter some text';
                  }
                  return null;
                },
                controller: _controllerSurname,
                decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Surname'),
              ),
            ),
            Padding(padding: EdgeInsets.symmetric(vertical: 16, horizontal: 8),
              child: TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter some text';
                  }
                  return null;
                },
                controller: _controllerEmail,
                decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Email Address'),
              ),
            ),
            Padding(padding: EdgeInsets.symmetric(vertical: 16, horizontal: 8),
              child: TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter some text';
                  }
                  return null;
                },
                controller: _controllerCell,
                decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Cell Number'),
              ),
            ),
            Padding(padding: EdgeInsets.symmetric(vertical: 16, horizontal: 8),
              child: TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter some text';
                  }
                  return null;
                },
                obscureText: true,
                controller: _controllerPassword0,
                decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Password'),
              ),
            ),
            Padding(padding: EdgeInsets.symmetric(vertical: 16, horizontal: 8),
              child: TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter some text';
                  }
                  return null;
                },
                obscureText: true,
                controller: _controllerPassword1,
                decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Confirm Password'),
              ),
            ),

            Center(
              child: ElevatedButton(
                onPressed: _submitRegistrationForm,
                child: const Text("Submit"),
              ),
            ),
          ], // Children list
        ),
      ),
    );
  }

  void _submitRegistrationForm () async {

    if (_formkey.currentState!.validate()) {
      //First setup a socket connection to the server listening on the other side.
      //Socket socket = await Socket.connect('3.16.36.117', 8000);
      Socket socket = await Socket.connect('10.0.0.109', 8000);

      //Write the users' registration details into a comma separated string.
      //First ensure passwords entered match.
      if (_controllerPassword0.text.contains(_controllerPassword1.text)) {
        socket.writeln("Name " + _controllerName.text + "," +
            "Surname " + _controllerSurname.text + "," +
            "Email " + _controllerEmail.text + "," +
            "Password " + _controllerPassword0.text + "," +
            "CellNo " + _controllerCell.text + "," +
            "FormType Register");
        await socket.flush();

        socket.listen((Uint8List data) {
          final serverResponse = String.fromCharCodes(data);

          //test if form was submitted successfully.
          if (serverResponse.contains("1")){
            Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => MainDashBoard(name:_controllerName.text,)));
          }

          //If error occurred redirect to error page.
          else{
            Navigator.push(
                context,
                //MaterialPageRoute(builder: (context) => MainDashBoard()));
                MaterialPageRoute(builder: (context) => FormSubmissionResult(response: "Error",)));
          }
        },
            onError: (error) {print(error);
            }
        );
      }

      //If passwords don't match redirect to homepage.
      else {
        Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => MyHomePage())
        );
      }
      socket.close();
    }
  }
}

//class to navigate onto after submission of form.
class FormSubmissionResult extends StatefulWidget {
  final String response;
  const FormSubmissionResult({Key? key, required this.response}) : super(key: key);

  @override
  FormSubmissionResultState createState () {
    return FormSubmissionResultState();
  }
}

class FormSubmissionResultState extends State<FormSubmissionResult> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(child: Text(''),),
      ),
      body: Center(
        child: Column(
            children: [
              Text(
                widget.response,
                style: TextStyle(fontSize: 32),
              ),
              ElevatedButton(onPressed: () { Navigator.pop(context);}, child: Text('Go Back'))
            ]
        ),
      )
    );
  }
}

//Definition of the Main Dashboard page.MyHomePage
class MainDashBoard extends StatefulWidget {
  final String name;
  const MainDashBoard({Key? key, required this.name}) : super(key : key);

  @override
  MainDashBoardState createState() {
    return MainDashBoardState();
  }
}

class MainDashBoardState extends State<MainDashBoard> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text(
          'Welcome ' + widget.name,
          style: TextStyle(fontSize: 32, color: Colors.green),
        ),)
      ),
      body: Center(
        child: Container(
          decoration: const BoxDecoration(color: Colors.black, shape: BoxShape.rectangle),
          child: ListView(
            children: [
              Container(
                decoration: const BoxDecoration(color: Colors.blue, shape: BoxShape.circle),
                child: Text(
                    'Here',
                    style: TextStyle(fontSize: 25, color: Colors.green),
                ),
              ),
              Container(
                decoration: const BoxDecoration(color: Colors.green, shape: BoxShape.circle),
                child: Text(
                  'Here',
                  style: TextStyle(fontSize: 25, color: Colors.green),),
              ),
            ],
          ),
        ),
      ),
    );
  }
}