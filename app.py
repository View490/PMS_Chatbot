from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        data = request.json
        image_url = data.get('image_url')

        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content)).convert("L")  # grayscale

        # 💡 Resize the image (Tesseract needs less memory)
        image = image.resize((int(image.width * 0.5), int(image.height * 0.5)))

        reading = pytesseract.image_to_string(image, config='--psm 6 digits')
        reading = ''.join(filter(str.isdigit, reading))

        return jsonify({"reading": reading})

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
