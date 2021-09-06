function pageLoad()
{
    
}


function submitForm()
{
    var x = document.getElementById("name").value;

    alert(x);
}

function loadFunction()
{
    var path = window.location.pathname;
    var page = path.split("/").pop();

    switch(page)
    {
        case "register":
            alert("Please enter your details in order to create an account with us.");
            document.style.backgroundColor = 'black';
            document.body.style.backgroundImage = "App_icon_3.png";
            break;

        case "sign-in":
            alert("here");
            if (confirm("Are you registered?"))
            {
                alert("Please use your email as username and password as your given password upon registration");
            }
            else
            {
                continue;
            }
            
            break;
    }
}

function signIn()
{
    var username = document.getElementById("username").value;
    var passord = document.getElementById("password").value;

    var sign_in = {}
    sign_in.username = username;
    sign_in.passord = passord;


}