from flask import Blueprint,render_template, request
from scanner.awvs import Awvs
import xlrd

scanner = Blueprint('awvs',__name__)

A = Awvs()

@scanner.route('/awvs/scan',methods=["POST","GET"])
def awvsscan():
    if request.method == "POST":
        f = request.files['file']
        raw = f.read()
        data = xlrd.open_workbook(file_contents=raw)
        table = data.sheets()[0]
        domain = table.col_values(0)
        result = A.start_scan(domain)
        return result

    return render_template('upload.html')


@scanner.route('/awvs/result',methods=["POST"])
def awvsresult():
    if request.method == "POST":
        argsJson = request.get_json()
        domain = argsJson['domain']
        result = A.get_scan_result(domain)
        return result

@scanner.route('/awvs/report',methods=["POST"])
def awvsreport():
    if request.method=="POST":
        argsJson = request.get_json()
        domain = argsJson['domain']
        result = A.report(domain)
        return result

