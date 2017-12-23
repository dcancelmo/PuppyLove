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
           #unmatch{
                width:50%;
           }
    </style>
<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
<script>

    
    $(function getUserInfo(){
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
                    
                    var userName = data.userName;
                    var description = data.description;
                    
                    $('#curr_username').val(userName);
                    $('#matches_welcome').text(name + "'s Matches");
                    //alert("User's name is " + data['humanName'] );
                   // console.log(data.humanName);
                    updateMatches(userName);
                },
                error: function(jqXHR, textStatus, error){
                    console.log("error from getUserInfo")
                }
            });
        
     });
    function updateMatches(userName){
        $.ajax({
            type: "GET",
            url: '/cgi-bin/getUserMatches.py',
            data: {'userName' : userName},
            success: function(data){
                var data = JSON.parse(data);
                htmlstring="";
                $.each(data, function(i, item){
                    
                    console.log("item is: " + item['username']);
                    username = item['username'];
                    humanName = item['humanName'];
                    humanPic = item['userPic'];
                    dogPic = item['dogPic'];
                    phoneNumber = item['phoneNumber'];
                    dogName = item['dogName'];
                    description = item['description'];
                    htmlstring += "<div class=\"match\" id=\"" +username + "\"><div class=\"human\"> <h2 class=\"humanName\"> Human: " + humanName + " </h2><br> <img class=\"profpic\" src=\"data:;base64, " + humanPic + "\"/></div><div class=\"dog\"> <h2 class=\"dogname\"> Dog:" + dogName + "</h2> <img class=\"dogpic\" src=\"data:;base64, " + dogPic + "\"/> </div> <br> <h2 class=\"description\">Description: </h2><br> <p> " + description + "</p><br><div class=\"container\"><h2>Phone Number:<h2>" + phoneNumber + "<br></div><div class=\"container\"><img id=\"unmatch\" src=\"photos/hate.png\" onclick=\"unmatch('"+username+"')\"></img></div></div></div>";
                    
                });
                $('#users').append(htmlstring);
                
                
                
            },
            error: function(jqXHR, textStatus, error){
                console.log("Error from getmatches: " + error);
                console.log("jqXHR: " + jqXHR);
                console.log("Textstatus: " + textStatus);
                alert ("ERROR");
            }

        });
        
    }
    function unmatch(username){
        unmatch_bool = confirm("Are you sure you want to un-match?");
        if (unmatch){
            console.log("unmatching");
            $.ajax({
                type: "GET",
                url: "/cgi-bin/unmatch.py",
                data:{"match_un": username},
                success: function(response){
                    alert("Deleted successfully");
                    reloadMatches()
                },
                error: function(){
                    console.log("halp");
                }
                
            });

        }else{
            console.log("still matched");
        }
    }
    function reloadMatches(){
        $('#users').html('');
        updateMatches();
    }
</script>

</head>
<body>
    <input type="hidden" id="curr_username" value="">
    <div id = "header">

        <img src = "photos/logo.png" id = "logo">
        <h1 id="matches_welcome"> View Matches </h1>
    </div>
    <?php include("navbar.php"); ?>
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