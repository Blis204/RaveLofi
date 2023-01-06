# RaveLofi
24/7 Lofi bot designed for the official [RaveCraft Discord server](https://dsc.gg/ravecraft)

![RaveLofi Banner](https://i.imgur.com/UPqUgd7.png)

**⚠️Important!** This bot isn't hosted publicly, feel free however to clone this repo to host your own version!

### Installation
You need to have python, git and pip already setup on your machine, in order to follow this guide!

#### 1. Clone the repo
  ```sh
  git clone https://github.com/nikdraws/RaveLofi
  ```
#### 2. Install the requirements
  ```sh
  pip install -r requirements.txt
  ```
or
  ```sh
  python -m pip install -r requirements.txt
  ```
#### 3. Create a bot
Head over to the [Developer Portal](https://discord.com/developers/applications). And create a bot if you didn't already. If you don't know how to setup a bot follow [this guide](https://discordpy.readthedocs.io/en/latest/discord.html)<br>
##### 4. Setting env variables
Now you will need to set your envoirement variables. Create a file named `.env`, paste the following text and insert your data
  ```sh
  TOKEN=YOUR_BOT_KEY
  HOST=LAVALINK_HOST
  PORT=LAVALINK_PORT
  PASSWORD=LAVALINK_PASSWORD
  ```
If you don't have a lavalink server you can pick one from [here](https://lavalink.darrennathanael.com/SSL/lavalink-with-ssl/). It is always recommended to host your own server, for best performance and privacy.
#### 5. Change the settings.json
Now you need to change the data in the settings.json.<br><br>
**Playlist:** You can define your own playlist or use the one already predefined<br>
**Channel:** This is the channel id, of the channel that the bot will automatically join and stay in<br>
**Guild** This is the guild id of the guild your bot is in.<br><br>

#### 6. Starting the bot
Now you need to change the guild id in the main.py file to your guild id.<br><br>
If you followed everything correctly you should now be able to run the bot using
```sh
python main.py
```
or
```
python3 main.py
```
