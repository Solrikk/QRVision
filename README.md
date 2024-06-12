<p align="center">
  <img src="https://github.com/Solrikk/QRVision/blob/main/assets/photo/scanner.png" alt="Logo" width="300">
</p>

<div align="center"> <h3> <a href="https://github.com/Solrikk/QRVision/blob/main/README.md">⭐English⭐</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_RU.md">Russian</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_GE.md">German</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_JP.md">Japanese</a> | <a href="README_KR.md">Korean</a> | <a href="README_CN.md">Chinese</a> </h3> </div>

-----------------

**`QRVision`** — is a web service for scanning QR codes, where the frontend interacts with an operator to capture an image through the camera, and the backend processes this image and tries to extract data from the QR codes into a database.

## ⚠️ Getting Started with QRVision: ⚠️
This section is meant to introduce you to the basics of getting started with the "QRVision" project. Let's go through the details step-by-step:

1. Python 3.10: Make sure you have Python 3.10 installed on your machine. You can download it from the official Python website.
2. Node.js: Ensure you have Node.js installed for managing frontend dependencies. Download it from the Node.js website.
3. Poetry: Install Poetry, which is used for managing Python dependencies. You can install it by running:

**_Setting Up the Backend:_**

```Shell Script
curl -sSL https://install.python-poetry.org | python3 -
```
## Setting Up the Backend
1. Clone the repository:

```Shell Script
git clone https://github.com/Solrikk/QRVision.git
cd QRVision
```
2. Install Python dependencies:

```Shell Script
poetry install
```

**_Setting Up the Frontend:_**

1. Navigate to the static directory:
```Shell Script
cd static
```

2. Install Node.js dependencies (if any, otherwise skip):
```Shell Script
npm install
```
3. Serve the frontend (if needed, otherwise skip):
There are no specific commands for serving frontend files here since Flask serves the static files. Ensure Flask is running to serve the frontend.

**_Running the Application:_**
1. Access the application:
Open your web browser and navigate to http://127.0.0.1:5000. You should see the main application interface.
2. Using the QR Scanner:
-  Allow access to your webcam when prompted.
-  Position a QR code within the view of your webcam.
-  Click the "Scan QR Code" button.
-  The captured image will be sent to the backend for processing.

Additional Notes
- Admin and Operator Access Codes:
 -  Use the code **1111** to access the operator interface.
 -  Use the code **2222** to access the admin interface.
 -  These can be adjusted in access.js if needed.

## Features ⚙️

### _Technology Stack:_

### _Backend:_

- **`Python`**: The main programming language used for implementing the server-side of the project.
- **`Flask`**: A lightweight yet powerful web framework used to create and deploy web applications. Flask provides all the necessary tools and libraries for building server-side functionalities and is based on the principle of extensibility.
- **`OpenCV`**: A computer vision library used for image processing. We use it for performing various image transformation operations that aid in improving QR code recognition, including noise filtering and distortion correction.
- **`pyzbar`**: A specialized library for decoding QR codes. It provides accurate and fast reading of information from QR codes, which is critically important.
- **`scikit-learn`**: One of the leading machine learning libraries used for versatile data processing. In our project, it is used to analyze text using the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm, which allows efficient analysis and classification of text data.
- **`numpy`**: A high-performance library for numerical computations that works with multi-dimensional arrays and matrices. It provides numerous mathematical functions, making it indispensable for data processing and performing complex calculations.

### _Frontend:_

- **`HTML`**: A markup language used to create the structure of the web page. With it, you can define various elements of the page such as headings, paragraphs, forms, and buttons.
- **`CSS`**: A stylesheet language used to style HTML elements. You can set the color, fonts, sizes, paddings, and other visual characteristics of web page elements.
- **`JavaScript`**: A programming language used to add interactivity to the web page. In this project, it is necessary for managing interactions with the operator, such as capturing an image from the camera and sending it to the server.

### _Additional Dependencies:_

- **`Poetry`**: A tool for dependency management and creating isolated virtual environments in Python. Poetry simplifies the installation and updating of packages, as well as managing versions, ensuring consistency and reproducibility of environments.
- **`pyright`**: A fast and powerful static type analyzer for Python that helps identify type errors before the code execution, thereby increasing the reliability and quality of the software.
- **`ruff`**: A linter designed to improve code quality and maintain the style. Ruff helps identify and fix stylistic errors, ensuring consistency and code cleanliness according to the set standards.

### _Deployment:_

- **`Gunicorn`**: A high-performance WSGI HTTP server for running Flask applications in a production environment. Gunicorn provides scalability and reliability for your web application, allowing it to handle a large number of simultaneous requests and ensuring stable service operation.

### _File Structure:_

```shell
/app
├── .replit
├── static
│   ├── script.js
│   └── styles.css
├── main.py
├── pyproject.toml
├── templates
│   └── index.html
├── ...
├── replit.nix
├── models.py
```
_This project structure organizes code and resources logically, simplifying development and maintenance of the application._

- **`main.py`**: The main backend file containing Flask routes and logic for image and QR code processing.
- **`templates/index.html`**: An HTML template for the main page of the application.
- **`pyproject.toml`**: A configuration file for managing project dependencies and code linting settings (Pyright and Ruff).

___

- **OpenCV (Open Source Computer Vision Library)** — is used for performing various tasks related to image processing and QR code recognition. OpenCV is a powerful tool for computer vision and image processing, providing a wide range of functions and modules, including filtering, shape transformation, object recognition, and more. With its extensive capabilities, OpenCV enables efficient image processing to improve the quality of scanning and accuracy of QR code recognition.

_Example of OpenCV in action:_
<img src="https://pbs.twimg.com/media/C2iLN6iW8AEbk5D.jpg:large">

## _The QR Code Scanning Process:_

1. When the page loads, a script is initiated that requests access to the user's webcam:

```javascript
navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Ошибка доступа к камере: ", err);
    });
```

2. The video stream from the webcam is displayed inside a **`<video>`** element, allowing the user to check the correct angle and position of the QR code before scanning. This element is placed in the center of the page for user convenience.

3. The operator clicks the "Scan QR Code" button. This action captures the current image from the webcam and draws it onto a **`<canvas>`** element.

```javascript
captureBtn.addEventListener('click', () => {
    setTimeout(() => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.style.display = 'block';
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
```

4. After drawing the image onto the `<canvas>` element, it is converted to **`Blob format`** and sent to the server endpoint **`/scan-qr/`** using the **`Fetch API`**:
```javascript
    canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'capture.png');

        fetch('/scan-qr/', {
            method: 'POST',
            body: formData
        })
```
5. On the server, Flask processes this request at the **`/scan-qr/`** endpoint. The image is first read and converted into an object using **Pillow (PIL)**:

```python
file = request.files['file']
contents = file.read()
image = Image.open(io.BytesIO(contents))
image_np = np.array(image)
```

6. The server performs several preprocessing steps on the image to improve the quality for reading QR codes. Preprocessing is done using a function called **`preprocess_image`** in multiple attempts:

```python
attempts = 12
decoded_objects = []
for attempt in range(attempts):
    processed_image = preprocess_image(image_np, attempt)
    decoded_objects = decode(Image.fromarray(processed_image))
    if decoded_objects:
        break
```
7. The library **`pyzbar`** is used to recognize and decode QR codes from preprocessed images:

```python
if decoded_objects:
    qr_data_list = []
    image_draw = ImageDraw.Draw(image)
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        qr_data_list.append(qr_data)
```

8. The server creates markers on the original image to show the location of the QR codes using **`OpenCV`**:

```python
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            cv2.polylines(image_np, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            text_position = (points[0].x, points[0].y - 10)
            image_draw.text(text_position, f"QR", fill=(255, 0, 0))
```

<img src="https://link-akyoning.replit.app/files/photo_2024-05-28_14-18-24.jpg">

9. An **`alert`** is displayed on the client side with the QR code scanning results:

```javascript
.then((data) => {
        alert('Данные QR-кода: ' + data.data);
        canvas.style.display = 'none';
    })
    .catch(error => {
        console.error('Ошибка:', error);
        canvas.style.display = 'none';
    });
```

<img src="https://link-akyoning.replit.app/files/photo_2024-05-28_14-42-14.jpg">