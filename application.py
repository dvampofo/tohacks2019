from flask import Flask, request, render_template, redirect, url_for
from CalculateCost import analyse_cost
import json

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    return "Sucess Azure deployment"

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        result = analyse_cost(file)
        return result

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        # print(file)
        result = json.dumps(analyse_cost(file))
        print(result)

        return redirect(url_for('.get_summary', result=result))


@app.route('/summary')
def get_summary():
    result = request.args['result']
    return render_template('summary.html', result=json.loads(result))


if __name__ == '__main__':
    app.run(debug=True)