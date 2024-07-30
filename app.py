from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string
import db
import os

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "Hiqshagiq@5352r2gsbgdsk"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieving the data from the form
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieving the data from the form
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
            flash("Password does not match", "danger")
            return render_template('login.html')
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
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
