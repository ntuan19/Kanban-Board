# Flask Kanban Board
Simple Flask Kanban Board for managing your to-do list

## Features
- Add New Task
- Switch Taks to different states
![image](https://user-images.githubusercontent.com/61070900/111058724-2dbe7b00-8445-11eb-9202-b1ed79728d80.png)

- Delete Task
![image](https://user-images.githubusercontent.com/61070900/111058705-036cbd80-8445-11eb-8cd7-f6555b2977b6.png)


## Installation

Install necessary dependencies

    $ pip3 install -r requirements.txt

Start flask server

    $ python3 kanban.py

Another way to launch the web app

    $ python3.6 -m venv .venv 
    $ source .venv/bin/activate
    $ pip3 install -r requirements.txt  
    $ export FLASK_APP=kanban.py
    $ flask run
  




Your Kanban board should be up and running at http://127.0.0.1:5000/

## Unit Testing

On the project root directory, run

    $ python3 test.py
    $ python3 python3 -m unittest discover test

