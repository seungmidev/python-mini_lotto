from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dblotto


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/win-num', methods=['GET'])
def get_num():
    result = list(db.win_num.find({}, {'_id': False}).sort('drwNo', -1).limit(1))
    return jsonify({'result': 'success', 'win_num': result})


@app.route('/win-result', methods=['GET'])
def get_result():
    result = list(db.win_result.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'win_result': result})


@app.route('/store', methods=['GET'])
def get_store():
    result = list(db.store.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'store': result})


@app.route('/my-num', methods=['GET'])
def get_my_num():
    number_list = [
        request.args.get('firstRow01'),
        request.args.get('firstRow02'),
        request.args.get('firstRow03'),
        request.args.get('firstRow04'),
        request.args.get('firstRow05'),
        request.args.get('firstRow06')
    ]

    result = list(db.win_num.find({}, {'_id': False}).sort('drwNo', -1).limit(1))

    result_list = [
        result[0]['drwtNo1'],
        result[0]['drwtNo2'],
        result[0]['drwtNo3'],
        result[0]['drwtNo4'],
        result[0]['drwtNo5'],
        result[0]['drwtNo6']
    ]

    print('db result : ', result_list)

    correct_list = []
    for number in number_list:
        if int(number) in result_list:
            correct_list.append(number)
        else:
            correct_list.append(-1)

    return jsonify({'result': 'success', 'my_num': correct_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)