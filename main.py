from flask import Flask, request, redirect, render_template
import cgi
app = Flask(__name__)

app.config['DEBUG'] = True



@app.route("/signup", methods=['POST'])
def sign_up():
    # look inside the request to figure out what the user typed
    user_name = request.form['user-name']
   
    
    
    

    # if the user typed nothing at all, redirect and tell them the error
    
    if  (user_name.strip() == "") or (len(user_name) < 3 or len(user_name) > 20):
        user_error = "Please Enter a valid user name.".format(user_name)
        return redirect("/?user_error=" + user_error)
    
    for space in user_name:
        if space.isspace():
            user_error = "User Names contain no spaces.".format(user_name)
            return redirect("/?user_error=" + user_error)

    password = request.form['password']  

    
    if (password.strip() == "")  or (len(password) < 3 or len(password) > 20):
        password_error = "Please enter a valid password".format(password)
        return redirect("/?password_error=" + password_error)
    
    for spaces in password:
        if spaces.isspace():
            password_error = "passwords contain no spaces".format(password)
            return redirect("/?password_error=" + password_error)

    password_verification = request.form['password-verify']
       
    if (password_verification.strip() != password):
        verify_error = "Password must be entered correctly in both boxes".format(password_verification)
        return redirect("/?verify_error=" + verify_error)

    email = request.form['email']
    
    if (email.strip() != ""):
        if (len(email) > 20 or len(email) < 3) or (email.strip() !=  email + "@email.com"):
            email_error = "Invalid email".format(email)
            return redirect("/?email_error=" + email_error)
        


    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    user_name_escaped = cgi.escape(user_name, quote=True)
    password_escaped = cgi.escape(password,quote=True)
    verify_escaped = cgi.escape(password_verification,quote=True)
    email_escaped = cgi.escape(email,quote=True)

    return render_template('Add_User.html', user_name=user_name)

@app.route("/")
def index():
    encoded_user_error = request.args.get("user_error")
    encoded_password_error = request.args.get('password_error')
    encoded_verify_error = request.args.get('verify_error')
    encoded_email_error = request.args.get('email_error')

    return render_template('User_Signup_Edit.html', user_error=encoded_user_error and cgi.escape(encoded_user_error, quote=True),
    password_error=encoded_password_error and cgi.escape(encoded_password_error, quote=True),
    verify_error=encoded_verify_error and cgi.escape(encoded_verify_error, quote=True),
    email_error=encoded_email_error and cgi.escape(encoded_email_error, quote=True))

app.run()