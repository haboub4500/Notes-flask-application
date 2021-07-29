from flask.json import jsonify
from website.models import Note
from flask import Blueprint, render_template, request, jsonify
from flask.helpers import flash
# this file is gonna be a blueprint for our app : it will have a lots of routes inside of it
from flask_login import login_user, login_required, logout_user, current_user
#from werkzeug.wrappers import request
from . import db 
import json




views = Blueprint('views', __name__)

@views.route('/', methods = ['GET','POST']) #whenever we go to the root : / (main page of website), we run the home function
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) <= 1 :
            flash('note is too short !', category='error')
        else :
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note added ! ', category='success')
    return render_template("home.html", user = current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})