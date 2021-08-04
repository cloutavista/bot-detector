### This script will be responsible for evaluating a given model against a curated test set ###
from sklearn.metrics import classification_report
import json
from bots_detector.models.followers_model import FollowersModel

model = FollowersModel()


def get_predictions(profiles):
    predictions = [model.predict(p) for p in profiles]
    return predictions


def evaluate_model():
    pass


def evaluate_mock_data():
    with open('../bots.json') as f:
        bots = json.load(f)
    with open('../non_bots.json') as f:
        users = json.load(f)
    y_true, y_pred = [], []
    bot_preds = get_predictions(bots)
    y_true.extend(['bot'] * len(bots))
    y_pred.extend(['bot' if pred else 'human' for pred in bot_preds])
    user_preds = get_predictions(users)
    y_pred.extend(['bot' if pred else 'human' for pred in user_preds])
    y_true.extend(['human'] * len(user_preds))
    report = classification_report(y_true, y_pred, labels=['bot', 'human'])
    print(report)


evaluate_mock_data()
