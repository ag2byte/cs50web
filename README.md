# Project 2

# Web Programming with Python and JavaScript

This is a chat applcation built using HTML, CSS, Javascript and ScoketIO. Flask is the backend server.
Project structure:
#### application.py
backend server for the application (in debug mode). Run using 'python application.py'
#### templates 
folder with html pages
            * base.html = layout page
            * index.html = user name registration page, also the landing page for the application
            * chat.html = chat page, where all the message sending and receiving takes place

#### static
        * css = folder for css
            - index.css = styling for index.html
            -chat.css = styling for chat.html
        * javascript = folder for js
            - chat.js = entire js script for chat.html
### Important note:
    * The server only stores the top 100 messages and deletes the rest
    * To send a message, click on the send button(required). 'Enter' is send feature not available

Personal Touch:
    The application can display who is currently typing a message 
    This works using socket.io
        Whenever a key is pressed a message is sent to the server containing username.
        This message is received in the client side, which checks if the username is equal to current username and displays the message
