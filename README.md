## Bot for educational purposes
It's using basic Twitch IRC things: listening and sending messages <br>

It's made for one specific channel, so editing this might be difficult. It's using twitch-chat-irc package for sending and listening messages. <br>

# Details
It utilizes multiprocessing to achieve different things. First process is the listener, second is the IPC proxy, and then you can add as many as you want. <br>

# config.json
Required fields: <br>
- channel: str <br>
- user: { name, oauth } <br>

# Usage
```pip install -r requirements.txt``` <br>
```python3 index.py```
