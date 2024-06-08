![Logo](https://github.com/Solrikk/QRVision/blob/main/assets/photo/scanner.png) 

<div align="center"> <h3> <a href="https://github.com/Solrikk/QRVision/blob/main/README.md"⭐>English⭐</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_RU.md">Russian</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_GE.md">German</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_JP.md">Japanese</a> | <a href="README_KR.md">Korean</a> | <a href="README_CN.md">Chinese</a> </h3> </div>

-----------------

**`QRVision`** is a web service for scanning QR codes, where the frontend interacts with the operator to capture an image through the camera, and the backend processes this image and attempts to extract data from the QR codes into a database.

## Main components

### _Tech Stack:_

### _Backend:_

- **`Python`**: The main programming language used to implement the server-side part of the project.
- **`Flask`**: A lightweight yet powerful web framework used to create and deploy web applications. Flask provides all necessary tools and libraries to form backend functionality, working on the principle of extensibility.
- **`OpenCV`**: A computer vision library used for image processing. We use it to perform various image transformation operations that contribute to better QR code recognition, including noise filtering and distortion correction.
- **`pyzbar`**: A specialized library for decoding QR codes. It ensures accurate and fast reading of information from QR codes, which is critically important.
- **`scikit-learn`**: One of the leading machine learning libraries used for versatile data processing. In our project, it's used for text analysis using the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm, which allows effective analysis and classification of text data.
- **`numpy`**: A high-performance library for numerical computations working with multi-dimensional arrays and matrices. It provides various mathematical functions, making it indispensable for data processing and complex calculations.
- **`SQLAlchemy`**: An Object-Relational Mapping (ORM) library that simplifies interaction with the database. SQLAlchemy allows you to abstract away the details of SQL queries, providing a convenient way to work with the database through an object-oriented interface.
- **`PostgreSQL`**: A powerful and scalable Database Management System (DBMS). PostgreSQL is used for reliable storage of QR codes and related data, ensuring high performance and data security.

### _Frontend:_

- **`HTML`**: A markup language used to create the structure of a webpage. It allows you to define various page elements such as headings, paragraphs, forms, and buttons.
- **`CSS`**: A style sheet language used to style HTML elements. It allows you to set colors, fonts, sizes, margins, and other visual characteristics of webpage elements.
- **`JavaScript`**: A programming language used to add interactivity to a webpage. In this project, it is needed to manage interactions with the operator, for example, capturing an image from the camera and sending it to the server.

### _Additional dependencies:_

- **`Poetry`**: A tool for dependency management and creating isolated virtual environments in Python. Poetry simplifies the installation and updating of packages as well as version management, ensuring consistency and reproducibility of environments.
- **`pyright`**: A fast and powerful static type checker for Python that helps identify type errors before code execution, thereby increasing software reliability and quality.
- **`ruff`**: A linter designed to enhance code quality and enforce code style. Ruff helps detect and fix stylistic errors, ensuring uniformity and cleanliness of code according to defined standards.

### _Deployment:_

- **`Gunicorn`**: A high-performance WSGI HTTP server for running Flask applications in a production environment. Gunicorn ensures the scalability and reliability of your web application, handling a large number of simultaneous requests and providing stable service operation.

### _File structure:_

```shell
/app
├── .replit
├── static
│   ├── script.js
│   └── styles.css
├── main.py
├── pyproject.toml
├── templates
│   └── index.html
├── ...
├── replit.nix
├── models.py
```
_This project structure organizes code and resources in a logical way, simplifying the development and maintenance of the application._

- **`main.py`**: The main backend file containing Flask routes and the logic for image and QR code processing.
- **`templates/index.html`**: The HTML template for the application's main page.
- **`pyproject.toml`**: Configuration file for project dependency management and code linting setup (Pyright and Ruff).

________

  - **OpenCV (Open Source Computer Vision Library)** is used for performing various tasks related to image processing and QR code recognition. OpenCV is a powerful tool for computer vision and image processing, providing a wide range of functions and modules, including filtering, shape transformation, object recognition, and more. Thanks to its rich feature set, OpenCV enables efficient image processing to improve scanning quality and QR code recognition accuracy.

_Example of OpenCV in action:_
<img src="https://pbs.twimg.com/media/C2iLN6iW8AEbk5D.jpg:large">

## _QR Code Scanning Process:_

1. When the page loads, a script is executed to request access to the user's webcam:

```javascript
navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing camera: ", err);
    });
```

2. The video stream from the webcam is displayed inside the <video> element, allowing the user to check the correct angle and position of the QR code before scanning. This element is placed in the center of the page for user convenience.

3. The operator clicks the "Scan QR code" button. This action starts capturing the current image from the webcam and drawing it on the <canvas> element.

```javascript
captureBtn.addEventListener('click', () => {
    setTimeout(() => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.style.display = 'block';
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
```

4. После рисования изображения на элементе <canvas>, оно конвертируется в **`Blob-формат`** и отправляется на серверный эндпоинт **`/scan-qr/`** с помощью **`Fetch API`**:
```javascript
    canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'capture.png');

        fetch('/scan-qr/', {
            method: 'POST',
            body: formData
        })
```
5. На сервере Flask обрабатывает этот запрос в эндпоинте **`/scan-qr/`**. Изображение сначала считывается и преобразуется в объект **`Pillow (PIL)`**:

```python
file = request.files['file']
contents = file.read()
image = Image.open(io.BytesIO(contents))
image_np = np.array(image)
```

6. Сервер производит серию предобработок на изображении для улучшения качества чтения QR-кодов. Предобработка выполняется функцией **`preprocess_image`** в нескольких попыток:

```python
attempts = 12
decoded_objects = []
for attempt in range(attempts):
    processed_image = preprocess_image(image_np, attempt)
    decoded_objects = decode(Image.fromarray(processed_image))
    if decoded_objects:
        break
```
7. Библиотека **`pyzbar`** используется для распознавания и декодирования QR-кодов на предобработанных изображениях:

```python
if decoded_objects:
    qr_data_list = []
    image_draw = ImageDraw.Draw(image)
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        qr_data_list.append(qr_data)
```
8. Декодированные данные QR-кода сохраняются в базу данных при помощи **`SQLAlchemy`**:

```python
        qr_data_entry = QRData(data=qr_data)
        db_session.add(qr_data_entry)
        db_session.commit()
```

9. Сервер создает метки на исходном изображении для отображения местоположения QR-кодов, используя **`OpenCV`**:

```python
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            cv2.polylines(image_np, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            text_position = (points[0].x, points[0].y - 10)
            image_draw.text(text_position, f"QR", fill=(255, 0, 0))
```

10. На клиентской стороне отображается **`alert`** с результатами сканирования QR-кодов:

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

<img src="https://github.com/Solrikk/QRVision/blob/main/assets/photo_2024-05-28_14-42-14.jpg">

### 7. **База данных:**
Для хранения данных используем PostgreSQL, СУБД, которая позволяет надежно хранить данные и легко масштабироваться.
 - SQLAlchemy ORM используется для взаимодействия с базой данных. Он упрощает работу с данными и позволяет писать код, независимый от конкретной СУБД.
 - Модели определяются в `models.py`. Они представляют собой схемы таблиц базы данных и позволяют взаимодействовать с данными через классы Python.

**`PostgreSQL`** — это мощная, объектно-реляционная база данных с открытым исходным кодом (ORDBMS). Она поддерживает множество современных функций и стандартов SQL.

_**Основные характеристики PostgreSQL:**_

1. **Открытый исходный код**: PostgreSQL распространяется под лицензией PostgreSQL, которая позволяет свободно использовать, изменять и распространять базу данных.

2. **Совместимость со стандартами**: PostgreSQL поддерживает полный набор функций стандарта SQL и добавляет дополнительные возможности, такие как индексирование полнотекстового поиска, массивы, таблицы с наследованием и др.

3. **Расширяемость**: PostgreSQL может быть легко расширена за счет Операторских функций, агрегатов, типов данных и операторов.

4. **Продвинутое управление транзакциями**: PostgreSQL поддерживает ACID (Atomicity, Consistency, Isolation, Durability), обеспечение высокой надежности данных.

5. **Поддержка JSON**: PostgreSQL имеет мощные встроенные функции для работы с JSON и JSONB, что делает его подходящим для хранения гибких и сложных документов.

6.**Масштабируемость и производительность**: PostgreSQL поддерживает широкий диапазон функций, которые позволяют масштабировать и оптимизировать производительность, включая индексы, репликацию, шардинг (разделение данных) и параллельное выполнение запросов.
