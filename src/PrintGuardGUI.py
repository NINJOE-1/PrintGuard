from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def final():
    return render_template('GUITemplate.html')
if __name__ == '__main__':
    app.run(debug=True)