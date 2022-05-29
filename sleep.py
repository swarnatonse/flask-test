import requests
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from auth import login_required
from aws import (
    form_input_map, get_sleepdata, update_table, construct_update_item, get_report_url, get_report_lambda_url
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
        error = None
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
    report_url = None
    if request.method == 'POST':
        report_lambda_url = get_report_lambda_url()
        dummyobj = {'randomkey': 'randomvalue'}
        response = requests.post(report_lambda_url, data=dummyobj)
        report_url = get_report_url(response.json().get('report_key'))
    return render_template('sleep/report.html', report_url=report_url)
    
        
    