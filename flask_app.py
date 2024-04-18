from flask import Flask, request, session, render_template,redirect,url_for
from dbOperations import *
from functools import wraps
import requests
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
API_KEY = "https://cb3ua87b6f.execute-api.us-east-1.amazonaws.com/Production"



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            # If the user is not logged in, redirect to login page
            return redirect(url_for('loginPage', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/",methods=['GET'])
def redirectToLogin():
    return render_template('login.html',success_message = 'Welcome' )

#default route
@app.route("/login",methods=['GET','POST'])
def loginPage():
    # Retrieve success message from query parameters, default value if not provided
    if request.method == 'GET':
        success_message = request.args.get('success_message', 'Welcome!')
        return render_template('login.html',success_message=success_message)
    elif request.method == 'POST':
        api_url = f'{API_KEY}/lambda_loginUser'
        email = request.form['email']
        password = request.form['password']
        response = requests.post(api_url, json={'email':email,'password':password})
        
        if response.status_code == 200:
            data = response.json()
            body = json.loads(data['body'])
            if 'user' in body.keys():
                  # Extract user information if needed)
                session['user_email'] = body['user']['email']  # Storing the user identifier in session
                return redirect(url_for('main_page'))
            else:
                return redirect(url_for('loginPage',success_message=body['message']))
        else:
            message = response.json()['message']
            return redirect(url_for('loginPage', success_message=message))



        
# register new user
@app.route("/register", methods = ['GET','POST'])
def registerUser():
    if request.method == 'GET':
        return render_template('register_page.html')
    if request.method == 'POST':
        registrationData = request.form
        print(registrationData)
        api_url = f'{API_KEY}/lambda_addUser'
        print(registrationData.get('email'))
        response = requests.post(api_url, json={'email':registrationData.get('email'),'password':registrationData.get('password'),'username':registrationData.get('username')})
        print(f'response is {response.json()}')
        if response.status_code==200:
            response_data = response.json()  # Parse JSON response
            body = json.loads(response_data['body'])
            
            return redirect(url_for('loginPage', success_message=body['message']))
        else:
            return redirect(url_for('loginPage', success_message='something went wrong'))



 #main-page route after logging in
@app.route('/main_page')
@login_required
def main_page():
    user_email = session.get('user_email', 'Guest')
    # Fetch user-specific data using user details stored in session
    # Render the main page with user details and other required information
    #currentSubscriptions = fetchSubscriptions(user_email)
    api_url = f'{API_KEY}/lambda_fetchSub'
    response = requests.post(api_url, json={'email':user_email})
    if response.status_code == 200:
        data = response.json()
        body = json.loads(data['body'])
        session['subscriptions'] = body['subscriptions']
        return render_template('main_page.html', user_email=user_email,subscriptions = session['subscriptions'])
    else:
        return redirect(url_for('loginPage', success_message='something went wrong'))


#logout route
@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    # Redirect to login page or home page
    return redirect(url_for('loginPage'))


#query music
@app.route('/query_music', methods = ['GET','POST'])
@login_required
def queryMusic():
    musicQuery = request.form
    non_empty_data = {}
    # Iterate over each item in the ImmutableMultiDict
    for key, value in musicQuery.items():
        if value:  # Checks if value is not empty
            non_empty_data[key] = value
    api_url = f'{API_KEY}/lambda_fetchMusic'
    response = requests.post(api_url, json=non_empty_data)
    if response.status_code == 200:
        data = response.json()
        if 'body' in data:
            body = json.loads(data['body'])
            print(body)
        # Access the music list
            music_list = body['musicList']
    # musicList = fetchMusic(musicQuery)
            return render_template('main_page.html',user_email = session.get('user_email','Guest'),query_results = music_list,subscriptions= session.get('subscriptions') )
        else:
            return render_template('main_page.html',user_email = session.get('user_email','Guest'),query_results = [],subscriptions= session.get('subscriptions') )


@app.route('/subscribe', methods = ['GET','POST'])
def subscribe():
    subscribedSong = request.form
    api_url = f'{API_KEY}/lambda_addSubscribedMusic'
    response = requests.post(api_url, json={'email':session.get('user_email','Guest'),'songInfo':subscribedSong.to_dict()})
    if response.status_code == 200:
        return redirect(url_for('main_page'))

    
@app.route('/remove_subscription',methods=['GET','POST'])
def unsubscribe():
    unsubscribedSong = request.form
    api_url = f'{API_KEY}/lambda_unsubscribe'
    response = requests.post(api_url, json={'email':session.get('user_email','Guest'),'songInfo':unsubscribedSong.to_dict()})
    if response.status_code == 200:
        return redirect(url_for('main_page'))

    
if __name__ == '__main__':
    app.run()
