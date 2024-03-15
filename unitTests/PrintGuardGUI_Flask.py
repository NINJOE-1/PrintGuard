from flask import Flask, render_template

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/camera')
def camera_feed():
    return render_template('camera_feed.html')

@app.route('/print_management')
def print_job_management():
    return render_template('print_job_management.html')

@app.route('/notifications')
def notification_center():
    return render_template('notification_center.html')

@app.route('/user_management')
def user_management():
    return render_template('user_management.html')

@app.route('/')
def final():
    return render_template('GUI_unitTest.html')
if __name__ == '__main__':
    app.run(debug=True)
