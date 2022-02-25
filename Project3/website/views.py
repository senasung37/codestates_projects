from flask import Blueprint, render_template, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Apt
from .auth import apt
import pickle

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')
    return render_template("home.html")

@views.route('/result', methods=['GET'])
def result():
    predict = session['predict']

    return render_template("result.html", predict=predict)
