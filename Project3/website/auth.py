from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Note, Apt
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

import os
import json
# %pip install xmltodict
import xmltodict
import xml.etree.ElementTree as ET
import requests
from requests.models import parse_header_links
import csv
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pickle


with open('model.pkl','rb') as pickle_file:
    rfmodel = pickle.load(pickle_file)


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')
    data = request.form
    print(data)
    return render_template("login.html", boolean=True)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 4 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html")

@auth.route('/apt', methods=['GET', 'POST'])
def apt():
    if request.method == 'POST':
        location1 = request.form.get('location1')
        old = request.form.get('old')
        size = request.form.get('size')
        brand = request.form.get('brand')
        deal = request.form.get('deal')

        with open('model.pkl','rb') as pickle_file:
            rfmodel = pickle.load(pickle_file)

        input_list = [location1, size, old, brand, deal]
        df_dict_made = pd.DataFrame([input_list], columns=['location1', 'size', 'old', 'brand', 'deal'], index = [1])
        predict = rfmodel.predict(df_dict_made)
        predict = int(predict)
        session['predict'] = predict

        new_apt = Apt(location1=location1, size=size, old=old, brand=brand, deal=deal)
        db.session.add(new_apt)
        db.session.commit()
        flash('예측 매매가를 확인하세요!', category='success')
               
        return redirect(url_for('views.result', predict=predict))
       
    return render_template('apt.html')
