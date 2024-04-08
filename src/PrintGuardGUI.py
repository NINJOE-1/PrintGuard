# Written by Joseph Vretenar and Raunak Soi
from flask import Flask, render_template, request
import PrusaLinkWrapper
import info

printer = PrusaLinkWrapper.PrusaLinkWrapper(info.printerIP, info.printerKey)

app = Flask(__name__)

@app.route('/')
def final():
    return render_template('GUITemplate.html')

# Function to handle pause printer
@app.route('/pause_printer', methods=['POST'])
def pause_printer():
    if request.method == 'POST':
        printer.pausePrint()
        print("Printer paused")
        return "Printer paused"

# Function to handle stop printer
@app.route('/stop_printer', methods=['POST'])
def stop_printer():
    if request.method == 'POST':
        printer.stopPrint()
        print("Printer stopped")
        return "Printer stopped"

if __name__ == '__main__':
    app.run(debug=True)
