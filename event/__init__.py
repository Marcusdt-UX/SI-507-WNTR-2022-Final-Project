from flask import Flask
import json
import os
from event.config import Config
from api.api import *
from models.graph import Graph

graph= Graph()


def create_app(config_class=Config):

    """Sets up the application ans returns a flask application instance"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    from event.project.routes import event
    app.register_blueprint(event)

    
        # print(load_events_from_db_to_graph(graph).get_vertices())



    return(app)


