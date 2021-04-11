from flask import Flask, jsonify
from flask import request
import json
import requests
import json
import config
from googlesearch import search

app = Flask(__name__)



# function to get the link of the user using the name
def get_github(name,organization, suggession_count, language):
    urls = [url for url in search(name+" "+organization+" github", num_results=suggession_count, lang=language)][:suggession_count]
    return urls

# function to get the link of the user using the name    
def get_linkedIn(name,organization,suggession_count, language):
    urls = [url for url in search(name+" "+organization+" Linkedin", num_results=suggession_count, lang=language)][:suggession_count]
    return urls

# function to check if the correct output are present
def validation_user_data(user):
    if not user['name']:
        error = "Name Not Found"
        return True
    if not user['organisation']:
        error = "Organisation Not Found"
        return True
    if not user['max_count']:
        error = "Max Count Not Found"
        return True
    return False           



# to get linked in suggessions
@app.route('/linkedin', methods=['POST'])
def suggestLinkedin():
    user = request.form
    validate = validation_user_data(user)
    urls = get_linkedIn(user["name"],user["organisation"],int(user["max_count"]),user["language"])
    print(urls)
    if not validate:
        return jsonify({"payload":{"url":urls},"error":{"status":validate}})
    else:
        return jsonify({"error":{"status":validate}})


# to get the suggessions for github account
@app.route('/github', methods=['POST'])
def suggestGithub():
    user = request.form
    validate = validation_user_data(user)
    urls = get_github(user["name"],user["organisation"],int(user["max_count"]),user["language"])
    print(urls)
    if not validate:
        return jsonify({"payload":{"url":urls},"error":{"status":validate}})
    else:
        return jsonify({"error":{"status":validate}})

# to get the leaderbord from the accounts
@app.route('/leaderbord', methods=['POST'])
def suggestRanks():
    user = req.form
    return 




# to check if the function is working or not
@app.route('/', methods=['GET'])
def basic():
    return jsonify({"payload":"Hello World"})



if __name__ == '__main__':
    app.run(threaded=True)