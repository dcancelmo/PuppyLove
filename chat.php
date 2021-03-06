<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Dog Park</title>
        <script src="http://127.0.0.1:3000/socket.io/socket.io.js"></script>
        <script src="http://code.jquery.com/jquery-1.11.1.js"></script>
        <link rel = "stylesheet" type = "text/css" href = "style/styleDash.css" />
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font: 13px Helvetica, Arial;
            }
            form {
                background: #000;
                padding: 3px;
                position: fixed;
                bottom: 0;
                width: 100%;
            }
            form input {
                border: 0;
                padding: 10px;
                width: 90%;
                margin-right: .5%;
            }
            form button {
                width: 9%;
                background: rgb(130, 224, 255);
                border: none;
                padding: 10px;
            }
            #messages {
                list-style-type: none;
                margin: 0;
                padding: 0;
            }
            #messages li {
                padding: 5px 10px;
            }
            #messages li:nth-child(odd) {
                background: #eee;
            }
        </style>
    </head>
    <body>
        <div id = "header">

        <img src = "photos/logo.png" id = "logo">
        <h1 id="chat_title"> The Dog Park </h1>
    </div>
    
    <?php include("navbar.php"); ?>
   
    <div id = "messages" style = "margin-left:100px">
        <ul id="messages"></ul>
      
        <form action="">
            <input id="m" autocomplete="off"/><button>Send</button>
        </form>
    </div>
        <script>
            $(document).ready(function(){
                $.ajax({
                    url: 'cgi-bin/load-messages.py',
                    type: 'GET',
                    dataType: 'JSON',
                    success:function(response){

                        $.each(response, function(i, item){
                            var username = item['username'];
                            var message = item['message'];
                            var printedMessage = username + ": " + message;
                            $('#messages').append($('<li>').text(printedMessage));
                        });
                    },
                    error: function(jqXHR, exception){
                        alert(exception);
                    }
                })
            });

            var socket = io.connect('http://127.0.0.1:3000');
            // this function is called when the user presses ENTER or clicks the Submit
            // button in the form.
            $('form').submit(function() {
                $.ajax({
                    url:'cgi-bin/get_username.py',
                    type: 'GET',
                    dataType: 'text',
                    success: function(response){
                        var response = JSON.parse(response);
                        var username = response.username;
                        var message = username + ": " + $('#m').val();
                        console.log(username);
                        console.log("should transmit message: " + message);
                        socket.emit('chat message', message);
                        

                        $.ajax({
                            url:'cgi-bin/store-message.py',
                            type: 'POST',
                            data: {"message": $('#m').val(), "username": username},
                            success: function(response){
                                $('#m').val('');
                            },
                            error: function(jqXHR, exception){
                                alert(exception);
                            }
                        });

                    }
                });
                return false;
            });

            socket.on('chat message', function(msg) {
                $('#messages').append($('<li>').text(msg));
                // add the contents of the message to the unordered list.
            });
         </script>
    </body>
</html>