#######################Krish imports
from __future__ import division, print_function
# coding=utf-8

# Keras
#from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename

#####################
import secrets
#from ultralytics import YOLO
#model = YOLO("app/static/Yolo/best.pt")

####################

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Response
from app import app, db, bcrypt
from app.forms import RegisterForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from flask import session
import json


#from flask_sock import Sock
import os, datetime, pytz
import logging
import numpy as np

#sock = Sock(app)
import datetime
from datetime import timedelta
from pytz import timezone
#ymd = "%Y-%m-%d"
ymd = "%m-%d-%Y"


###########



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('today2'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user:
            if attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                session.permanent = True  # Make the user's session permanent
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('today2'))
            else:
                flash('Wrong password! Please try again', category='danger')
        else:
            flash('Username does not exist! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))



################################### Krish naik

# Model saved with Keras model.save()
print(os. getcwd())
#MODEL_PATH = 'app/static/models/resnet50.h5'
#MODEL_PATH = 'app/static/models/EfficientNetV2S_None.h5'

@app.route('/index3', methods=['GET'])
def index3():
#    # Main page
    return render_template('index3.html')

################################## end of Krish Naik

'''
@app.route("/today3", methods=['GET', 'POST'])
def today3():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))

    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == now_Hawaii.strftime("%Y-%m-%d") and f[3:4] not in ["K", "B", "M"]]

    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    predictions = []
    if request.method == 'POST':
        for image_file in image_namez:
            file_path = os.path.join(save_location, image_file)
            results = model.predict(source=file_path)
            predictions.append((image_file, results[0]))  # Store image name and prediction

    return render_template('today3.html', image_names=image_namez, predictions=predictions)
'''

@app.route("/today", methods=["GET", "POST"])
#@login_required
def today2():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == now_Hawaii.strftime(ymd) and f[3:4] != "K" and f[3:4] != "B" and f[3:4] != "M"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("today2.html", image_names=image_namez)
  

@app.route("/yesterday", methods=["GET", "POST"])
#@login_required
def yesterday():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    yesterday_Hawaii = now_Hawaii - timedelta(days=1)
    
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == yesterday_Hawaii.strftime(ymd) and f[3:4] != "K" and f[3:4] != "B" and f[3:4] != "M"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("yesterday.html", image_names=image_namez)



@app.route("/today2k", methods=["GET", "POST"])
def today2k():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == now_Hawaii.strftime(ymd) and f[3:4] == "K"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        date3[4:6]  # Then by trap name
    ), reverse=True)

    return render_template("today2k.html", image_names=image_namez)

@app.route("/today2x", methods=["GET", "POST"])
def today2x():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == now_Hawaii.strftime(ymd) and f[3:4] == "X"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("today2x.html", image_names=image_namez)



@app.route("/today2b", methods=["GET", "POST"])
def today2b():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == now_Hawaii.strftime(ymd) and f[3:4] == "B"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("today2b.html", image_names=image_namez)

@app.route("/today2m", methods=["GET", "POST"])
def today2m():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == now_Hawaii.strftime(ymd) and f[3:4] == "m"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("today2b.html", image_names=image_namez)

@app.route("/today2M", methods=["GET", "POST"])
def today2M():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == now_Hawaii.strftime(ymd) and f[3:4] == "M"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("today2M.html", image_names=image_namez)



@app.route("/todaypred", methods=["GET", "POST"])
def todaypred():
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    today_date_str = now_Hawaii.strftime("%m-%d-%Y")

    prediction_folder = os.path.join(app.root_path, "static", "prediction-result", f"{today_date_str}_prediction")
    
    if os.path.exists(prediction_folder):
        all_files = [f for f in os.listdir(prediction_folder) if os.path.isfile(os.path.join(prediction_folder, f))]
        image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg'))]

        print(f"Prediction Folder: {prediction_folder}")  # Debugging line
        print(f"Images: {image_files}")  # Debugging line

        return render_template("todaypred.html", image_names=image_files, today_date=today_date_str)
    else:
        return f"Prediction folder for {today_date_str} does not exist.", 404





@app.route("/yesterdayk", methods=["GET", "POST"])
#@login_required
def yesterdayk():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    yesterday_Hawaii = now_Hawaii - timedelta(days=1)
    
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == yesterday_Hawaii.strftime(ymd) and f[3:4] == "K"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("yesterdayk.html", image_names=image_namez)




@app.route("/yesterdayx", methods=["GET", "POST"])
#@login_required
def yesterdayx():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    yesterday_Hawaii = now_Hawaii - timedelta(days=1)
    
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == yesterday_Hawaii.strftime(ymd) and f[3:4] == "X"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("yesterdayx.html", image_names=image_namez)


@app.route("/yesterdayb", methods=["GET", "POST"])
#@login_required
def yesterdayb():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    yesterday_Hawaii = now_Hawaii - timedelta(days=1)
    
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == yesterday_Hawaii.strftime(ymd) and f[3:4] == "B"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("yesterdayb.html", image_names=image_namez)

@app.route("/yesterdayM", methods=["GET", "POST"])
#@login_required
def yesterdayM():
    save_location = os.path.join(app.root_path, "static")
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_Hawaii = now_utc.astimezone(timezone('US/Hawaii'))
    yesterday_Hawaii = now_Hawaii - timedelta(days=1)
    
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    image_namez3 = [f for f in filesandfolders if f[19:29] == yesterday_Hawaii.strftime(ymd) and f[3:4] == "M"]

    # Modified sorting key
    image_namez = sorted(image_namez3, key=lambda date3: (
        int(date3[13:15]),  # Sort by hour only
        int(date3[4:6])  # Then by trap number
    ), reverse=True)

    return render_template("yesterdayM.html", image_names=image_namez)



@app.route("/search", methods=["GET", "POST"])
def search():
    save_location = (os.path.join(app.root_path, "static"))
    print("root+static")
    print(save_location)
    filesandfolders = [f for f in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, f))]
    name = request.args.get("name")
    image_namezf = [f4 for f4 in filesandfolders if f4[3:6]==name]
    image_namezff = sorted(image_namezf ,key = lambda date3: datetime.datetime.strptime(date3[13:29], '%H-%M_%m-%d-%Y'), reverse=True)    
    print(name)
    print("We are in flask_app")
    return render_template("search.html", image_names=image_namezff, name = name) 


@app.route("/uploads", methods=["GET", "POST"])
def upload_image2():
    if request.method == 'POST':
        image_raw_bytes = request.get_data()  #get the whole body
        #image_raw_bytes = request.files.get('imagefile', '')  #get the whole body
        print(type(image_raw_bytes))
        print(image_raw_bytes)
        #image_raw_bytes=request.files['file']
        #print(image_raw_bytes)
        dt_Hawaii = datetime.datetime.now(tz=pytz.timezone('US/Hawaii'))
        fname = dt_Hawaii.strftime('%B.%d.%Y.%X')
        fname= fname.replace(":", ".")
        fname2=fname
        #save_location = (os.path.join(app.root_path, 'static', fname2+'.jpg')) 
        save_location = (os.path.join(app.root_path, "static/testz.jpg"))
        f = open(save_location, 'wb') # wb for write byte data in the file instead of string
        f.write(image_raw_bytes) #write the bytes from the request body to the file
        f.close()
    #return redirect(url_for('uploaded_file', fname2=fname2))
    if request.method == "GET":
        return render_template("image_show.html")
    return "if you see this, that is bad request method"

#########################

# /map/
# /map/?island=oahu
# /map/?island=bad_island_name
@app.route('/map/')
def map():
  island = request.args.get('island')
  if island == "oahu":
    island_center = { "latitude": 21.4389, "longitude": -158.0001}
    valid_island=True
    pretty_island_name = "Oahu"
  elif island == "kauai":
    island_center = { "latitude": 22.0964, "longitude": -159.5261}
    valid_island=True
    pretty_island_name = "Kauai"
  elif island == "maui":
    island_center = { "latitude": 20.7984, "longitude": -156.3319}
    valid_island=True
    pretty_island_name = "Maui"
  elif island == "big_island":
    island_center = {"latitude": 19.5429, "longitude": -155.6659}
    valid_island=True
    pretty_island_name = "Big Island"
  elif island == "molokai":
    island_center = {"latitude": 21.1444, "longitude": -157.0226}
    valid_island=True
    pretty_island_name = "Molokai"
  else:
    island_center = { "latitude": 21.4389, "longitude": -158.0001}
    valid_island=False
    pretty_island_name = island
  return(
      render_template(
        'map.html',
        valid_island_template=valid_island,
        island_name_template=pretty_island_name,
        island_center_template = island_center,
        computerized_island_name_template = island,
      )
    )

@app.route('/traps/')
def traps():
  island = request.args.get('island')
  path = 'app/static/prediction-result/today_json_files/'
  if island == "kauai":
   file_location = (f'{path}/kauai.json')
  elif island == "oahu":
    file_location = (f'{path}/oahu.json')
  elif island == "maui":
    file_location = (f'{path}/maui.json')
  elif island == "big_island":
    file_location = (f'{path}/big_island.json')
  elif island == "molokai":
    file_location = (f'{path}/molokai.json')
  else:
    file_location = "no data file available"

  try:
    with open(file_location) as file:
      locations = json.load(file)
  except FileNotFoundError:
    locations = []
  return locations
