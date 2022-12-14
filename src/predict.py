import argparse
import configparser
from datetime import datetime
import os
import json
import pickle
import shutil
import sys
import time
import traceback
import yaml

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline 
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

from logger import Logger

SHOW_LOG = True

class Predictor():

    def __init__(self) -> None:
        """
        default initialization of model
        load config, test datasets and binary model into memory
        """

        logger = Logger(SHOW_LOG)

        self.config = configparser.ConfigParser()
        self.log = logger.get_logger(__name__)
        self.config_path = os.path.join(os.getcwd(), 'config.ini')
        self.config.read(self.config_path)

        self.parser = argparse.ArgumentParser(description="Predictor")
        self.parser.add_argument("-t",
                                 "--tests",
                                 type=str,
                                 help="Select tests",
                                 required=True,
                                 default="smoke",
                                 const="smoke",
                                 nargs="?",
                                 choices=["smoke", "func"])
        self.X_test = pd.read_csv(
            self.config["SPLIT_DATA"]["X_test"], index_col=0)
        self.X_test = self.X_test['text']
        self.y_test = pd.read_csv(
            self.config["SPLIT_DATA"]["y_test"], index_col=0)
        self.y_test = self.y_test['classname']
        
        # if we can't load model there is no sense to do something else
        try:
            with open(self.config["MODEL"]["path"], "rb") as modelfile:
                self.classifier = pickle.load(modelfile)
        except FileNotFoundError:
            self.log.error(traceback.format_exc())
            sys.exit(1)
        
        self.log.info("Predictor is ready")

    def predict(self) -> bool:

        """
        main method for test, which proccess smoke of functional tests
        test type define as command string argument
        """

        args = self.parser.parse_args()

        # try to run smoke test on stored test subset of data
        if args.tests == "smoke":
            try:
                y_pred = self.classifier.predict(self.X_test)
                print('accuracy:', accuracy_score(self.y_test, y_pred))
                print('confusion matrix:')
                print(confusion_matrix(self.y_test, y_pred))
                print('classification report:')
                print(classification_report(self.y_test, y_pred))
            except Exception:
                self.log.error(traceback.format_exc())
                sys.exit(1)
            self.log.info(
                f'{self.config["MODEL"]["path"]} passed smoke tests')

        # try to run functional tests which stored in json files
        elif args.tests == "func":

            tests_path = os.path.join(os.getcwd(), "tests")
            exp_path = os.path.join(os.getcwd(), "experiments")
            for test in os.listdir(tests_path):
                with open(os.path.join(tests_path, test)) as f:

                    try:
                        data = json.load(f)
                        X = [x['text'] for x in data['X']]
                        y = [y['classname'] for y in data['y']]

                        score = self.classifier.score(X, y)
                        print(f'model has {score} score')
                    except Exception:
                        self.log.error(traceback.format_exc())
                        sys.exit(1)

                    self.log.info(
                        f'{self.config["MODEL"]["path"]} passed func test {f.name}')
                    exp_data = {
                        "model params": dict(self.config.items("MODEL")),
                        "tests": args.tests,
                        "score": str(score),
                        "X_test path": self.config["SPLIT_DATA"]["x_test"],
                        "y_test path": self.config["SPLIT_DATA"]["y_test"],
                    }

                    date_time = datetime.fromtimestamp(time.time())
                    str_date_time = date_time.strftime("%Y_%m_%d_%H_%M_%S")
                    exp_dir = os.path.join(exp_path, f'exp_{test[:6]}_{str_date_time}')
                    
                    os.mkdir(exp_dir)
                    with open(os.path.join(exp_dir,"exp_config.yaml"), 'w') as exp_f:
                        yaml.safe_dump(exp_data, exp_f, sort_keys=False)
                    
                    shutil.copy(os.path.join(os.getcwd(), "logfile.log"), os.path.join(exp_dir, "exp_logfile.log"))
                    shutil.copy(self.config["MODEL"]["path"], os.path.join(exp_dir, f'exp.sav'))
        
        return True
    
    def predict_spam(self, text: list) -> list:
        """
        method for interactive class prediction
        returns list of strings with human-readable class names

        params:
        text -- a list of strings, each string is one message for classification
        """
        return self.classifier.predict(text)


if __name__ == "__main__":
    predictor = Predictor()
    predictor.predict()