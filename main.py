from flask import Flask, request, jsonify, render_template
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw, ImageFont
import io
import cv2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import base64
import csv

app = Flask(__name__)


@app.route("/", methods=['GET'])
def read_root():
  return render_template('index.html')


@app.route("/scan-qr/", methods=['POST'])
def scan_qr():
  try:
    file = request.files['file']
    contents = file.read()
    image = Image.open(io.BytesIO(contents))

    # Convert image to OpenCV format
    image_np = np.array(image)

    # Decode QR codes using pyzbar
    decoded_objects = decode(image)

    if decoded_objects:
      qr_data_list = []
      image_draw = ImageDraw.Draw(image)

      for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        qr_data_list.append(qr_data)

        points = obj.polygon
        if len(points) == 4:
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

      vectorizer = TfidfVectorizer()
      X = vectorizer.fit_transform(qr_data_list)
      tfidf_scores = X.toarray()

      with open("qr_data.txt", "a") as file:
        for idx, qr_data in enumerate(qr_data_list):
          file.write(f"Data: {qr_data}, TF-IDF Scores: {tfidf_scores[idx]}\n")

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
      return jsonify({"data": "No QR code found."})
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
