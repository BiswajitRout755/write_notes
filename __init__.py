from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy #creating databases now
from flask_login import LoginManager

db=SQLAlchemy() #db is the object 
DB_NAME="database.db" #databse.db is the name of our databse

def create_app():
    app= Flask(__name__) #its the file which will run
    app.config['SECRET_KEY'] = "cookies files "  #cookies are the files 
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}" #SETTING THE DATABASE LOCATION
                                                       #this means here our sqlite databse is stored in the sqlite:///{dbname}
    db.init_app(app) #initializing the app here 



    from .views import views #name of the views(blueprint)
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import  User, Note
    create_database(app)

    #all these required if ur using flask_login manager..
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #it telling the login maanager that where u need to go if ur nt logged in..
    login_manager.init_app(app) #telling the manager wihch app we are using..

#once the user class obj is created in the models.py you need to load each evry login credentials so that it(login manager) will check all the login correct procedures..
    @login_manager.user_loader
    def load_user(id): #this is called before every request..
        return User.query.get(int(id)) #this will query or load through the id. #check each models of the user through id whether it satisfies all the conditons or not..



    return app

def create_database(app):
    if not path.exists ('WEBSITE/' + DB_NAME):  #this os path here denotes that if this path doesnt exist
                                                   #website/database.db , then create that database.
                                                   #this os .path used check the path of the file being mentiond.
                                                   #if it does then create_database(app)
        db.create_all(app=app)
        print("Created Database!")
