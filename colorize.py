from flask import Flask, request, render_template, send_from_directory
import requests
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        file = request.files['file']
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        # Using the DeepAI Colorizer API
        api_url = "https://api.deepai.org/api/colorizer"
        response = requests.post(api_url, 
                                 files={"image": open(filename, 'rb')}, 
                                 headers={'api-key': 'api-key:2fe3fffe-88c8-4670-84c8-c74755e7b347'})

        result_url = response.json()["output_url"]
        colorized_image = cv2.imread(result_url)

        output_path = os.path.join(UPLOAD_FOLDER, "colorized_" + file.filename)
        cv2.imwrite(output_path, colorized_image)

        return send_from_directory(UPLOAD_FOLDER, "colorized_" + file.filename, as_attachment=True)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
