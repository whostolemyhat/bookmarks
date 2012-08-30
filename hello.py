from flask import Flask, url_for, render_template
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/about/')
def about():
    return url_for('static', filename='style.css')

if __name__ == "__main__":
    app.run(debug=True)
