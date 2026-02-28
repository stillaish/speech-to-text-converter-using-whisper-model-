from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import whisper
import os

app = Flask(__name__)

model = whisper.load_model("base")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        file = request.files.get("audio")

        if not file or file.filename == "":
            message = "Please select an audio file."
        else:
            try:
                filename = secure_filename(file.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)

                result = model.transcribe(path, fp16=False)
                message = result["text"]

            except Exception:
                message = "Error processing audio."

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)