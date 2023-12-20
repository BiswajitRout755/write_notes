from flask import Blueprint , render_template  , flash, request, jsonify #blueprints here is the module where all the default routes has been defined to where a user can easily get into it..
from flask_login import login_required,  current_user #this current user will tell us everything about the current logged in user..else it will tell that its a anonymous user
from .models import Note
from . import db
import json
#setting  up the blueprint application
views = Blueprint('views' , __name__) #defining the name of the blueprint , it makes the flask app runable..

@views.route('/' , methods=['GET', 'POST']) 
@login_required   #until n unless u have logged in you cannot go to the homeroute, only after the loggin session u r able to aceess to the home page..
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id) #add note is like be:
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user) #here user is the User class from views.py and this will add all details to the current_user..

@views.route('/delete-note' , methods=['POST'])
def delete_note():
    note=json.loads(request.data) #this takes the noteID argument passed in the index.js which is a string (for stringify method) and here it will be stored as dict.
    noteId = note['noteId'] #then in the noteID var.and note['noteID] fetches the proper id..all details from it 
    note = Note.query.get(noteId) #and then get all the details of that noteID and then,
    if note:
        if note.user_id == current_user.id: #checks whether the note's id is same as the user's id 
            db.session.delete(note)
            db.session.commit()

    return jsonify({})