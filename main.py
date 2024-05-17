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
    image_np = np.array(image)

    # Use pyzbar for QR code detection
    decoded_objects = decode(image_np)

    if decoded_objects:
      qr_data_list = []
      image_draw = ImageDraw.Draw(image)  # Use PIL ImageDraw for drawing

      for idx, obj in enumerate(decoded_objects):
        qr_data = obj.data.decode('utf-8')
        qr_data_list.append(qr_data)

        # Draw the polygons around the detected QR codes
        points = obj.polygon
        pts = np.array([[point.x, point.y] for point in points],
                       np.int32).reshape((-1, 1, 2))
        cv2.polylines(image_np, [pts],
                      isClosed=True,
                      color=(0, 255, 0),
                      thickness=2)

        # Draw text label next to each QR code polygon
        text_position = (pts[0][0][0], pts[0][0][1] - 10
                         )  # Slightly above the top-left corner
        image_draw.text(text_position, f"QR-{idx+1}",
                        fill=(255, 0, 0))  # Red color text

      # Save the image with drawn polygons and text labels
      marked_image = Image.fromarray(image_np)
      marked_image.save("marked_image.png")

      # Encode the image with drawn polygons
      _, buffer = cv2.imencode('.png', image_np)
      encoded_image = io.BytesIO(buffer).getvalue()

      # Save the QR data and TF-IDF scores
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

      # Check if the data is in CSV format
      csv_data = []
      try:
        csv_reader = csv.reader(qr_data.splitlines())
        for row in csv_reader:
          csv_data.append(row)
      except Exception as e:
        csv_data = None

      if csv_data:
        return jsonify({
            "data": csv_data,
            "processed_image": encoded_image_b64
        })
      else:
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
