from flask import Flask, redirect, url_for, render_template, request, session

#create flask obj
app = Flask(__name__)
app.secret_key = "hodor"

@app.route("/")
#define a home page
def home():
    return render_template("index.html")

@app.route("/silfunc")
# put another page with functionalities here
def silfunc():
    return render_template("functional.html")

@app.route("/login", methods=["POST", "GET"]) #this login has an upload button
def login():
    if request.method == "POST":
        user = request.form["nm"] #stores info as a dictionary
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/output")
#this has to be turned into a new tab that opens when there's an output
def output():
    return render_template("output.html")

#conditional to run the app
if __name__ == "__main__":
    app.run(debug=True)

