<p align="center">
  <img src="https://github.com/Solrikk/QRVision/blob/main/assets/photo/scanner.png" alt="Logo" width="300">
</p>

<div align="center"> <h3> <a href="https://github.com/Solrikk/QRVision/blob/main/README.md">⭐English⭐</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_RU.md">Russian</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_GE.md">German</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_JP.md">Japanese</a> | <a href="README_KR.md">Korean</a> | <a href="README_CN.md">Chinese</a> </h3> </div>

-----------------

**`QRVision`** —  is a web service for scanning QR codes, where the frontend interacts with an operator to capture an image through the camera, and the backend processes this image and tries to extract data from the QR codes into a database.

## Main Components

### _Technology Stack:_

### _Backend:_

**`QRVision`** — is a web service for scanning QR codes, where the frontend interacts with an operator to capture an image through the camera, and the backend processes this image and tries to extract data from the QR codes into a database.

## Main Components

### _Technology Stack:_

### _Backend:_

- **`Python`**: The main programming language used for implementing the server-side of the project.
- **`Flask`**: A lightweight yet powerful web framework used to create and deploy web applications. Flask provides all the necessary tools and libraries for building server-side functionalities and is based on the principle of extensibility.
- **`OpenCV`**: A computer vision library used for image processing. We use it for performing various image transformation operations that aid in improving QR code recognition, including noise filtering and distortion correction.
- **`pyzbar`**: A specialized library for decoding QR codes. It provides accurate and fast reading of information from QR codes, which is critically important.
- **`scikit-learn`**: One of the leading machine learning libraries used for versatile data processing. In our project, it is used to analyze text using the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm, which allows efficient analysis and classification of text data.
- **`numpy`**: A high-performance library for numerical computations that works with multi-dimensional arrays and matrices. It provides numerous mathematical functions, making it indispensable for data processing and performing complex calculations.
- **`SQLAlchemy`**: An Object-Relational Mapping (ORM) tool that simplifies database interactions. SQLAlchemy allows abstraction from the details of SQL queries, providing a convenient way to work with the database through an object-oriented interface.

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
_Эта структура проекта организует код и ресурсы логичным образом, упрощая разработку и поддержку приложения._

- **`main.py`**: Основной backend файл, содержаший Flask маршруты и логику обработки изображений и QR-кодов.
- **`templates/index.html`**: HTML-шаблон для главной страницы приложения.
- **`pyproject.toml`**: Файл конфигурации для управления зависимостями проекта и настройки релевации кода (Pyright и Ruff).
________

  - **OpenCV (Open Source Computer Vision Library)** — используется для выполнения различных задач, связанных с обработкой изображений и распознаванием QR-кодов. OpenCV является мощным инструментом для компьютерного зрения и обработки изображений, предоставляющим широкий спектр функций и модулей, включая фильтрацию, преобразование формы, распознавание объектов и многое другое. Благодаря богатому набору возможностей, OpenCV позволяет эффективно обрабатывать изображения для улучшения качества сканирования и точности распознавания QR-кодов.

_Пример работы OpenCV:_
<img src="https://pbs.twimg.com/media/C2iLN6iW8AEbk5D.jpg:large">

## _Процесс сканирования QR-кодов:_

1. При загрузке страницы запускается скрипт, который запрашивает доступ к веб-камере пользователя:

```javascript
navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Ошибка доступа к камере: ", err);
    });
```

2. Видеопоток с веб-камеры отображается внутри элемента **`<video>`**, предоставляя пользователю возможность проверить корректность ракурса и положения QR-кода перед сканированием. Этот элемент находится в центре страницы для удобства пользователя.

3. Оператор нажимает кнопку "Сканировать QR-код". Это действие инициирует захват текущего изображения с веб-камеры и его отрисовку на элементе **`<canvas>`**:

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

<img src="https://link-akyoning.replit.app/files/photo_2024-05-28_14-18-24.jpg">

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

<img src="https://link-akyoning.replit.app/files/photo_2024-05-28_14-42-14.jpg">

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
5. **Поддержка JSON**: PostgreSQL имеет мощные встроенные функции для работы с JSON и JSONB, что делает его подходящим для хранения гибких и сложных документов.

6.**Масштабируемость и производительность**: PostgreSQL поддерживает широкий диапазон функций, которые позволяют масштабировать и оптимизировать производительность, включая индексы, репликацию, шардинг (разделение данных) и параллельное выполнение запросов.
