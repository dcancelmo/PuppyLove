<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Puppy Love </title>
        <meta charset="UTF-8">
        <link rel = "stylesheet" type = "text/css" href = "style/styleDash.css" />
        <style>
            body {
                text-align: center;
                font-family: sans-serif;
            }
            form {
                padding-bottom: 30px;
            }
        </style>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
        $.ajax({
            type: "GET",
            url: "/cgi-bin/getLoginCookie.py",
            data: { param: " "},
            dataType: "text"
        }).done(function(response) {
            $('#welcomeMessage').html(response+ " is logged in")
        });

        function confirmDelete() {
            if (confirm("Are you sure? This CANNOT be reversed.") === true) {
                $.ajax({
                    type: "GET",
                    url: "/cgi-bin/delete.py",
                    data: { },
                    success: function (response) {
                        window.location.href = "./login.html";
                    },
                    error: function (jqXHR, textStatus, error) {
                        console.log("An error has occurred. " + jqXHR);
                    }
                });
//                window.location.href = "./cgi-bin/delete.py";
//                $.ajax({
//                    type: "POST",
//                    url: "/cgi-bin/delete.py",
//                    data: {username: document.getElementById("welcomeMessage").value},
//                    dataType: "text"
//                }).done(function(response) {
//                    window.location.href = "./login.html";
//                });
            }
        }
        
        function updateUserLocation(pos,radius){
          $.ajax({
                type: "GET",
                url: "/cgi-bin/UserLocation.py",
                data:{"longitude" : pos.longitude, "latitude" : pos.latitude, 
                    "radius" : radius},
                success: function(response){
                    console.log("Radius: "+ radius);
                    console.log("updatedUserLocation successfully");
                    console.log("response" + response);
                },
                error: function(){
                    console.log("halp");
                }
                
            });
        }
   
        //update their location when they update their profile to ensure all users have an updated location
        $(function getLocation(){
            if (navigator.geolocation) {
              navigator.geolocation.getCurrentPosition(function(position) {
                var pos = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude
                };
                
                
            
                radius = 17;
                console.log("Position: " + pos.lat);
                
                //updateUserLocation(position.coords, radius);
                $('#longitude').val(position.coords.longitude);
                $('#latitude').val(position.coords.latitude);
                $('#radius').val(radius);
                console.log("long, lat, radius updated to " + position.coords.longitude + ", " + position.coords.latitude + ", " + radius);
              }, function() {
                handleLocationError(true);
              });

            } else {
              // Browser doesn't support Geolocation
              handleLocationError(false);
            }
        });

        $.ajax({
                type: "GET",
                url: '/cgi-bin/getUserInfo.py',
                data: {param: " "},

                success: function(data){
                    var data = JSON.parse(data);
                    var userName = data.userName;
                    var name = data.humanName;
                    var humanPicSrc =data.humanPic;
                    var dogPicSrc = data.dogPic;
                    var dogName = data.dogName;
                    var genderPref = data.genderPref;
                    var gender = data.gender;
                    var description = data.description;
                    var phoneN = data.phoneNumber;
                    console.log(phoneN);
                    // '<img  src=\"data:;base64,'+humanPic.encode('base64')+'\"/>'
                    $('#username').val(name);
//                    $('#userPic').html('<img id="profilepic_img" width="500dp" src=\"data:;base64, ' + humanPicSrc + '\"/>');
                    $('#description').val(description);
                    $('#dogName').val(dogName);
//                    $('#dogPic').html('<img id="dogpic_img" width="250dp" src=\"data:;base64, ' + dogPicSrc + '\"/>');
                    switch(gender) {
                        case "male":
                            document.getElementById('male').checked = true;
                            break;
                        case "female":
                            document.getElementById('female').checked = true;
                            break;
                    }
                    switch(genderPref) {
                        case "male":
                            document.getElementById('maleP').checked = true;
                            break;
                        case "female":
                            document.getElementById('femaleP').checked = true;
                            break;
                        case "both":
                            document.getElementById('bothP').checked = true;
                            break;
                    }
                    $('#phone').val(phoneN);

                },
                error: function(jqXHR, textStatus, error){
                    console.log("error from getUserInfo")
                }
            });
    </script>
    <body>
        <div id = "header">
            <img src = "photos/logo.png" id = "logo">
            <h1> Update Profile </h1>
        </div>
        <?php include("navbar.php"); ?>

        <form action="/cgi-bin/updateInfo.py" method = "post" enctype="multipart/form-data">
            <h1 id="welcomeMessage"></h1>
            <h2> Your Name: </h2>
            <input type="text" name="username" id="username" required>
            <br>
            <h2> Profile Picture: </h2>
            <input type="file" name="userPic" id="userPic">
            <br>
            <h2> Your Dog's Name: </h2>
            <input type="text" name="dogName" id="dogName" required>
            <br>
            <h2> A Picture of your dog: </h2>
            <input type="file" name="dogPic" id="dogPic">
            <br>
            <h2> Add a description: </h2>
            <input type="text" name="description" id="description" size="40" required>
            <br>

            <h2> Your Gender: </h2>
            <input type="radio" name="gender" value="male" id="male" required> Male<br>
            <input type="radio" name="gender" value="female" id="female"> Female<br>
            
            <br>
            <h2> Who are you interested in?: </h2>
            <input type="radio" name="genderPref" value="male" id="maleP" required> Male<br>
            <input type="radio" name="genderPref" value="female" id="femaleP"> Female<br>
            <input type="radio" name="genderPref" value="both" id="bothP"> Both<br>
            <h2> Phone Number: </h2>
            <input type="text" name="phoneNumber" id="phone" required><br>
<!-- Hidden Location Inputs -->
            <input type="hidden" id="longitude" name="longitude" value="">
            <input type="hidden" id="latitude" name="latitude" value="">
            <input type="hidden" id="radius" name="radius" value="">
            <input type="text" name="newUser" value="false" required hidden>
            <button type="submit"> Update </button>

        </form>
        <h1 style="color: red"><strong> DELETE ACCOUNT </strong></h1>
        <br>
        <button id="delete" onclick=confirmDelete()> DELETE </button>
        <br><br>
    </body>
</html>
