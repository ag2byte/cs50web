import os
import time

from flask import Flask, render_template, request, redirect, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = ['General']  # the default channel is General
messages = {}


@app.route("/")
def index():

    return render_template("index.html")


@app.route('/chat')
def chat():

    return render_template("chat.html", channels=channels)


@app.route('/newchannel', methods=['POST'])
def newchannel():

    if request.form.get("channel") not in channels:
        channels.append(request.form.get("channel"))
    return jsonify(channels)


#

@socketio.on('new_message')
def message(data):
    # data contains the message and other details
    now = time.strftime('%b-%d %I:%M%p', time.localtime())
    # this is the timestamp
    values = {'channel': data['channel'], 'message': (
        ' '+data['message']+' '), 'username': data['username'], 'timestamp': now}
    print(values)
    messages.setdefault(data['channel'], []).append(values)
    if len(messages[data['channel']]) > 100:
        del messages[data['channel']][0]
    # server stores only 100 messages in a channel

    print(messages)
    emit("messages", values, broadcast=True)


# this is joining a channel
@socketio.on('channel_joined')
def channel_joined(data):
    print(f'in channel_joined: {data}')
    emit('cur_messages', messages[data['channel']], broadcast=False)

# for displaying who is typing


@socketio.on('typing')
def typing(data):
    values = {'username': data['username']}
    emit('typing', values, broadcast=True)


if __name__ == "__main__":
    app.run(debug=True)
    socketio.run(app)
