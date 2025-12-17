from flask import Flask
import os

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello, World! Welcome Python!!\n'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3500))
    app.run(debug=True, host='0.0.0.0', port=port)

