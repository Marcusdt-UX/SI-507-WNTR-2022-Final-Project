from flask import Blueprint, render_template,session,request,redirect,url_for,flash
from event import graph
from api.api import *
from api.helpers import *
from datetime import datetime
event = Blueprint("event", __name__)

from .forms import FilterForm

@event.route('/', methods=['POST', 'GET'])
def home():
   
    filter_word=request.args.get('filter_word')
    criteria=request.args.get('criteria')
    geo=request.args.get('geo')
    radius=request.args.get('radius')
    keyword=request.args.get('keyword')



    if filter_word is None:
        criteria = 'country'
        filter_word = 'united states'

    data={criteria:filter_word}
    print(f'Data is {data}')
    if keyword:
        data.update({'keyword':keyword})
    if radius:
        data.update({'radius':radius})

    if geo:
        data.update({'lat':session['latitude']})
        data.update({'lon':session['longitude']})
        print(f"After geo is true data is {data}")
       
    form = FilterForm()
    events= filter_dups(delegator(**data))


    return render_template('home.html',events=events,form=form)


@event.route('/about')
def about():
    return render_template('about.html')

@event.route('/geo/<lon>/<lat>')
def set_geolocation(lon,lat):
    session['longitude']=lon
    session['latitude']=lat
    return {"resp":"OK"}
