from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string
import db
import os

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "Hiqshagiq@5352r2gsbgdsk"

@app.route('/')
def index():
    if 'username' in session:
        return render_template("index.html")
    else:
        redirect(url_for(login))

@app.route('/shop')
def shop():
    if 'username' in session:
        return render_template("shop.html")
    else:
        redirect(url_for(login))

@app.route('/contact')
def contact():
    if 'username' in session:
        return render_template("contact.html")
    else:
        redirect(url_for(login))

@app.route('/game')
def game():
    if 'username' in session:
        return render_template("product-details.html")
    else:
        redirect(url_for(login))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #Retrieving the data from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # Handling the registration logic
        user = db.get_user(connection, username)
        if user:
            flash("Username already exists. Please choose a different username.", "danger")
            return render_template('login.html')
        else:
            db.add_user(connection, username, password, email)
    return render_template("login.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Retrieving the data from the form
        username = request.form.get('username')
        password = request.form.get('password')
        # Handling the login logic
        user = db.get_user(connection, username)

        if user:
            if user[2] == password:
                session['username'] = user[1]
                session['user_id'] = user[0]
                return redirect(url_for('index'))
        else:
            flash("Password dose not match", "danger")
            return render_template('login.html')
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/profile',methods=['GET','POST'])
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    db.init_db(connection)
    app.run(debug=True,port=80)