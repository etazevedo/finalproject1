from flask import Flask, url_for, render_template, request, session, flash, redirect, Response
from helper import open_image, image_to_text, rotateImage, binarize, noise_removal, getSkewAngle, deskew, write_deskew, display, display_text, create_pdf, create_document
from datetime import timedelta
from werkzeug.utils import secure_filename
import pytesseract as tess
import webbrowser
import cv2
from PIL import Image
import requests
import os
import imutils

app = Flask(__name__)
app.secret_key = "hodor"
app.permanent_session_lifetime = timedelta(days=5)
app.config["IMAGE_UPLOADS"] = "/Users/eazevedo/Desktop/Ironhack/Curso/final_proj/static/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "TIFF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
        if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
            return True
        else:
            return False


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST", "GET"])
# put another page with functionalities here
def upload():
    return render_template("functional.html")

@app.route("/urlupload", methods=["POST", "GET"])
def urlupload():
    return render_template("urlupload.html")

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if image:
                filename = secure_filename(image.filename)
                #image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                #img = open_image(filename)
                textt = image_to_text(filename)

                print("Image saved")
                #return redirect(request.url)
                download = create_document(textt)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)
        #return webbrowser.open_new_tab('output.html', text=textt)
        return render_template("upload_image.html", text=textt)

    elif request.method == 'GET':
        return render_template("upload_image.html")


@app.route("/urloutput", methods=["POST", "GET"])
def urloutput():


    if request.method == "POST":

        urlimage = request.form["urlimage"]
        img = requests.get(urlimage).content
        with open('image_name.jpg', 'wb') as handler:
            handler.write(img)
        #img = imutils.url_to_image(urlimage)
        #image = requests.get(urlimage)
        #imgcv = cv2.imwrite('test2.jpeg', img)
        #image = Image.open(img)
        text = image_to_text('image_name.jpg')
        #display(image)
        #download = create_document(text)

        return render_template("urloutput.html", text1=text)

    elif request.method == 'GET':
        return render_template("urloutput.html")


@app.route("/preprocessing", methods=["POST", "GET"])
def preprocessing():

    if request.method == "POST":
        if request.form["noise"]:
            image = os.path(app.config["IMAGE_UPLOADS"], image.filename)
            noise_removal(cv2.imshow(os.path(app.config["IMAGE_UPLOADS"], image.filename)))
        return webbrowser.open_new_tab('output.html')

    return render_template("preprocessing.html")


@app.route("/login", methods=["POST", "GET"])
# this login has an upload button
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        # stores info as a dictionary
        session["user"] = user
        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in.")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/output")
# this has to be turned into a new tab that opens when there's an output
def output():
    return render_template("output.html")

# conditional to run the app

if __name__ == "__main__":
    app.run(debug=True)
