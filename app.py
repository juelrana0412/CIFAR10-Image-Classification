import os

from flask import (
    Flask,
    render_template,
    request
)


from werkzeug.utils import secure_filename

from model_loader import (
    load_cnn,
    load_swin
)

from predict import predict


UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -------------------------------
# Load models once
# -------------------------------
cnn_model = load_cnn("./models/CNN.pth")

swin_model = load_swin("./models/swin_model.pth")


@app.route("/")

def home():

    return render_template("index.html")


@app.route("/predict", methods=["POST"])

def classify():

    image = request.files["image"]

    selected_model = request.form["model"]

    filename = secure_filename(image.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    image.save(filepath)


    if selected_model == "cnn":

        model = cnn_model

    else:

        model = swin_model


    prediction, confidence = predict(
        filepath,
        model
    )

    return render_template(

        "index.html",

        prediction=prediction,

        confidence=confidence,

        image_path=filepath,

        selected_model=selected_model

    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 7860)),
        debug=False
    )