from flask import Flask, request, session, render_template,redirect,url_for
from dbOperations import *
from functools import wraps


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            # If the user is not logged in, redirect to login page
            return redirect(url_for('loginPage', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


#default route
@app.route("/login",methods=['GET','POST'])
def loginPage():
    # Retrieve success message from query parameters, or use default value if not provided
    if request.method == 'GET':
        success_message = request.args.get('success_message', 'Welcome!')
        return render_template('login.html',success_message=success_message)
    elif request.method == 'POST':
        response, user = login(request)
        print(user)
        print(response)
        if user:
            session['user_email'] = user.get('email') # Storing the user identifier in session
            return redirect(url_for('main_page'))
        else:
            return redirect(url_for('loginPage',success_message= response.get_json()['message']))

        
# register new user
@app.route("/register", methods = ['GET','POST'])
def registerUser():
    if request.method == 'GET':
        return render_template('register_page.html')
    if request.method == 'POST':
        registrationData = request.form
        result = validateUser(registrationData)
        if 'Item' not in  result:
            if(addUser(registrationData)):
                #return jsonify({'message':'User added to DB'}),200
                 # Redirect to login page with a success message
                return redirect(url_for('loginPage', success_message='User added successfully'))
            else:
                # return jsonify({'message':'something went wrong'})
                return redirect(url_for('loginPage', success_message='something went wrong'))
        else:
            return redirect(url_for('loginPage', success_message='email already exists'))
            #return jsonify({'message':'user with this email already exists'}),200



 #main-page route after logging in
@app.route('/main_page')
@login_required
def main_page():
    user_email = session.get('user_email', 'Guest')
    # Fetch user-specific data using user details stored in session
    # Render the main page with user details and other required information
    return render_template('main_page.html', user_email=user_email)


#logout route
@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    # Redirect to login page or home page
    return redirect(url_for('loginPage'))


#query music
@app.route('/query_music', methods = ['GET','POST'])
def queryMusic():
    musicQuery = request.form
    musicList = fetchMusic(musicQuery)
    return render_template('main_page.html',user_email = session.get('user_email','Guest'),query_results = musicList)




