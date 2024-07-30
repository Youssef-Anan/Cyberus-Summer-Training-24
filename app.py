from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
import os
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "AHSGstaya@8463e7shagA"
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["25 per minute"])

@app.route('/')
def index():
    if 'username'in session:
        flash(f"Welcome "+session['username'])
        return render_template("index.html")
    flash("You are not logged in")
    return render_template("index.html")

@app.route('/shop')
def shop():
    return render_template("shop.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/game')
def game():
    return render_template("product-details.html")
    

@app.route('/register', methods=['GET','POST'])
@limiter.limit("10 per minute")
def register():
    if request.method == 'POST':
        #Retrieving the data from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Handling the registration logic
        if not utils.is_strong_password(password):
            flash("Sorry You Entered a weak Password,Please Choose a stronger one", "danger")
            return render_template('login.html')
        
        user = db.get_user(connection, username)

        if user:
            flash("Username already exists. Please choose a different username.", "danger")
            return render_template('login.html')
        else:
            db.add_user(connection, username, password, email)
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/login', methods=['GET','POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        #Retrieving the data from the form
        username = request.form['username']
        password = request.form['password']
        # Handling the login logic
        user = db.get_user(connection, username)
        if user:
            if utils.is_password_match(password, user[2]):
                session['username']=user[1]
                session['user_id']=user[0]
                flash("Login successful", "success")
                return redirect(url_for('index'))
            else:
                flash("Wrong credentials", "danger")
                return render_template('login.html')
        else:
            flash("Wrong credentials", "danger")
            return render_template('login.html')
    return render_template('login.html')

            
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = "anan"
        new_username = request.form['user']
        new_email = request.form['email']
        pfpImage = request.files.get('image')

        pfp_url = None
        if pfpImage and pfpImage.filename != '':
            pfp_url = f"uploads/{pfpImage.filename}"
            pfpImage.save(os.path.join("static",pfp_url))

        # Call the edit_user function
        db.edit_user(connection, username, new_username, new_email, pfp_url)
                
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    username = session.get('username')
    if username:
        user = db.get_user(connection, username)
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.init_db(connection)
    app.run(debug=True, port=80)
