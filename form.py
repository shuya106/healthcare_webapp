from flask import Flask, render_template, request, make_response, jsonify
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from flask_sqlalchemy import SQLAlchemy
import pymysql

from keras.models import load_model
from Functions import process_img
import cv2
import numpy as np

app = Flask(__name__)

db_uri = 'mysql+pymysql://root:@localhost/healthcare?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class body_temperature(db.Model):
    __talebname__ = "body_temperature"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temperature = db.Column(db.Integer)

class posts(db.Model):
    __talbename__ = "posts"
    id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    content = db.Column(db.Text())


"""
def getConnection():
    return pymysql.connect(
        host="localhost",
        db="healthcare",
        user = "root",
        password = "",
        charset = "utf8",
        cursorclass = pymysql.cursors.DictCursor
    )
"""

@app.route("/")
def test():

    """
    connection = getConnection()
    sql = "select * from body_temp"
    cursor = connection.cursor()
    cursor.execute(sql)
    db_data = cursor.fetchall()

    cursor.close()
    connection.close()
    """
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

@app.route("/confirm.html", methods=["POST"])
def confirm():

    try:
        if ("temp" in request.form):
            new_body_temp = body_temperature()
            new_body_temp.temperature = request.form["temp"]
            db.session.add(new_body_temp)
            db.session.commit()
        
        elif ("title" in request.form):
            if request.form["title"] == "" or request.form["content"] == "":
                return render_template("/not_confirm.html")

            new_memo = posts()
            new_memo.title = request.form["title"]
            new_memo.content = request.form["content"]
            db.session.add(new_memo)
            db.session.commit()

        return render_template("confirm.html")

    except:
        return render_template("/not_confirm.html")

@app.route("/not_confirm.html")
def not_confirm():
    return render_template("/not_confirm.html")
    


    

@app.route("/data_list.html")
def data_list():
    data_body_temperature = body_temperature.query.all()
    data_memo = posts.query.all()

    return render_template("data_list.html", data_body_temperature = data_body_temperature, data_memo = data_memo)

@app.route("/self_record.html")
def self_check():
    return render_template("self_record.html")

@app.route("/graph.html")
def graph():

    graph_temperature = body_temperature.query.all()
    temp_list=[]
    for temp in graph_temperature:
        temp_list.append(temp.temperature)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title('サンプル')
    plt.legend()
    plt.plot(temp_list)

    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()

    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

    #return render_template("graph.html", graph_temperature = temp_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)