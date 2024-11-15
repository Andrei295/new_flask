from flask import Flask, redirect, render_template, request, session #python -m flask run
from flask_session import Session
from cs50 import SQL
import hashlib


data = SQL("sqlite:///C:/Users/335165/OneDrive - Milton Keynes College O365/new_flask/userdata.db") #Used to gather information from the database #This line will need changing if your database is saved somewhere else

app = Flask(__name__)


#Below is the configuration for session variables for the website
 

app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem" 
Session(app) 


@app.route("/") #Used as a default (login / register) page
def index():
        return render_template("index.html")


@app.route("/home-tutor", methods=["POST", "GET"]) #Used as a home page after the user successfully enters their correct details - they will be able to update their information here
def home_tutor(): #This is used to validate the user's entries, and direct them to appropriate pages

    if not request.form.get("Username"): #This is used to check if the username field is empty
        return redirect("/failure")

    elif not request.form.get("Password"): #This is to check if the password field is empty
        return redirect("/failure")

    else:

        name = request.form.get("Username") #This is used to store the user's entered username
        phrase = request.form.get("Password") #This is used to store the user's entered password
 

        if not data.execute("SELECT * FROM tutors WHERE Username = ?", name): #This is used to check if the username matches any names in the database
            return redirect("/failure")
        
        else:            

            value = hashlib.md5(phrase.encode()) 
            value = value.hexdigest() 

            if data.execute("SELECT * FROM tutors WHERE Username = ? AND Password = ?", name, value): #This is used to check if the password matches the password in the database
                data.execute("UPDATE tutors SET Count = 0 WHERE Username = ?", name) #This will reset the failed attempt count (this will only happen if the user enters their password correctly)

                #The code below will check the account status and redirect the user to a page based on their account's status

                if data.execute("SELECT Status FROM tutors WHERE Username = ? AND Status LIKE 1", name): #This will check if the account is active (normal)

                    users = data.execute("SELECT * FROM tutors WHERE Username = ? AND Password = ?", name, value) #This is used to ensure that only the ID of the correct user is being used instead of other users that may have the same username

                    return render_template("home_tutor.html", users= users) #A new page is open for the user to update their account information
                
                elif data.execute("SELECT Status FROM tutors WHERE Username = ? AND Status LIKE 2", name): #This will check if the account is locked
                    return redirect("/locked")
                
                elif data.execute("SELECT Status FROM tutors WHERE Username = ? AND Status LIKE 3", name): #This will check if the account needs a password reset
                    return redirect("/reset-tutor")

                elif data.execute("SELECT Status FROM tutors WHERE Username = ? AND Status LIKE 9", name): #This will check if the account is an administrator
                    data.execute("UPDATE tutors SET Count = 0 WHERE Username = ?", name) #This is used to prevent the admin from getting locked out
                    return redirect("/admin") #The admin will be sent to the admin page, where they can update the database
                
                elif data.execute("SELECT Status FROM tutors WHERE Username = ? AND Status LIKE 0", name): #This wil check if the account is inactive
                    return redirect("/inactive")

            else:

                if data.execute("SELECT Count FROM tutors WHERE Username = ? AND Count LIKE 0", name): #This will check the database for if the amount of failed attempts is 0
                    data.execute("UPDATE tutors SET Count = 1 WHERE Username = ?", name) #This will change the number of failed attempts to 1

                    return redirect("/failure")
                

                elif data.execute("SELECT Count FROM tutors WHERE Username = ? AND Count LIKE 1", name): #This will check the database for if the amount of failed attempts is 1
                    data.execute("UPDATE tutors SET Count = 2 WHERE Username = ?", name) #This will change the number of failed attempts to 2

                    return redirect("/failure")
                

                elif data.execute("SELECT Count FROM tutors WHERE Username = ? AND Count LIKE 2", name): #This will check the database for if the amount of failed attempts is 2
                    data.execute("UPDATE tutors SET Count = 3 WHERE Username = ?", name) #This will change the number of failed attempts to 3

                    return redirect("/failure")

                else:
                    data.execute("UPDATE tutors SET Status = 2 WHERE Username = ?", name) #This will set the user's status to 2, which will lock their account
                
                    return redirect("/locked")




@app.route("/home-learner", methods=["POST", "GET"]) #Used as a home page after the user successfully enters their correct details - they will be able to update their information here
def home_learner(): #This is used to validate the user's entries, and direct them to appropriate pages

    if not request.form.get("Username"): #This is used to check if the username field is empty
        return redirect("/failure")

    elif not request.form.get("Password"): #This is to check if the password field is empty
        return redirect("/failure")

    else:

        name = request.form.get("Username") #This is used to store the user's entered username
        phrase = request.form.get("Password") #This is used to store the user's entered password
 

        if not data.execute("SELECT * FROM learners WHERE Username = ?", name): #This is used to check if the username matches any names in the database
            return redirect("/failure")
        
        else:            

            value = hashlib.md5(phrase.encode()) 
            value = value.hexdigest() 

            if data.execute("SELECT * FROM learners WHERE Username = ? AND Password = ?", name, value): #This is used to check if the password matches the password in the database
                data.execute("UPDATE learners SET Count = 0 WHERE Username = ?", name) #This will reset the failed attempt count (this will only happen if the user enters their password correctly)

                #The code below will check the account status and redirect the user to a page based on their account's status

                if data.execute("SELECT Status FROM learners WHERE Username = ? AND Status LIKE 1", name): #This will check if the account is active (normal)

                    users = data.execute("SELECT * FROM learners WHERE Username = ? AND Password = ?", name, value) #This is used to ensure that only the ID of the correct user is being used instead of other users that may have the same username

                    return render_template("home_learner.html", users= users) #A new page is open for the user to update their account information
                
                elif data.execute("SELECT Status FROM learners WHERE Username = ? AND Status LIKE 2", name): #This will check if the account is locked
                    return redirect("/locked")
                
                elif data.execute("SELECT Status FROM learners WHERE Username = ? AND Status LIKE 3", name): #This will check if the account needs a password reset
                    return redirect("/reset-learner")

                elif data.execute("SELECT Status FROM learners WHERE Username = ? AND Status LIKE 9", name): #This will check if the account is an administrator
                    data.execute("UPDATE learners SET Count = 0 WHERE Username = ?", name) #This is used to prevent the admin from getting locked out
                    return redirect("/admin") #The admin will be sent to the admin page, where they can update the database
                
                elif data.execute("SELECT Status FROM learners WHERE Username = ? AND Status LIKE 0", name): #This will check if the account is inactive
                    return redirect("/inactive")

            else:

                if data.execute("SELECT Count FROM learners WHERE Username = ? AND Count LIKE 0", name): #This will check the database for if the amount of failed attempts is 0
                    data.execute("UPDATE learners SET Count = 1 WHERE Username = ?", name) #This will change the number of failed attempts to 1

                    return redirect("/failure")
                

                elif data.execute("SELECT Count FROM learners WHERE Username = ? AND Count LIKE 1", name): #This will check the database for if the amount of failed attempts is 1
                    data.execute("UPDATE learners SET Count = 2 WHERE Username = ?", name) #This will change the number of failed attempts to 2

                    return redirect("/failure")
                

                elif data.execute("SELECT Count FROM learners WHERE Username = ? AND Count LIKE 2", name): #This will check the database for if the amount of failed attempts is 2
                    data.execute("UPDATE learners SET Count = 3 WHERE Username = ?", name) #This will change the number of failed attempts to 3

                    return redirect("/failure")

                else:
                    data.execute("UPDATE learners SET Status = 2 WHERE Username = ?", name) #This will set the user's status to 2, which will lock their account
                
                    return redirect("/locked")
                

@app.route("/failure") #Used for when credentials are not entered or matched when a user attempts to login
def failure():
    return render_template("failure.html")


@app.route("/admin") #This is used to manage all users in the database
def admin():
    learners = data.execute("SELECT * FROM learners") #This is used to store all learners in a variable, then sent to the admin page for management

    tutors = data.execute("SELECT * FROM tutors") #This is used to store all tutors in a variable, then sent to the admin page for management

    return render_template("admin.html", learners= learners, tutors= tutors)


@app.route("/confirm") #This is used to present the user with a confirmation messsage after successfully registering a new user
def confirm():
    return render_template("confirm.html")


@app.route("/sign-in") #This is used to take the user to a page where they can sign in
def sign_in():

    return render_template("sign-in.html")



@app.route("/register", methods=["POST"]) #This is used to register a new user
def register():

    if not request.form.get("Username") or len(request.form.get("Username")) < 2: #This is used to check if the username field is empty #Also used to check the length of the username
        return redirect("/failure")

    elif not request.form.get("Password"): #This is to check if the password field is empty
        return redirect("/failure")
    
    elif request.form.get("Password") != request.form.get("Re-enter_Password"): #This is used to check if the original password matches the re-entered one for verification
        return redirect("/failure")

    else:

        if not request.form.get("user_type"): #This is used to get the type of user that is registering
            return redirect("/failure")


        elif request.form.get("user_type") == "tutor": #This is used to check the type of user

            username = request.form.get("Username") #This is used to store the user's entered username
            phrase = request.form.get("Password") #This is used to store the user's entered password
            mail = request.form.get("Email") #This is used to store the user's entered email
            name = request.form.get("Name") #This is used to store the user's entered name

            phrase = hash(phrase) #This is to convert the password into a hash value

            data.execute("INSERT INTO tutors (Username, Password, Email, Status, Name, Count) VALUES (?)", (username, phrase, mail, "1", name, "0")) #This will update the database with a new user

            return redirect("/confirm")
        

        elif request.form.get("user_type") == "learner": #This is used to check the type of user

            username = request.form.get("Username") #This is used to store the user's entered username
            phrase = request.form.get("Password") #This is used to store the user's entered password
            mail = request.form.get("Email") #This is used to store the user's entered email
            name = request.form.get("Name") #This is used to store the user's entered name

            phrase = hash(phrase) #This is to convert the password into a hash value

            data.execute("INSERT INTO learners (Username, Password, Email, Status, Name, Count) VALUES (?)", (username, phrase, mail, "1", name, "0")) #This will update the database with a new user

            return redirect("/confirm")



@app.route("/deregister-tutor", methods=["POST"]) #Used to deregister people
def deregister_tutor():

    ID = request.form.get("ID") #This uses a unqiue ID to identify and delete a field from a table
    if ID: 

        data.execute("DELETE FROM tutors WHERE ID = ?", ID) #This will delete any records that match a user's hidden ID

    return redirect("/admin") #This will simply return to the (updated) admin page 


@app.route("/deregister-learner", methods=["POST"]) #Used to deregister people
def deregister_learner():

    ID = request.form.get("ID") #This uses a unqiue ID to identify and delete a field from a table
    if ID: 

        data.execute("DELETE FROM learners WHERE ID = ?", ID) #This will delete any records that match a user's hidden ID

    return redirect("/admin") #This will simply return to the (updated) admin page 


@app.route("/unlock-tutor", methods=["POST"]) #This is used to unlock a user's account from the adminn page
def unlock_tutor():

    ID = request.form.get("ID")
    if ID:

        data.execute("UPDATE tutors SET Status = 3 WHERE ID = ?", ID) #This will change the user's account to unlocked, but needs a password change

    return redirect("/admin")


@app.route("/unlock-learner", methods=["POST"]) #This is used to unlock a user's account from the adminn page
def unlock_learner():

    ID = request.form.get("ID")
    if ID:

        data.execute("UPDATE learners SET Status = 3 WHERE ID = ?", ID) #This will change the user's account to unlocked, but needs a password change

    return redirect("/admin")


@app.route("/locked") #This is used to render a unique failure-like template that is only activated if a user's account is locked
def locked():

    return render_template("locked.html")


@app.route("/update-tutor", methods=["POST"]) #This will be used to update a user's account information
def update_tutor(): #This route will obtain a user's id, then update their information changed by the admin

    ID = request.form.get("ID") #This is used to store the user's hidden ID

    username = request.form.get("Username") #This is used to store the user's entered username
    phrase = request.form.get("Password") #This is used to store the user's entered password
    mail = request.form.get("Email") #This is used to store the user's entered email
    name = request.form.get("Name") #This is used to store the user's entered name

    phrase = hash(phrase) #This is to convert the password into a hash value


    #Below is a set of SQL statements that will update a user's account details
    data.execute("UPDATE tutors SET Username = ? WHERE ID = ?", username, ID)
    data.execute("UPDATE tutors SET Password = ? WHERE ID = ?", phrase, ID)
    data.execute("UPDATE tutors SET Email = ? WHERE ID = ?", mail, ID)
    data.execute("UPDATE tutors SET Name = ? WHERE ID = ?", name, ID)

    return redirect("/confirm")



@app.route("/update-learner", methods=["POST"]) #This will be used to update a user's account information
def update_learner(): #This route will obtain a user's id, then update their information changed by the admin

    ID = request.form.get("ID") #This is used to store the user's hidden ID

    username = request.form.get("Username") #This is used to store the user's entered username
    phrase = request.form.get("Password") #This is used to store the user's entered password
    mail = request.form.get("Email") #This is used to store the user's entered email
    name = request.form.get("Name") #This is used to store the user's entered name

    phrase = hash(phrase) #This is to convert the password into a hash value


    #Below is a set of SQL statements that will update a user's account details
    data.execute("UPDATE learners SET Username = ? WHERE ID = ?", username, ID)
    data.execute("UPDATE learners SET Password = ? WHERE ID = ?", phrase, ID)
    data.execute("UPDATE learners SET Email = ? WHERE ID = ?", mail, ID)
    data.execute("UPDATE learners SET Name = ? WHERE ID = ?", name, ID)

    return redirect("/confirm")


@app.route("/new-tutor", methods=["POST"]) #This wil collect the user ID, and send it off to the update page, whewre it will be used to update the correct user
def new_tutor():

    ID = request.form.get("ID")

    return render_template("update_tutor.html", ID= ID)


@app.route("/new-learner", methods=["POST"]) #This wil collect the user ID, and send it off to the update page, whewre it will be used to update the correct user
def new_learner():

    ID = request.form.get("ID")

    return render_template("update_learner.html", ID= ID)


def hash(phrase): #This is a function used to hash a new password

    object = hashlib.md5(phrase.encode())
    object = object.hexdigest()

    return object


@app.route("/inactive") #This will display a screen that will tell the user that their account is inactive
def inactive():

    return render_template("inactive.html")


@app.route("/reset-learner") #This will get a new password from a user to reset and send it to '/phrasereset'
def reset_learner():
    return render_template("reset_learner.html")


@app.route("/reset-tutor") #This will get a new password from a user to reset and send it to '/phrasereset'
def reset_tutor():
    return render_template("reset_tutor.html")


@app.route("/phrasereset-learner", methods=["POST"]) #This uses changes a user's password into their new one after receiving it from '/reset'
def phrasereset_learner():

    username = request.form.get("Username") #This is used to store the user's current username
    current = request.form.get("Current") #This is used to store the user's current password
    phrase = request.form.get("Password") #This is used to store the user's new password

    if not request.form.get("Username"): #This is used to check if the username field is empty
        return redirect("/failure")

    elif not request.form.get("Password"): #This is to check if the password field is empty
        return redirect("/failure")
    
    elif not data.execute("SELECT * FROM learners WHERE Username = ? AND Password = ?", username, current):
        return redirect("/failure")

    else:

        phrase = hash(phrase) #This is to convert the password into a hash value

        data.execute("UPDATE learners SET Password = ? WHERE Username = ?", phrase, username) #This will update the user's password
        data.execute("UPDATE learners SET Status = 1 WHERE Username = ?", username)

        return redirect("/confirm")
    


@app.route("/phrasereset-tutor", methods=["POST"]) #This uses changes a user's password into their new one after receiving it from '/reset'
def phrasereset_tutor():

    username = request.form.get("Username") #This is used to store the user's current username
    current = request.form.get("Current") #This is used to store the user's current password
    phrase = request.form.get("Password") #This is used to store the user's new password

    if not request.form.get("Username"): #This is used to check if the username field is empty
        return redirect("/failure")

    elif not request.form.get("Password"): #This is to check if the password field is empty
        return redirect("/failure")
    
    elif not data.execute("SELECT * FROM tutors WHERE Username = ? AND Password = ?", username, current):
        return redirect("/failure")

    else:

        phrase = hash(phrase) #This is to convert the password into a hash value

        data.execute("UPDATE tutors SET Password = ? WHERE Username = ?", phrase, username) #This will update the user's password
        data.execute("UPDATE tutors SET Status = 1 WHERE Username = ?", username)

        return redirect("/confirm")
    


@app.route("/deactivate-tutor", methods=["POST"]) #This is used to deactivate a user's account
def deactivate_tutor():

    ID = request.form.get("ID")

    data.execute("UPDATE tutors SET Status = 0 WHERE ID = ?", ID)

    return redirect("/admin")


@app.route("/deactivate-learner", methods=["POST"]) #This is used to deactivate a user's account
def deactivate_learner():

    ID = request.form.get("ID")

    data.execute("UPDATE learners SET Status = 0 WHERE ID = ?", ID)

    return redirect("/admin")


 
@app.route("/logout") #This is used to clear session variables when a user logs out
def logout(): 

    session.clear() 

    return redirect("/") 



@app.route("/aboutus") #Used to render the about us page
def aboutus():

    return render_template("aboutus.html")


@app.route("/contactus") #Used to render the contact us page
def contactus():

    return render_template("contactus.html")


@app.route("/accessibility") #This is used to change the zoom or colour scheme of the web page
def accessibility():

    return render_template("accessibility.html")


@app.route("/back-tutor") #This is used to return the user back to the home page
def back_tutor():

    return redirect("/home-tutor")


@app.route("/back-learner") #This is used to return the user back to the home page
def back_learner():

    return redirect("/home-learner")


@app.route("/classes") #This is used to take the user to the classes/sechedule page
def classes():

    return render_template("classes.html")


@app.route("/resources") #This is used to take the user to the resources page
def resources():

    return render_template("resources.html")


@app.route("/results", methods=["POST"]) #This is used to present to the user their search results from the resources page
def results():

    search = request.form.get("search")

    return render_template("results.html", search= search)


###List of names and passwords - so they are not forgotten

### Username: admin, Password: zxcvb --> Tutor

### Username: Andrei567, Password: qwerty --> Learner

### Username: Ben812, Pasword: jkl90 --> Tutor

