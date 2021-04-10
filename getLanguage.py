import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('merlin-c4fa7-firebase-adminsdk-7cfbn-8323034d25.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

user_ref = db.collection(u'users')
docs = user_ref.stream()

user_list = []
for doc in docs:
    user_list.append(doc.to_dict())
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

print(user_list)