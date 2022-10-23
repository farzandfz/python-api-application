from flask import Flask, jsonify, request
from report_generator import report
from test_file import test_func
app = Flask(__name__)

@app.route('/api')
def api():
    NAME = request.args.get('name')
    AGE = int(request.args.get('age'))
    SEX = request.args.get('sex')
    # CUST_HEIGHT = int(request.args.get('CUST_HEIGHT'))
    # WEIGHT = int(request.args.get('WEIGHT'))
    # LIFESTYLE = request.args.get('LIFESTYLE')
    # FOOD = request.args.get('FOOD')
    # GOAL = request.args.get('GOAL')
    # GOAL2 = request.args.get('GOAL2')

    # Use this to pass a Error/ Success message
    result = report(NAME, AGE, SEX)
    
    return jsonify(result)

@app.route('/testapi')
def testapi():
    NAME = request.args.get('name')
    AGE = int(request.args.get('age'))
    SEX = request.args.get('sex')


    result = test_func(NAME, AGE, SEX)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)