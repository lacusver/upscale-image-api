from flask import Flask, request, jsonify
from PIL import Image
import base64
from io import BytesIO
import os
import glob

UPLOAD_DIR = "../ESRGAN/LR/"
RESULT_DIR = "../ESRGAN/results/"


app = Flask(__name__)

def clear_dir(path):
    files = glob.glob(os.path.join(path, '*'))
    for f in files:
        os.remove(f)


@app.route("/upscale", methods=["POST"])
def process_image():
    file = request.files['image']
    filename, ext = file.filename.split('.')
    img = Image.open(file.stream)
    clear_dir(UPLOAD_DIR)
    clear_dir(RESULT_DIR)
    # img.save(os.path.join(UPLOAD_DIR, "test.jpg"))
    img.save(os.path.join(UPLOAD_DIR, file.filename))
    os.chdir("../ESRGAN/")
    os.system("python test.py")
    os.chdir("../flask_app/")
    # result_img = Image.open(os.path.join(RESULT_DIR, "test_rlt.png"))
    result_img = Image.open(os.path.join(RESULT_DIR, f"{filename}_rlt.png"))
    buffered = BytesIO()
    result_img.save(buffered, format="PNG")
    img_byte = buffered.getvalue() 
    img_base64 = base64.b64encode(img_byte)
    img_str = img_base64.decode('utf-8')

    files = {
        "text":"upscale_result",
        "img":img_str
    }

    return jsonify(files)


if __name__ == "__main__":
    app.run(debug=True)