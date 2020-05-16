from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from keras.models import load_model
from Functions import process_img
import cv2
import numpy as np

app = Flask(__name__)

db_uri = 'mysql+pymysql://root:@localhost/mydb?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


@app.route("/")
def test():
    return render_template("/index.html")

@app.route("/judge.html", methods=["POST"])
def judge():
    image = request.form["image"]
    image = cv2.imread(image)
    image = image.astype(np.float)
    image /= 255
    model = load_model("Predict_model.h5")
    image = image.reshape(1, 224, 224, 3)
    result = model.predict(image)
    result = np.argmax(result)

    self_check_list = request.form.getlist("selfcheck")
    self_check_result = len(self_check_list)
    
    if result == 0:
        image_result = 0
    else:
        image_result = 1

    result_judge = image_result + self_check_result

    if result_judge <= 1:
        result_judge = "正常です"
    else:
        result_judge = "病院へいきましょう"


    return render_template("/judge.html", result = result, self_check_result = self_check_result, result_judge = result_judge)

@app.route("/diagnosis.html")
def diagnosis():
    return render_template("/diagnosis.html")

@app.route("/R.html")
def R():
    return render_template("/R.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)