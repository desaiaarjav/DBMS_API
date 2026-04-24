from flask import Flask, request, jsonify
from flask_cors import CORS

import pipeline as core  

app = Flask(__name__)
CORS(app)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        result = core.output(core.schema_map, question)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)