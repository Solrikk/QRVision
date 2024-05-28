<div align="center"> <h3> <a href="https://github.com/Solrikk/QRVision/blob/main/README.md">Englisch</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_RU.md">Russisch</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_GE.md">⭐Deutsch⭐</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_JP.md">Japanisch</a> | <a href="README_KR.md">Koreanisch</a> | <a href="README_CN.md">Chinesisch</a> </h3> </div>

-----------------

**`QRVision`** — ist ein Web-Service zur QR-Code-Scannung, bei dem das Frontend mit dem Bediener interagiert, um Bilder über die Kamera aufzunehmen, und das Backend dieses Bild verarbeitet und versucht, Daten aus den QR-Codes in einer Datenbank zu extrahieren.

## Hauptkomponenten

### _Tech-Stack:_

### _Backend:_

- **`Python`**: Primäre Programmiersprache des Projekts.
- **`Flask`**: Web-Framework zum Erstellen von Web-Anwendungen.
- **`OpenCV`**: Computer-Vision-Bibliothek zur Bildverarbeitung.
- **`pyzbar`**: Bibliothek zur Dekodierung von QR-Codes.
- **`scikit-learn`**: Machine-Learning-Bibliothek (wird für TF-IDF-Datenverarbeitung verwendet).
- **`numpy`**: Bibliothek für numerische Berechnungen in Python.
- **`SQLAlchemy`**: ORM für die Arbeit mit der Datenbank.
- **`PostgreSQL`**: DBMS zur Speicherung von QR-Codes und zugehörigen Daten.

### _Frontend:_

- **`HTML`**: Markup-Sprache zur Erstellung von Webseiten.
- **`CSS`**: Stylesheet-Sprache zur Gestaltung der Webseite.
- **`JavaScript`**: Zur Benutzerinteraktion (Bildaufnahme mit der Kamera und Senden an den Server).

### _Zusätzliche Abhängigkeiten:_

- **`Poetry`**: Tool zur Abhängigkeitsverwaltung und Erstellung virtueller Umgebungen in Python.
- **`pyright`**: Statischer Typ-Checker für Python.
- **`ruff`**: Linter zur Verbesserung der Codequalität und Einhaltung des Stils.

### _Deployment:_

- **`Gunicorn`**: WSGI HTTP-Server zum Ausführen des Flask-Apps in der Produktionsumgebung.

### _Dateistruktur:_

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
