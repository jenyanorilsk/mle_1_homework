import os
import traceback
from logger import Logger

from predict import Predictor
from flask import Flask, request, render_template


SHOW_LOG = True

logger = Logger(SHOW_LOG)
log = logger.get_logger(__name__)


server = Flask(__name__)
server.debug = True

log.info("Loading model")

try:
    clf_model = Predictor()
except Exception:
    log.error(traceback.format_exc())
    sys.exit(1)


@server.route('/', methods=['GET', 'POST'])
def index():

    page_context = None

    if request.method == 'POST':
        input_text = request.form['text']
        page_context = {
            'input_text': input_text,
            'clf_result': clf_model.predict_spam([input_text])[0]
        }

        log.info(f"predict class form text: '{input_text}'")

    return render_template('input_form.html', context=page_context)


if __name__ == "__main__":
   server.run()