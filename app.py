from os import getenv
from flask import Flask, jsonify
import requests
import json
import csv

from PyDictionary import PyDictionary
dictionary = PyDictionary()
# from flask_restful import Api

app = Flask(__name__)

app_id = getenv('api_id')
app_key = getenv('api_key')

@app.route("/")
def main():
	return jsonify({'my_home': 'welcome home'})

@app.route("/find/<word>", methods=['POST'])
def fetchMeaningOfWord(word):
    # url = f'http://pydictionary-geekpradd.rhcloud.com/api/meaning/{word}'
    meaning = dictionary.meaning(word)
    return jsonify({
        'data': meaning
    })


@app.route("/synonyms/<word>", methods=['POST'])
def fetchSynonymsOfWord(word):
    # url = f'http://pydictionary-geekpradd.rhcloud.com/api/meaning/{word}'
    meaning = dictionary.synonym(word)
    return jsonify({
        'data': meaning
    })

@app.route('/new/<word>', methods=['POST'])
def getWordFromOxford(word):
    endpoint = "entries"
    language_code = "en-us"
    word_id = word

    url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word_id.lower()
    new_word = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
    return jsonify({
        'status': new_word.status_code,
        'word': json.dumps(new_word.json())
    })

    # print("code {}\n".format(r.status_code))
    # print("text \n" + r.text)
    # print("json \n" + json.dumps(r.json()))

@app.route('/data', methods=['GET'])
def getItemFormCsv():
    with open('birthday.txt') as birthday_file:
        reader = csv.reader(birthday_file)
        line_count = 0
        for row in reader:
            if line_count == 0:
                return jsonify({
                    'message': f'column names are {", ".join(row)}'
                })
                line_count += 1
            else:
                return f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.'
                line_count += 1
        return f'Processed {line_count} lines.'

if __name__ == '__main__':
	app.run()