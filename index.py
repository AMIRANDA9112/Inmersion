from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('streamer.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='localhost', port=8000, debug=True)
