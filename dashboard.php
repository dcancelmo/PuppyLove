<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
    <title>User Dashboard</title>
    <link rel = "stylesheet" type = "text/css" href = "style/styleDash.css" />
    <style>
            .match img{
                position: center;
                width:55%;
                height:55%;
                margin: 0 auto;
                display: block;
                
                
            }
           .match{
                position: relative;
                

                display: inline-block;
                border: 1px solid black;
                width:60%;
                height: 20%;
                overflow: hidden;
            }
            .human, .dog{
                position: relative;
                
                width: 50%;
                margin: 2px;
                float: left;
            }
           /*.like_or_hate{
                display: inline-block;
                position: relative;
                border: 1px solid black;
                width:60%;
                height: 20%;
                overflow: hidden;
           }*/
           .like_or_hate, .container{
                /*display: inline-block;
                position: relative;*/
                
                /*width:60%;
                height: 20%;*/
                margin-right: 2%;
                overflow: hidden;
           }
           .like_or_hate img{
                width: 50%;
                padding-bottom: 10%;
                padding-top: 5%;
           }
    </style>
<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
<script>

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
    $(function getLocation(){
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            
            
        
            radius = 30;
            console.log("Position: " + pos.lat);
            
            updateUserLocation(position.coords, radius);
          }, function() {
            handleLocationError(true);
          });

        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false);
        }
    });
    var refToGetUserInfoFunc = (function getUserInfo(){
     $.ajax({
                type: "GET",
                url: '/cgi-bin/getUserInfo.py',
                data: {param: " "},
                
                success: function(data){
                    
                    var data = JSON.parse(data);
                    //Logged In Users' information
                    var name = data.humanName;
                    var humanPicSrc =data.humanPic;
                    var dogPicSrc = data.dogPic;
                    var dogName = data.dogName;
                    var genderPref = data.genderPref;
                    var gender = data.gender;
                    var userName = data.userName;
                    var description = data.description;
                    var longitude = data.longitude;
                    var latitude = data.latitude;
                    var radius = data.radius;
                    $('#curr_username').val(userName);
                    $('#dashboard_welcome').text(name + "'s Dashboard");
                    //alert("User's name is " + data['humanName'] );
                   // console.log(data.humanName);
                    passGender(genderPref, gender, userName, longitude, latitude, radius);
                },
                error: function(jqXHR, textStatus, error){
                    console.log("error from getUserInfo")
                }
            });
        return getUserInfo;
     }());
            function passGender(genderPref, gender, userName, longitude, latitude, radius){
                $.ajax({
                    type: "GET",
                    url: '/cgi-bin/getPotentialMatches.py',
                    data: {"genderPref": genderPref, "gender" : gender, "userName" : userName,
                            "longitude": longitude, "latitude" : latitude, "radius" : radius},
                    success: function(data){
                        
                        console.log("genderpref: "+ genderPref);
                        console.log("gender: " + gender);
                        console.log("userName: " + userName);
                        var data = JSON.parse(data);
                        var num_potential_matches = Object.keys(data).length;
                        
                        htmlstring="";
                        $.each(data, function(i, item){
                            
                            console.log("item is: " + item['username']);
                            username = item['username'];
                            humanName = item['humanName'];
                            humanPic = item['userPic'];
                            dogPic = item['dogPic'];
                            distance = item['distance'];
                            distance = Number(Math.round(distance+'e2')+'e-2');
                            dogName = item['dogName'];
                            description = item['description'];
                            htmlstring += "<div class=\"match\" id=\"" +username + "\"><div class=\"human\"> <h2 class=\"humanName\"> Human: " + humanName + " </h2><br> <img class=\"profpic\" src=\"data:;base64, " + humanPic + "\"/></div><div class=\"dog\"> <h2 class=\"dogname\"> Dog:" + dogName + "</h2> <img class=\"dogpic\" src=\"data:;base64, " + dogPic + "\"/> </div> <br> <h2 class=\"description\">Description: </h2><br> <p> " + description + " <br> " + distance + " mi. Away</p>" + "<div class=\"like_or_hate\"> <div class=\"container\"><img class=\"like\" id=\"match_" + username + "\" src=\"photos/like.png\" onclick=\"like('" +username+"')\"></div><div class=\"container\"> <img class=\"hate\" id=\"pass_"+username +"\" src=\"photos/hate.png\"  onclick=\"pass('"+username+"')\"></div></div></div>";
                            
                        });
                        $('#users').append(htmlstring);
//                        console.log(htmlstring);
                        if (htmlstring === "") {
                            $('#users').append("No more available potential matches, sorry!");
                        }

                        
                        //alert("Success: genderPref is " + gender);
                        
                    },
                    error: function(jqXHR, textStatus, error){
                        console.log("Error from getPotentialMatches: " + error);
                        console.log("jqXHR: " + jqXHR);
                        console.log("Textstatus: " + textStatus);
                        alert ("ERROR");
                    }

                });
                
            }
            function like(username){
                //add to matches
                if (confirm("You really want to like " + username + "?")){
                    console.log("un: " + username);
                    $.ajax({
                        type: "GET",
                        url: '/cgi-bin/updateLikes.py',
                        data: {"liker" : "lludford", "likee": username, 'like_or_hate': "like"},
                        success: function(data){
                            var x = JSON.parse(data);
                            console.log("Success, data: " + x.success);
                            console.log("Response, data: " + x.response);
                            reloadPotentialMatches();
                            if(x.success == "True"){
                                alert("Congrats, It's a match!");
                            }

                        },
                        error: function(jqXHR, textStatus, error){
                            console.log("Error from like(): " + error);
                            console.log("jqXHR: " + jqXHR);
                            console.log("Textstatus: " + textStatus);
                            alert ("ERROR");
                        }
                            

                    });
                }
                
                
            }
    function reloadPotentialMatches(){
        $('#users').html('');
        refToGetUserInfoFunc();
    }
    function pass(username){
        //add to pass
        if(confirm("You really want to pass "+ username + "?")){
        
            console.log("un,pass: " + username);
            $.ajax({
                type: "GET",
                url: '/cgi-bin/updateLikes.py',
                //liker is useless, so dw, i use cookies to populate the 'liker'
                data: {"liker" : "lludford", "likee": username, 'like_or_hate': "hate"},
                success: function(data){
                    var x = JSON.parse(data);
                    console.log("Success, data: " + x.success);//is never a success bc they passed
                    reloadPotentialMatches();
                    
                },
                error: function(jqXHR, textStatus, error){
                    console.log("Error from like(): " + error);
                    console.log("jqXHR: " + jqXHR);
                    console.log("Textstatus: " + textStatus);
                    alert ("ERROR");
                }

            });
        }
    }
    
</script>

</head>
<body>
    <input type="hidden" id="curr_username" value="">
    <div id = "header">

        <img src = "photos/logo.png" id = "logo">
        <h1 id="dashboard_welcome"> Dashboard </h1>
    </div>
    <?php include 'navbar.php'; ?>
    <div id = "users">
        <div id = "profile_pic">
        </div>
        <div id = "profile_info">
        </div>
        <div id = "buttons">
        </div>
    </div>
</body>
</html>