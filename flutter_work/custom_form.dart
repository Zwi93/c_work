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
    const appTitle = 'Grace DP';

    return MaterialApp(
      title: appTitle,
      //color: Colors.black,
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
          'GraceDp',
          style: TextStyle(fontSize: 40, color: Colors.yellow),)
          ,),
          //backgroundColor: Colors.black87,
    ),
    body: Center(
      child: Padding(
        padding: EdgeInsets.symmetric(vertical: 160, horizontal: 0),
        child: Column(
          children: [
            Text(
              'Hello.',
              style: TextStyle(fontSize: 60, color: Colors.green),
            ),
            ElevatedButton(
              onPressed: () {Navigator.push(context, MaterialPageRoute(builder: (context) => RegistrationForm()));},
              child: Text('Register', style: TextStyle(fontSize: 20),),
              //style: ButtonStyle(backgroundColor: ),
            ),
            Text("Already a Grace customer?", style: TextStyle(fontSize: 20),),
            ElevatedButton(
              onPressed: () {Navigator.push(context, MaterialPageRoute(builder: (context) => SignInForm()));},
              child: Text('Sign In', style: TextStyle(fontSize: 20),),
              //style: ButtonStyle(backgroundColor: ),
            ),
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
      body: Padding(
        padding: EdgeInsets.symmetric(vertical: 160, horizontal: 0),
        child: Form (
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
      )

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
                  if (value != _controllerPassword0.text) {
                    return 'Please enter matching passwords';
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
            onError: (error) {
          print(error);
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

//class to navigate onto after submission of form. Useless now.
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

  //Get the current time of day in string format.
  String today = DateTime.now().toString().split(' ')[0];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(
            Icons.menu,
            semanticLabel: 'menu',
          ),
          onPressed: () {
            showDialog(
                context: context,
                builder: (BuildContext context) => _popupMenu(),
                barrierColor: Colors.black87,
                barrierDismissible: false,
            );
          },
        ),
        title: Center(
          child: Text(
          widget.name,
          style: TextStyle(fontSize: 32, color: Colors.yellowAccent),
        ),
        ),
        actions: [

        ],
      ),
      /*bottomNavigationBar: BottomNavigation() No longer necessary*/
      persistentFooterButtons: [
        Container(
            child: Column(
              children: [
                Icon(
                  Icons.dashboard,
                ),
                TextButton(
                  onPressed: () {
                    Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => MainDashBoard(name: widget.name,))
                    );
                  },
                  child: Text("Dashboard"),
                ),
              ],
            )
        ),
        Container(
          child: Column(
        children: [
          Icon(
        Icons.checklist,
        ),
          TextButton(
            onPressed: () {},
            child: Text("ToDo"),
          ),
        ],
          )
        ),
        Container(
          child: Column(
          children: [
            Icon(Icons.chat_bubble_rounded,),
            TextButton(
              onPressed: () {},
              child: Text("Complaint"),
            ),
    ],
    )

        ),
        Container(
          child: Column(
            children: [
              Icon(
                Icons.warning_amber_rounded,
              ),
              TextButton(
                onPressed: () {},
                child: Text("Maintenance"),
              ),
            ],
          )

        ),
      ],
      body: Center(
        child: Container(
          decoration: const BoxDecoration(color: Colors.black12, shape: BoxShape.rectangle),
          child: ListView(
            children: [
              Container(
                decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.rectangle),
                  padding: const EdgeInsets.only(bottom: 10, top: 10),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text("Current Deposit:", style: TextStyle(fontSize: 15, color: Colors.black),),
                            Text("R10 000", style: TextStyle(fontSize: 20, color: Colors.blue),),
                            Text("Tenant's Rating:", style: TextStyle(fontSize: 15, color: Colors.black),),
                            Icon(Icons.star, color: Colors.blue,size: 15,),
                            Text("Occupation date: ", style: TextStyle(fontSize: 15, color: Colors.black), ),
                            Text(today, style: TextStyle(fontSize: 15, color: Colors.blue),)
                          ],
                        ),
                        Container(
                          decoration: const BoxDecoration(
                              color: Colors.blue,
                              shape: BoxShape.circle,
                              border: Border(top: BorderSide(color: Colors.black), left: BorderSide(color: Colors.black), right: BorderSide(color: Colors.black), bottom: BorderSide(color: Colors.black)),
                          ),
                          height: 50.0,
                          width: 50.0,
                          margin: const EdgeInsets.only(left: 100),
                          padding: const EdgeInsets.only(left: 100),
                          child: Text("Here", style: TextStyle(fontSize: 10, color: Colors.black),),
                        )
                      ],
                    )
                  ],
                )
              ),
              _products("Deposit Protection"),
              _products("Deposit Lending"),
              _products("Home Saver"),
              _products("Name Four"),
              //_products("Name Five"),
              //_products("Name Six")
            ],
          ),
        ),
      ),
    );
  }

  //Widget for the popup menu defined here.
  Widget _popupMenu (){
    return Container(
      //decoration: BoxDecoration(color: Colors.black),
      padding: EdgeInsets.symmetric(vertical: 160, horizontal: 0),
      child:Column(
          children: [
            TextButton(
              onPressed: () {

              },
              child: Text("Profile"),
            ),
            TextButton(
                onPressed: () {

                },
                child: Text("Something")
            ),
            TextButton(
                onPressed: () {
                  Navigator.of(context).pushNamedAndRemoveUntil('/', (route) => false);
                },
                child: Text("Logout"))
          ]
      ),

      //height: 100,
      //width: 100,
      );
}

  //Widget to build product icon depending on the name of the product
  Widget _productIcon (String productName) {
    switch (productName) {
      case 'Deposit Protection':
        return Icon(Icons.privacy_tip, size: 50,);
        break;
      case 'Deposit Lending':
        return Icon(Icons.credit_card, size: 50,);
        break;
      case 'Home Saver':
        return Icon(Icons.home, size: 50,);
        break;
      default:
        return Text("data");
    }
  }

  //Widget to build products container.
  Widget _products (String productName) {

    //Depending on the product name, the icon will vary.

    return Container(
      decoration: const BoxDecoration(
        shape: BoxShape.rectangle,
        border: Border(top: BorderSide(color: Colors.white), left: BorderSide(color: Colors.white), right: BorderSide(color: Colors.white), bottom: BorderSide(color: Colors.white)),
        borderRadius: BorderRadius.all(Radius.circular(10) ),
      ),
      //padding: const EdgeInsets.only(right: 100), //works for the children inside this container.
      margin: const EdgeInsets.all(10),  // gives the inner margin as measured from all sides.
      child: Column(
        children: [
          Text(
            productName,
            style: TextStyle(fontSize: 25, color: Colors.yellowAccent),
          ),
          Container(
            //decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.rectangle, ),
            height: 50.0,
            width: 50.0,
            child: _productIcon(productName), //or home_outlined.
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Expanded(child:
              ElevatedButton(
                  onPressed: () {
                    showDialog(
                        context: context, 
                        builder: (BuildContext context) => Center(child: Text("On the way!"),));
                  },
                  style: ButtonStyle(
                      backgroundColor: MaterialStateProperty.resolveWith((states) => Colors.black12),
                      foregroundColor: MaterialStateProperty.resolveWith((states) => Colors.white),
                      side: MaterialStateProperty.resolveWith((states) => BorderSide(color: Colors.white))
                  ),
                  child: Text('Get Product')
              ),
              ),
              Expanded(child:
              ElevatedButton(
                  onPressed: () {
                    showDialog(
                        context: context,
                        builder: (BuildContext context) => Center(child: Text("On the way!"),));
                  },
                  style: ButtonStyle(
                      backgroundColor: MaterialStateProperty.resolveWith((states) => Colors.black12),
                      foregroundColor: MaterialStateProperty.resolveWith((states) => Colors.white),
                      side: MaterialStateProperty.resolveWith((states) => BorderSide(color: Colors.white))
                  ),
                  child: Text('More Info')
              )
              )

            ],
          )
        ],
      ),
    );
  }

}