from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"webp", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "dfaces":
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_classifier = cv2.CascadeClassifier( cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
            for (x, y, w, h) in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
            img_rgb = cv2.cvtColor(img, cv2.COLORMAP_JET)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, img_rgb)
            return newFilename
            
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename

        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/how")
def how():
    return render_template("how.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return "error"
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return "error no file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'> here</a>")
            return render_template("index.html")
    return render_template("contact.html")

@app.route("/na")
def na():
    return render_template("na.html")


app.run(debug=True, port=5001)
