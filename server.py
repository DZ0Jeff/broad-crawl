import os
from flask import Flask, request, jsonify
from flask_executor import Executor
from time import sleep

from main import main_handler
from config import is_running_crawler

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

app = Flask(__name__)
app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = True
executor = Executor(app)


@app.route('/send', methods=['POST'])
def send():
    if is_running_crawler.check_status():
        return jsonify({'status': 'crawler running...'})

    data = request.json
    executor.submit(main_handler, data)
    return { 'status': 'loading...' }


if __name__ == "__main__":
    try:
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system('ulimit -n 1000000')

        is_running_crawler.set_false()
        app.run(host="0.0.0.0")

    except Exception:
        is_running_crawler.set_false()
        raise