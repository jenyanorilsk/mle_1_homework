import os
import traceback
from logger import Logger

from predict import Predictor
from flask import Flask, request, render_template


SHOW_LOG = True

# init logger

logger = Logger(SHOW_LOG)
log = logger.get_logger(__name__)

# init flask

server = Flask(__name__)
server.debug = True

log.info("Loading model")

# loading classification model
try:
    clf_model = Predictor()
except Exception:
    log.error(traceback.format_exc())
    sys.exit(1)


@server.route('/', methods=['GET', 'POST'])
def index():
    """
    The main procedure which works with users requests:
    GET method used for straight request to service
    POST method used for processing user input and return prediction
    
    both methods returns page with input form and result if POST method was used
    """

    # container for variables to output on the page
    page_context = None

    # if used POST method then we get text input from the request data
    # and predict class by classification model
    if request.method == 'POST':
        input_text = request.form['text']
        # where we call method predict_spam from model class
        # which special designed for interactive using
        page_context = {
            'input_text': input_text,
            'clf_result': clf_model.predict_spam([input_text])[0]
        }
        # write user input to log
        log.info(f"predict class form text: '{input_text}'")

    # render input form and pass context to output varibles
    return render_template('input_form.html', context=page_context)

# run server if we dont use this file as module
if __name__ == "__main__":
   server.run()