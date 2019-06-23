from flask import Flask, request, render_template
from CalculateCost import analyse_cost

app = Flask(__name__)

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
        result = analyse_cost(file)
        return result

if __name__ == '__main__':
    app.run()