import sendreq
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, Response
)
from auth import login_required
from aws import (
    form_input_map, get_sleepdata, update_table, construct_update_item, get_report_lambda_url, get_credentials, get_report_file
)
from datetime import datetime

bp = Blueprint('sleep', __name__, url_prefix='/sleep')

energy_val_map = {
    '1': 'Horrible',
    '2': 'Bad',
    '3': 'Average',
    '4': 'Good',
    '5': 'Great'
}

stress_val_map = {
    '1': 'Not stressed',
    '2': 'A little stressed',
    '3': 'Somewhat stressed',
    '4': 'Pretty stressed',
    '5': 'Very stressed'
}

mood_val_map = {
    '1': 'Sad',
    '2': 'Meh',
    '3': 'Just okay',
    '4': 'Good',
    '5': 'Great'
}

@bp.route('/index')
@login_required
def index():
    return render_template('sleep/index.html')

@bp.route('/data', methods=('GET', 'POST'))
@login_required
def data():
    if request.method == 'POST':
        sleepdata = {};
        for arg in form_input_map.keys():
            sleepdata[arg] = request.form[arg]
        update_table(sleepdata)
    return render_template('sleep/data.html')
    
@bp.route('/history', methods=('GET', 'POST'))
@login_required
def history():
    sleepdata = None
    if request.method == 'POST':
        if not request.form['requireddate']:
            flash('Date must be entered')
        else:
            sleepdata = get_sleepdata(request.form['requireddate'])
            if sleepdata:
                if sleepdata.get('energy1'):
                    sleepdata['energy1'] = energy_val_map[sleepdata.get('energy1')]
                if sleepdata.get('energy2'):
                    sleepdata['energy2'] = energy_val_map[sleepdata.get('energy2')]
                if sleepdata.get('energy3'):
                    sleepdata['energy3'] = energy_val_map[sleepdata.get('energy3')]
                if sleepdata.get('energy4'):    
                    sleepdata['energy4'] = energy_val_map[sleepdata.get('energy4')]
                if sleepdata.get('mood'):
                    sleepdata['mood'] = mood_val_map[sleepdata.get('mood')]
                if sleepdata.get('stress'):
                    sleepdata['stress'] = stress_val_map[sleepdata.get('stress')]
            else:
                flash('Sleep data for that day does not exist')
        
    return render_template('sleep/history.html', sleepdata=sleepdata)
    
@bp.route('/report', methods=('GET', 'POST'))
@login_required    
def report():
    report_key = None
    data_obj = None
    if request.method == 'POST':
        error = validate_date_input(request)
        if error:
            flash(error)
        else:
            report_lambda_url = get_report_lambda_url()
            credentials = get_credentials()
            data_obj = { 'startdate': request.form['startdate'], 'enddate': request.form['enddate'] }
            response = sendreq.create_request(credentials, report_lambda_url, data_obj).content
            report_key = json.loads(response).get('report_key')
            print(report_key)
    return render_template('sleep/report.html', report_key=report_key, data_obj=data_obj)
   
@bp.route('/download/<filename>')    
def download(filename):
    file = get_report_file(filename)
    return Response(file, 
                    mimetype="text/csv",
                    headers={"Content-Disposition":"attachment;filename="+filename})
                    
def validate_date_input(request):
    if not request.form['startdate']:
        return 'Start date not entered'
    if not request.form['enddate']:
        return 'End date not entered'
    if request.form['startdate'] > request.form['enddate']:
        return 'Invalid time range'
    return None
        
        
    