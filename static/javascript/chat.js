//js file that controls the chat ui


var cur_channel = '';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);//socket variable
var username = localStorage.getItem('username');//get username from local storage
document.addEventListener('DOMContentLoaded', () => {


    document.getElementById("username").innerHTML = username;
    if (!localStorage.getItem('channel'))
        load_page("default");
    // load default page if no channel in localstorage
    else
        load_page(localStorage.getItem('channel'));



    socket.on("cur_messages", msgs => {//populates the current page
        msgs.forEach(data => {
            //displaying all current messages
            if (data.message) {


                const div = document.createElement('div');

                const br = document.createElement('br');
                const t = document.createElement('p');

                div.innerText = data.message

                others = '-' + data.username + '  ' + data.timestamp;

                t.innerText = others;
                if (username === data.username) {
                    div.setAttribute("class", "my-message");
                    t.setAttribute("class", "other_details_mine");
                }
                else {
                    div.setAttribute("class", "not-my-message");
                    t.setAttribute("class", "other_details_notmine");

                }

                div.append(br);
                div.append(t);


                document.getElementById('chat').prepend(div);
            }
        })
    });

    socket.on("messages", data => {//adds new data
        if (data.message) {
            document.getElementById('typing').innerHTML = "";

            const div = document.createElement('div');

            const br = document.createElement('br');
            const t = document.createElement('p');

            div.innerText = data.message

            others = '-' + data.username + '  ' + data.timestamp;

            t.innerText = others;
            if (username === data.username) {
                div.setAttribute("class", "my-message");
                t.setAttribute("class", "other_details_mine");
            }
            else {
                div.setAttribute("class", "not-my-message");
                t.setAttribute("class", "other_details_notmine");

            }

            div.append(br);
            div.append(t);


            //message is the message emited by server
            document.getElementById('chat').prepend(div);
        }
    });

    user_message = document.getElementById('user-message');
    user_message.addEventListener('keypress', () => {
        if (username.length > 0)
            if (user_message.value.length > 0) {
                // broadcast typing message
                socket.emit('typing', { "username": username });
            }


    });

    socket.on('typing', data => {
        console.log(data);
        typing = document.getElementById('typing');
        if (username != data['username'])
            typing.innerHTML = data['username'] + ' is typing ...';


    })

});

function load_page(name) {

    const chat = document.getElementById('chat');
    if (name === "default") {
        document.getElementById('type').style.display = "none";

        chat.classList.add("nodata")

        chat.innerHTML = "Nothing to display yet. Click on a channel to begin";

    }
    else {

        chat.classList.remove("nodata");
        chat.innerHTML = "";
        cur_channel = name;
        localStorage.setItem('channel', cur_channel);//settong default room
        channellst = document.querySelectorAll('.channelname');
        for (i = 0; i < channellst.length; i++) {
            if (channellst[i].id === cur_channel)
                channellst[i].style.color = "#2d7a9c";
            else
                channellst[i].style.color = "black";
        }
        document.getElementById('type').style.display = "block";
        socket.emit('channel_joined', { 'channel': cur_channel });



    }

}
function new_message() {
    message = document.getElementById('user-message').value;
    document.getElementById('user-message').value = "";

    //we need to emit this to backend now;
    // cur_channel contains current channel 
    socket.emit('new_message', { 'channel': cur_channel, 'message': message, 'username': username });

}



function cnchannel() {
    const channel = prompt('Enter the new channel name');
    if (channel) {
        const request = new XMLHttpRequest();
        request.open('POST', '/newchannel');
        request.onload = () => {
            location.reload();

        };
        const data = new FormData();
        data.append('channel', channel);
        request.send(data);


    }


}




function sidebar() {
    var channels = document.querySelector('#channels');
    var cb = document.querySelector('.chatbox');
    var icon = document.querySelector('i');
    if (channels.style.display === "block")
        shrink(cb, channels, icon);
    else
        expand(cb, channels, icon);
}
function shrink(cb, channels, icon) {
    cb.style.animationDirection = "reverse"

    channels.style.display = "none";

    icon.innerHTML = "chevron_right";
}


function expand(cb, channels, icon) {

    cb.style.animationDirection = "normal";
    channels.style.display = "block";
    icon.innerHTML = "chevron_left";

}
function responsive() {
    var channels = document.querySelector('#channels');
    var cb = document.querySelector('.chatbox');
    var icon = document.querySelector('i');
    if (window.innerWidth <= 800)
        shrink(cb, channels, icon)
    else
        expand(cb, channels, icon)


}
