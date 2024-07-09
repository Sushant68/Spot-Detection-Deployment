from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app= Flask(__name__)

folder_upload = 'uploads'
folder_result= 'results'

app.config['folder_upload']= folder_upload
app.config['folder_result']= folder_result

if not os.path.exists(folder_upload):
    os.makedirs(folder_upload)
if not os.path.exists(folder_result):
    os.makedirs(folder_result)

def spot_hot_cold(img_python):
    img= cv2.imread(img_python, cv2.IMREAD_GRAYSCALE)

    Tmin_val, Tmax_val, Tmin_loc, Tmax_loc= cv2.minMaxLoc(img)

    # Encircling the  spots
    img_color= cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_color, Tmin_loc, 4, (255, 0, 0), 3)
    cv2.circle(img_color, Tmax_loc, 4, (0, 0, 255), 3)

    # Save the result
    op_img_result_path= os.path.join(app.config['folder_result'], 'op_img.jpg')
    cv2.imwrite(op_img_result_path, img_color)

    return Tmin_loc, Tmax_loc, op_img_result_path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods= ['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file= request.files['file']
    if file.filename == '':
        return 'No Selected File'
    if file:
        filename= secure_filename(file.filename)
        file_path= os.path.join(app.config['folder_upload'], filename)
        file.save(file_path)
        Tmin_loc, Tmax_loc, op_img_result_path= spot_hot_cold(file_path)
        return render_template('result.html', min_loc= Tmin_loc, max_loc= Tmax_loc, result_image= op_img_result_path)
@app.route('/results/<filename>')
def result_file(filename):
    return send_file(os.path.join(app.config[folder_result], filename))

if __name__ == '__main__':
    app.run(debug=True)