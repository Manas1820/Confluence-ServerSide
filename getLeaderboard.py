import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
from flask import jsonify
import seaborn as sns
from skcriteria.madm import simple
from sklearn.preprocessing import minmax_scale
from skcriteria import Data, MIN, MAX

 def normalize_data(logic="minmax"):
    df = users_data.iloc[:, 1:].values.copy()
    if logic == "minmax":
        normalized_data = minmax_scale(df)
        normalized_data[:, 2] = 1 - normalized_data[:, 2]
        normalized_data[:, 3] = 1 - normalized_data[:, 3]
    elif logic == "sumNorm":
        normalized_data = df / df.sum(axis=0)
        normalized_data[:, 2] = 1 / normalized_data[:, 2]
        normalized_data[:, 3] = 1 / normalized_data[:, 3]
    elif logic == "maxNorm":
        normalized_data = df / df.max(axis=0)
        normalized_data[:, 2] = 1 / normalized_data[:, 2]
        normalized_data[:, 3] = 1 / normalized_data[:, 3]
    return normalized_data


def get_ranking():
    # Use a service account
    cred = credentials.Certificate('merlin-c4fa7-firebase-adminsdk-7cfbn-8323034d25.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    user_ref = db.collection(u'users')
    docs = user_ref.stream()
    users_data = users_data.loc[:, ['ID', 'skills_score', 'work_experience', 'rating', 'origin']]
    users_data.head(10)

    criteria_data = Data(
        users_data.iloc[:, 1:],           # the pandas dataframe
        [MAX, MAX, MAX,MIN],              # direction of goodness for each column
        anames = users_data['ID'],        # each entity's name, here  userId
        cnames = users_data.columns[1:],  # attribute/column name
        # weights=[1,1,1,1,1]             # weights for each attribute (optional)
        )

    dm = simple.WeightedSum(mnorm="sum")
    dec = dm.decide(criteria_data)

    user_list = []
    for doc in docs:
        return jsonify({user_list.append(doc.to_dict())})