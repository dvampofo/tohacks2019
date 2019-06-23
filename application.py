from flask import Flask, request, render_template, redirect, url_for, session
from CalculateCost import analyse_cost
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    return "Sucess Azure deployment"


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        # print(file)
        result_cost = analyse_cost(file)
        session['result'] = result_cost
        print(result_cost)

        return redirect(url_for('.get_summary'))


@app.route('/summary')
def get_summary():
    result = session['result']
    return render_template('summary.html', result=json.loads(result))


if __name__ == '__main__':
    app.run(debug=True,port=8000)