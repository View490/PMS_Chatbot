from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    data = request.json
    image_url = data['image_url']
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    reading = pytesseract.image_to_string(image, config='--psm 6 digits')
    reading = ''.join(filter(str.isdigit, reading))
    return jsonify({"reading": reading})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
