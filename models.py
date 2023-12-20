#creating the schema for our database=
# here the dot(.) denotes that from the current folder(WEBSITE) import db(object)
from . import db
from flask_login import UserMixin #USermixin is a class comes under the flask_login module and it comes with various features while loggig in
from sqlalchemy.sql import func


class Note(db.Model): #inherit from the db.model
    id= db.Column(db.Integer, primary_key=True)
    data= db.Column(db.String(10000))
    date= db.Column(db.DateTime(timezone=True), default=func.now()) #func will automatically set the current date n time
    user_id= db.Column(db.Integer, db.ForeignKey('user.id')) #here this user_id is from User(user) class and .id is from (id of the User class) , in database the class name will be in lower case


#storing the database models
class User(db.Model , UserMixin): #inherit from the db.model(datas)
    id= db.Column(db.Integer , primary_key=True)
    email= db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes= db.relationship('Note') #Note is the Note class , it creates the relationship between 
                                    #everytime a note is created it will establish a relation with the User's id
                                    #everytime a note is added it will also add the users_id to the User's note.




