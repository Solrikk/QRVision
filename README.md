<div align="center"> <h3> <a href="https://github.com/Solrikk/QRVision/blob/main/README.md">⭐English⭐</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_RU.md">Russian</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_GE.md">German</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_JP.md">Japanese</a> | <a href="README_KR.md">Korean</a> | <a href="README_CN.md">Chinese</a> </h3> </div>

-----------------

**`QRVision`** is a web service for scanning QR codes, where the frontend interacts with the operator to capture an image via the camera, and the backend processes this image and attempts to extract data from the QR codes into a database.

## Main Components

### _Technology Stack:_

### _Backend:_

- **`Python`**: The main programming language of the project.
- **`Flask`**: A web framework for creating web applications.
- **`OpenCV`**: A computer vision library for image processing.
- **`pyzbar`**: A library for decoding QR codes.
- **`scikit-learn`**: A machine learning library (used for data processing with TF-IDF).
- **`numpy`**: A library for numerical computations in Python.
- **`SQLAlchemy`**: An ORM for working with the database.
- **`PostgreSQL`**: A DBMS for storing QR codes and related data.

### _Frontend:_

- **`HTML`**: A markup language for creating web pages.
- **`CSS`**: A stylesheet language for styling web pages.
- **`JavaScript`**: For user interaction (capturing an image from the camera and sending it to the server).

### _Additional Dependencies:_

- **`Poetry`**: A tool for dependency management and virtual environment creation in Python.
- **`pyright`**: A static type checker for Python.
- **`ruff`**: A linter for improving code quality and style adherence.

### _Deployment:_

- **`Gunicorn`**: A WSGI HTTP server for running the Flask application in a production environment.

### _File Structure:_

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

- **`main.py`**: Основной backend файл, содержаший Flask маршруты и логику обработки изображений и QR-кодов.
- **`templates/index.html`**: HTML-шаблон для главной страницы приложения.
- **`pyproject.toml`**: Файл конфигурации для управления зависимостями проекта и настройки релевации кода (Pyright и Ruff).
________

  - **OpenCV (Open Source Computer Vision Library)** — used for various tasks related to image processing and QR code recognition. OpenCV is a powerful tool for computer vision and image processing with many features and modules:

### _Process of QR Code Scanning:_

### 1. **Image Upload**:
    - When the scan button is clicked, `JavaScript` captures the image from the camera and sends it to the server via a `POST request` .

### 2. **Receiving the Image on the Server**: 
 - Flask receives the image via endpoint `/scan-qr/`.
    - `main.py`: Server-side code receives the image using Flask and reads its content.

### 3. **Image Preprocessing**: 
- Using **`OpenCV`**, the image is transformed to enhance the visibility of the QR code.
    - In the `preprocess_image` function, the image can be converted to grayscale, blurred, rotated, or subjected to adaptive thresholding transformations.

### 4. **QR Code Decoding**: 
- The **`Pyzbar`** library decodes QR codes on the processed image.
    - `main.py`: The `decode` function from Pyzbar attempts to recognize QR codes at each stage of image preprocessing.
    - The `models.py` file defines the QR code model for the database.

### 5. **Decoding Result**: 
- If the QR code is successfully recognized, the data from the QR code is saved to PostgreSQL.
    - `main.py`: The read data is saved into **`PostgreSQL`**.
    - `db.py` configures the database connection and manages query sessions.

### 6. **Returning the Result to the Client**: 
- The processing results, including the decoded data and the processed image, are returned to the operator.
   - The server encodes the processed image in Base64 to return it in JSON format via Flask.
   - The operator is shown the result on the webpage.

### 7. **Database**:
We use PostgreSQL to store data, a DBMS that allows reliable data storage and easy scalability.
 - SQLAlchemy ORM is used to interact with the database. It simplifies data handling and enables database-independent code.
 - Models are defined in `models.py`. These models represent database table schemas and allow interaction with the data through Python classes.

**`PostgreSQL`** — is a powerful, open-source object-relational database system (ORDBMS). It supports many modern features and SQL standards.

_**Key Features of PostgreSQL:**_

1. **Open Source**: PostgreSQL is distributed under the PostgreSQL license, allowing free use, modification, and distribution of the database.

2. **Standard Compliance**: PostgreSQL supports the full set of SQL standard features and adds additional capabilities such as full-text search indexing, arrays, table inheritance, etc.

3. **Extensibility**: PostgreSQL can be easily extended with custom functions, aggregates, data types, and operators.

4. **Advanced Transaction Management**: PostgreSQL supports ACID (Atomicity, Consistency, Isolation, Durability), ensuring high data reliability.

5. **JSON Support**: PostgreSQL has powerful built-in functions for working with JSON and JSONB, making it suitable for storing flexible and complex documents.
