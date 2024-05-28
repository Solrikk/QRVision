<div align="center"> <h3> <a href="https://github.com/Solrikk/QRVision/blob/main/README.md">英語</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_RU.md">ロシア語</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_GE.md">ドイツ語</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_JP.md">⭐日本語⭐</a> | <a href="README_KR.md">韓国語</a> | <a href="README_CN.md">中国語</a> </h3> </div>

-----------------

**`QRVision`** — は、カメラで画像をキャプチャするためにフロントエンドがオペレータと対話し、バックエンドがその画像を処理してQRコードからデータをデータベースに抽出しようとするWebサービスです。

## 主なコンポーネント

### _技術スタック:_

### _バックエンド:_

- **`Python`**: プロジェクトのメインプログラミング言語。
- **`Flask`**: Webアプリケーションを作成するためのWebフレームワーク。
- **`OpenCV`**: 画像処理のためのコンピュータビジョンライブラリ。
- **`pyzbar`**: QRコードのデコード用ライブラリ。
- **`scikit-learn`**: 機械学習ライブラリ（TF-IDFによるデータ処理に使用）。
- **`numpy`**: Pythonでの数値計算ライブラリ。
- **`SQLAlchemy`**: データベースとのやり取りに使用するORM。
- **`PostgreSQL`**: QRコードと関連データを保存するためのDBMS。

### _フロントエンド:_

- **`HTML`**: Webページを作成するためのマークアップ言語。
- **`CSS`**: Webページのスタイリング用スタイルシート言語。
- **`JavaScript`**: ユーザーインタラクション用（カメラでの画像キャプチャとサーバーへの送信）。

### _追加依存関係:_

- **`Poetry`**: Pythonでの依存関係管理と仮想環境の作成ツール。
- **`pyright`**: Pythonノための静的型チェッカー。
- **`ruff`**: コードの質とスタイルの遵守を向上させるためのリンター。

### _デプロイメント:_

- **`Gunicorn`**: Flaskアプリを本番環境で実行するためのWSGI HTTPサーバー。

### _ファイル構造:_

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
