from flask import Flask, render_template, request, session

app = Flask(__name__, template_folder="template")


@app.route('/base/')
def base_method():
    return render_template('base.html')


# @app.route('/login')
# def login_user():
# email = request.form['email']
# password = request.form['password']

# from src.models.user import User
# if User.login_valid(email, password):
# User.login(email)

# return render_template("profile.html", email=session['email'])


@app.route('/')
def login_method():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
