import json
import threading
from flask import Flask, request, send_file, render_template, jsonify, url_for, redirect

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/tables', methods=['GET'])
def tables_page():
    return render_template('tables.html')


@app.route('/apply', methods=['GET'])
def apply_page():
    return render_template('apply.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
