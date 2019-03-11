import MySQLdb
from flask import Flask, jsonify
import json
import os




# Flask App
app = Flask(__name__)

@app.route('/api/v1/swagger')
def documentation():
    datastore = {}
    with open('swagger.json', 'r') as f:
        datastore = json.load(f)
    return jsonify(datastore)

@app.route('/api/documentation')
def render_documentation():
    data = open('api.html').read()
    return data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5007))
    app.run(host="0.0.0.0", port=port, debug=True)
