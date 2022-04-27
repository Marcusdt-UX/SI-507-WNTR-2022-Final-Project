# DATA STRUCTURE 

- Data queried from the API is returned as a json containing details about each event.
- The json files are converted to an event object to allow for better programmatic manipulation.
- The event objects are the vertices of a graph. The edges/ relationship between the nodes is determined by the   distance that is calculated based on the latitude/longitude.
- Events that are 25km close are considered neighbors. 
Once all event objects are collected to a list, a custom function within range is defined that checks if the current node is close to any of the event objects already loaded. 
- If within range they are added as neighbors. A graph class that provides a higher overview of the functionalities required is implemented. 
