# Multi-armed bandit

This is a game based on the multi-armed bandit problem. At a time, five teams/individuals play for a specific number of rounds. The rules of the game is as follows:

1) Each round of the game is 7 seconds long. (This time is user defined.) Each team gets 100 point to start with.
2) Each team gets to select one of the five option in each round. Based on their selection, they obtain a sample/score for that particular option. The score can be negative or positive.
3) If a team choose to not play in a round, i.e. doesn't select one of the five option, then the team incurs the most negative score of -25.
4) At the end of each round, the scoreboard is updated with each team's chosen option and obtained score for that option.
5) Each team needs to observe their and their competition's performance from scoreboard.
6) The goal of each team is to maximise their score by identifying the distribution that gives the highest reward consistently and beat the competition.

The file structure is pretty simple:
- Static folder has all the necessary css files for displaying animation.
- Template folder has all the html files for each team as well as the scoreboard.
- server.py contains the game logic as well as Flask based server code. 

To start a game, use the following steps:
- Run the server.py code. This will generate a unique key for each game and output it in the python console.
- Go to the scoreboard page @ IP:9090/Scoreboard/UniqueKey
- Go to the Team_links page which is locally hosted. This page shows QR code for each team. 
- Scan QR Code for each team and they'll be directed to the game page.
- Start the game by clicking 'Start' button in scoreboard page.
- Have fun!
