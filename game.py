import git_repo
import server
import repository
from multiprocessing import Process
import subprocess
import time
import os
import random
import math

#Contains essential game logic. 
  
def init_game():
  #Sets up the game environment.
  #Also a good place to put commands which should only be run once.
  config = repository.get_config()
  os.environ["GITHUB_USERNAME"] = config["git_login"]
  os.environ["GITHUB_REPO"] = config["git_repo"]
  os.environ["GITHUB_PASS"] = config["git_password"]
  if not "db_setup" in config:
    players = git_repo.get_players()
    player1 = pick_next_player(players)
    repository.init_db(player1)
    #Save that weve set up the db
    config['db_setup'] = "complete"
    repository.set_config(config)
  
def play_round():
  #Start the game server
  game_server = Process(target = server.start_server)
  game_server.start()
  #Wait until the end of the round
  while 1:
    time.sleep(604800) #1 week
  
if __name__ == '__main__':
  #Start the database
  database_process = subprocess.Popen(["mongod"])
  #give the database a chance to start up
  time.sleep(5)
  #Do first time setup/onetime commands
  init_game()
  #START THE GAME
  play_round()
  
  #Rounds over. Clean up time.
  #Stop the db
  database_process.terminate()
  sleep(5)
