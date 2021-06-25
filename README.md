# warzoneBot
Minimal Python Bot to display Call Of Duty Warzone stats from WZStats.gg\
At the moment the bot is <b>not publicly available</b>.

## Getting Started

### Manually

You can clone or fork the repo and contibute or use it in your own discord channel.
For both Linux and Windows
 ```cmd
git clone https://github.com/singleit-tech/warzoneBot.git
 ```

### Activating the env
Windows
 ```cmd
 python3 -m pip install venv env
 python3 -m pip install -r requirements.txt
 env\Scripts\Activate
 ```
 
 Linux
 ```bash
 python3 -m pip install venv env
 python3 -m pip install -r requirements.txt
 source env\bin\activate
 ```
### Deploying on Docker
 ```cmd
git clone https://github.com/singleit-tech/warzoneBot.git && cd warzoneBot
 ```
```cmd
docker build -t warzone-bot:latest .
```
```cmd
docker run -d warzone-bot:latest
```
## Development

I develop this project in my free time, feel free to clone the repo and contribute.\
At the time all the output from the bot is in text format.\
![alt text](https://i.gyazo.com/e088311ede70cc8c7b7b85f6a51bc8f2.png)\
I'm currently working on a <b>card/image</b> presentation for the stats.

## License
[MIT](https://choosealicense.com/licenses/mit/)
