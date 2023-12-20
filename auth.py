#this views.py file here defines that here is a bunch of routes inside this .py file

from flask import Blueprint, render_template , request, flash , redirect, url_for#blueprints here is the module where all the default routes has been defined to where a user can easily get into it..
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash #hashing is the method of password encryption 
from . import db
from flask_login import login_user, login_required, logout_user, current_user
#setting  up the blueprint application
auth=Blueprint('auth' , __name__) #defining the name of the blueprint/ we've defined a blueprint for our flask app(__name__)

@auth.route('/welcome' , methods=['GET', 'POST'])
def default():
    return render_template("default.html", user=current_user)

@auth.route('/login' , methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        email= request.form.get('email')
        password= request.form.get('password')

        user= User.query.filter_by(email=email).first() #used to return the whole columns with the typed email..
        if user: # above code will check that if the typed email is within the columns and this code states that if the user does exists then terminates the further line codes..
            if check_password_hash(user.password, password): #check if the signedup(hashing password) matches the above typed password..
                flash("logged in successfully" , category="success")
                login_user(user , remember=True) #this remember argument helps flask to remember that the user has logged in until n unless any circumstances happens.
                return redirect(url_for("views.home"))
            else:
                flash("wrong password, try agin" , category="error")
        else:
            flash("email doesn't exist" , category="error")
    return render_template ("login.html" , user=current_user)



@auth.route('/logout')
@login_required            #this helps to not to go to the logout route until n unless any user have logged in..
def logout():
    logout_user()
    return redirect(url_for("auth.default"))

@auth.route('/sign-up' , methods=['GET' , 'POST']) #here first when we reload the page it goes with GET req. and then after hitting the submit button its goes qith the POST req.
def signup():
    #conditions to fetch the user values that the user has typed.. 
    if request.method == 'POST':
        email= request.form.get('email') #form is used to fetch the data being typed(html form__)
        first_name=request.form.get('firstName')
        password1=request.form.get('Password1')
        password2=request.form.get('Password2')

#conditions that a user should need to follow while giving the input..
        user= User.query.filter_by(email=email).first() #checks if the same email does exist while signing up then it flashes a error message..
        if user: #if the above user satisfies then it will show the error..
            flash("email already exists" , category="error")
        elif len(email) < 4:
            flash("email must be greater than 4 characters." , category="error") #flashing the error messages through the module flash
        elif len(first_name) < 2:
            flash("First Name must be greater than 3 characters." , category="error")
        elif password1!=password2:
            flash("Password don\'t match." , category="error")
        elif len(password1)< 7:
            flash("Password must be atleast 7 characters." , category="error")
        else:
             new_user=User(email=email, first_name=first_name, password=generate_password_hash(password2, method='sha256')) #if the above cond._not then exec. this else loop and create a new user with email, firstname, password(encrypted way) store it in the databse
             db.session.add(new_user) #this helps to add the account to the database
             db.session.commit() #this is to justify that we have made some changes & so committ itt(update itt)..
             login_user(new_user , remember=True) #this will remember the current logged_in user credentials, and when the next time the same user tries to login ,he gets redirected to the page without the being authenticated, 
             flash("Account created Successfully!" , category="success")
             return redirect(url_for('views.home')) #it will redirect u to the home page(blueprint_name.function_name)
        
            #add this info to the databse..



    return render_template("signup.html" , user=current_user)

#here this user is relataed to the base.html's if user_is_authenticated..
#means it will 1st go through the signup and login method and if any user haven't logged in currenly
#then it's gonna show the {% else %} department from the base.html , but if it is then the {% if%} depart.