from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/test", methods =["GET"])
def test():
  return jsonify({"message" : "working"}), 200

if __name__ == "__main__":
  app.run(debug=TRUE):
