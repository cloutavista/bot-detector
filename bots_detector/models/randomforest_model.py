import pandas as pd
import json

from sklearn.ensemble import *
from sklearn.metrics import *
from sklearn.model_selection import *

with open('../../bots.json') as f:
    bots = json.load(f)
with open('../../non_bots.json') as f:
    non_bots = json.load(f)
for u in bots:
    items = list(u.items())
    for k, v in items:
        if isinstance(v, dict):
            for ky, val in v.items():
                u[ky] = val
            del u[k]
for u in non_bots:
    items = list(u.items())
    for k, v in items:
        if isinstance(v, dict):
            for ky, val in v.items():
                u[ky] = val
            del u[k]
bots_df = pd.DataFrame(data=bots)
non_bots_df = pd.DataFrame(data=non_bots)
bots_df['is_bot'] = True
non_bots_df['is_bot'] = False
df = pd.concat((bots_df, non_bots_df))
df = df[df.columns[df.nunique() > 1]]
drop_cols = ['PublicKeyBase58Check', 'Username', 'Description']
df = df.drop(drop_cols, axis=1)
y = df.pop('is_bot')
train_x, test_x, train_y, test_y = train_test_split(df, y, test_size=0.25, random_state=42, stratify=y)
clf = RandomForestClassifier(n_jobs=-1, n_estimators=100, random_state=42)
clf.fit(train_x, train_y)
preds = clf.predict(test_x)
print(accuracy_score(test_y, preds), f1_score(test_y, preds), matthews_corrcoef(test_y, preds))
print(classification_report(test_y, preds))
