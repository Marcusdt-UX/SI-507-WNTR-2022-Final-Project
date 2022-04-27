# EVENT LOCATOR 
The project allows the user to  select events with a variety of filters. The filter criterions include: 
- country 
- state 
- keyword 
- radius 
- user's location 

The data is obtained from the api and  stored in a sqlite database. The  records are read and stored in 
event objects before being passed to the graph object

## Installation 
Flask is the only external dependency used. Other PyPI packages include 
- datetime 
- json 
- sqlite

```bash 
pip install flask 

```

# Project Setup 
The api key has been provided in the config.ini in the data module. It contains a reference to both the ticketmaster and seatgeek api.

# Running the Project
Locate the run.py found in the topmost directory hierarchy and run the file
