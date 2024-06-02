from flask import Flask, request, jsonify, render_template, send_file
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw, ImageEnhance
import io
import numpy as np
import base64
import cv2
import csv
import os

app = Flask(__name__)

CSV_FILE = 'qrdata.csv'

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['data'])


def preprocess_image(image_np, attempt):
    if attempt == 0:
        return image_np
    elif attempt == 1:
        return cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    elif attempt == 2:
        return cv2.GaussianBlur(image_np, (5, 5), 0)
    elif attempt == 3:
        return cv2.rotate(image_np, cv2.ROTATE_90_CLOCKWISE)
    elif attempt == 4:
        return cv2.rotate(image_np, cv2.ROTATE_180)
    elif attempt == 5:
        return cv2.rotate(image_np, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif attempt == 6:
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    elif attempt == 7:
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    elif attempt == 8:
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 50, 150)
    elif attempt == 9:
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        dilated = cv2.dilate(gray, np.ones((3, 3), np.uint8), iterations=1)
        return cv2.erode(dilated, np.ones((3, 3), np.uint8), iterations=1)
    elif attempt == 10:
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        return cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
    elif attempt == 11:
        image_pil = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Sharpness(image_pil)
        enhanced_image = enhancer.enhance(2.0)
        return cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
    return image_np


def read_csv_data():
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        return list(reader)


@app.route("/", methods=['GET'])
def read_root():
    return render_template('index.html')


@app.route("/scan-qr/", methods=['POST'])
def scan_qr():
    try:
        file = request.files['file']
        contents = file.read()
        image = Image.open(io.BytesIO(contents))

        image_np = np.array(image)

        attempts = 12
        decoded_objects = []

        for attempt in range(attempts):
            processed_image = preprocess_image(image_np, attempt)
            decoded_objects = decode(Image.fromarray(processed_image))

            if decoded_objects:
                break

        if decoded_objects:
            qr_data_list = []
            image_draw = ImageDraw.Draw(image)

            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                qr_data_list.append(qr_data)

                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([qr_data])

                points = obj.polygon
                if len(points == 4):
                    pts = np.array(points, dtype=np.int32)
                    cv2.polylines(image_np, [pts],
                                  isClosed=True,
                                  color=(0, 255, 0),
                                  thickness=2)

                    text_position = (points[0].x, points[0].y - 10)
                    image_draw.text(text_position, f"QR", fill=(255, 0, 0))

            marked_image = Image.fromarray(image_np)
            marked_image.save("marked_image.png")

            _, buffer = cv2.imencode('.png', image_np)
            encoded_image = io.BytesIO(buffer).getvalue()

            encoded_image_b64 = base64.b64encode(encoded_image).decode('utf-8')

            return jsonify({
                "data": qr_data_list,
                "processed_image": encoded_image_b64
            })
        else:
            return jsonify({"data": "No QR code found."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/operator", methods=['GET'])
def operator_page():
    return render_template('operator.html')


@app.route("/admin", methods=['GET'])
def admin_page():
    return render_template('admin.html')


@app.route("/db-view", methods=['GET'])
def db_view_page():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')]
    return render_template('db_view.html', files=files)


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
