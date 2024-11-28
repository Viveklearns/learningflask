from flask import Flask, redirect, url_for, render_template,request, session,flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "hello"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
   _id = db.Column("id", db.Integer, primary_key = True)
   name = db.Column("name", db.String(100))
   email = db.Column ("email", db.String(100)) 

   def __init__(self,name, email= None):
      self.name = name
      self.email = email


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/user", methods = ["POST","GET"])
def user():
    email = None
    if "user" in session:
       user = session["user"]
       if request.method == "POST":
        email = request.form["emailvalue"]
        found_user = users.query.filter_by(name = user).first()
        print ("found_user", found_user)
        found_user.email = email
        print("found_user.email",found_user.email)
        print (user)
        print(email)
        db.session.commit()    

        flash ("Email submitted")
        return render_template ( "user.html")
       else:
        if "email" in session:
           email = session["email"]
        return  render_template ("user.html")
    else:
       return  render_template ("user.html")


@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/login",methods = ["POST","GET"])
def login():
    print("enteredlogin")
    if request.method == "POST":
        print("enteredpost")
        user = request.form ["nm"]
        print( user)
        session["user"] = user 
       # return redirect(url_for("user",Name = user))
       # found_user = users.query.filter_by(name = user).first()
        #print(found_user)
        #if found_user:
        usr = users(user) 
        db.session.add(usr)
        db.session.commit()
        #found_user = users.query.filter_by(name = user).first()
        #print(found_user)

   #           session["email"] = found_user.email
   #     else:
        return redirect(url_for("user"))
       

    else:   
        if "user" in session:
            return redirect(url_for("user"))
        else:
            return render_template(("login.html"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)

    return redirect(url_for("login"))

@app.route("/view", methods=["POST", "GET"])
def view():
    print("entered view")
    if request.method == "POST":
        # Uncomment and use this if "user" session is needed
        # if "user" in session:
        #     user = session["user"]
        filter_usr = request.form.get("view_nm")
        print("filter_usr", filter_usr)
        found_user = users.query.filter_by(name=filter_usr).first()
        print ("found_user",found_user)
        if found_user:
            print(found_user)
            print("found_user.email=", found_user.email)
            user_data = {"name": found_user.name, "email": found_user.email}
            print(f"User found: {user_data}")
            return render_template("view.html", user_data=user_data)
        else:
            print("No user found")
            user_data = {"name": 'No User found', "email": 'No User found'}
            return render_template("view.html", user_data=user_data)
    else:
        print("No user found")
        return render_template("view.html", user_data=None)


if __name__ == "__main__":
 with app.app_context():
    db.create_all()
    app.run(debug=True)




             