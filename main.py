from flask import Flask, request, jsonify, render_template
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw
import io
import cv2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import base64
import csv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True

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
    return image_np

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan-qr", methods=['POST'])
def scan_qr():
    try:
        file = request.files['file']
        if file.mimetype not in ['image/jpeg', 'image/png']:
            return jsonify({"error": "Invalid file type. Only JPEG and PNG are supported."}), 400
        if file.content_length > 5 * 1024 * 1024:
            return jsonify({"error": "File size exceeds limit of 5MB"}), 400

        contents = file.read()
        try:
            image = Image.open(io.BytesIO(contents))
        except Exception as e:
            return jsonify({"error": f"Error opening image: {str(e)}"}), 500

        image_np = np.array(image)
        attempts = 6
        decoded_objects = []

        for attempt in range(attempts):
            try:
                processed_image = preprocess_image(image_np, attempt)
                decoded_objects = decode(Image.fromarray(processed_image))
            except Exception as e:
                app.logger.error(f"Error during decoding attempt {attempt}: {str(e)}")
                continue
            if decoded_objects:
                break

        if decoded_objects:
            qr_data_list = []
            image_draw = ImageDraw.Draw(image)
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                qr_data_list.append(qr_data)
                points = obj.polygon
                if len(points) == 4:
                    pts = np.array(points, dtype=np.int32)
                    cv2.polylines(image_np, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
                    text_position = (points[0].x, points[0].y - 10)
                    image_draw.text(text_position, f"QR", fill=(255, 0, 0))

            marked_image = Image.fromarray(image_np)
            _, buffer = cv2.imencode('.png', np.array(marked_image))
            encoded_image = io.BytesIO(buffer).getvalue()

            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(qr_data_list)
            tfidf_scores = X.toarray()

            with open("qr_data.txt", "a") as txt_file:
                for idx, qr_data in enumerate(qr_data_list):
                    txt_file.write(f"Data: {qr_data}, TF-IDF Scores: {tfidf_scores[idx]}\n")

            with open("qr_data.csv", "a", newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                for idx, qr_data in enumerate(qr_data_list):
                    csvwriter.writerow([qr_data] + tfidf_scores[idx].tolist())

            encoded_image_b64 = base64.b64encode(encoded_image).decode('utf-8')
            return jsonify({
                "data": qr_data_list,
                "processed_image": encoded_image_b64
            })
        else:
            return jsonify({"error": "No QR code found."}), 404
    except Exception as e:
        app.logger.error(f"Error in /scan-qr route: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
