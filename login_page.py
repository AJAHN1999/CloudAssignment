from flask import Flask, request, jsonify, render_template,redirect,url_for
from dbOperations import *


app = Flask(__name__)


# @app.route("/login", methods=['POST'])
# def login():
#     data = request.form
#     response = validateLogin(data)
#     return response

@app.route("/login",methods=['GET','POST'])
def loginPage():
    # Retrieve success message from query parameters, or use default value if not provided
    if request.method == 'GET':
        success_message = request.args.get('success_message', 'Welcome!')
        return render_template('login.html',success_message=success_message)
    elif request.method == 'POST':
        response = login(request)
        return render_template('login.html',success_message=response.json['message'])
        

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
    


