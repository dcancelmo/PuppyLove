<!DOCTYPE html>
<html lang="en">
    <head>
        <title>View Profile</title>
        <meta charset="UTF-8">
        <link rel = "stylesheet" type = "text/css" href = "style/styleDash.css" />
        <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
        <script>
            $.ajax({
                type: "GET",
                url: "/cgi-bin/getLoginCookie.py",
                data: { param: " "},
                dataType: "text"
            }).done(function(response) {
                document.title = response;
                $("#profile_head").html(response + "'s Profile");

            });
            $.ajax({
                type: "GET",
                url: '/cgi-bin/getUserInfo.py',
                data: {param: " "},
                
                success: function(data){
                    $("#username").text("hiaefl");
                    var data = JSON.parse(data);
                    var userName = data.userName;
                    var name = data.humanName;
                    var humanPicSrc =data.humanPic;
                    var dogPicSrc = data.dogPic;
                    var dogName = data.dogName;
                    var genderPref = data.genderPref;
                    var gender = data.gender;
                    var description = data.description;
                    // '<img  src=\"data:;base64,'+humanPic.encode('base64')+'\"/>'
                    $('#human_name').text("Human name: " + name);
                    $('#profpic').html('<img id="profilepic_img" width="500dp" src=\"data:;base64, ' + humanPicSrc + '\"/>');
                    $('#profile_head').text("Welcome, " + name + "!");
                    $('#description').text("Description: " + description);
                    $('#dogs_name').text("Dog Name: " + dogName);
                    $('#dogpic').html('<img id="dogpic_img" width="250dp" src=\"data:;base64, ' + dogPicSrc + '\"/>');
                    $('#gender').text("Your gender: " + gender.charAt(0).toUpperCase() + gender.slice(1));
                    $('#gender_interest').text("Who you are interested in: " + genderPref.charAt(0).toUpperCase() + genderPref.slice(1));


//                    alert("User's name is " + data['humanName'] );
//                    console.log(data.humanName);
                    passGender(genderPref, gender, userName);
                },
                error: function(jqXHR, textStatus, error){
                    console.log("error from getUserInfo")
                }
            });
            function passGender(genderPref, gender, userName){
                $.ajax({
                    type: "GET",
                    url: '/cgi-bin/getPotentialMatches.py',
                    data: {"genderPref": genderPref,
                        "gender": gender, "userName" : userName},
                    success: function(){
                        //alert("Success: genderPref is " + genderPref);
                    },
                    error: function(jqXHR, textStatus, error){
                        console.log("Error from getPotentialMatches: " + error);
                        console.log("jqXHR: " + jqXHR);
                        console.log("Textstatus: " + textStatus);
                        alert ("ERROR");
                    }

                });
                
            }
        
            
        </script>
        <style>
            #profpic{
                width:55%;
                height:55%;
                margin-right:2%;
                float: left;
                
            }
            #profilepic_img{
                float: left;
                display: inline;
                /*width:30%;*/
                /*height: 40%;*/
                margin-left: 2%;
                margin-top: 2%;
                margin-bottom: 2%;
            }
            .description{
                display: inline;
                width:45%;
                margin-left: 2%;
                float: right;
            }
            .side{
                display: inline-block;
                /*border: 1px solid black;*/
                width:70%;
                height: 70%;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        <div id="header">
            <img src = "photos/logo.png" id = "logo">
            <h1 id="profile_head"></h1>
        </div>
        <?php include("navbar.php"); ?>
    </div>
        <!--<h2 id="profile_head"> </h2>-->
        <div class="side">
            <h2 id="human_name"></h2>
            <div id="profpic"></div>
            <h2 id="dogs_name"></h2>
            <div id="dogpic"></div>
            <h3 id="description"></h3>
            <h4 id="gender"></h4>
            <h4 id="gender_interest"></h4>
        </div>
    </body>
</html>