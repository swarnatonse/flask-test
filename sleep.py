from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from auth import login_required
import aws

bp = Blueprint('sleep', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def hello():
    if request.method == 'POST':
        sleepdata = {};
        sleepdata['updatedate'] = request.form['updatedate']
        sleepdata['phonedown'] = request.form['phonedown']
        sleepdata['activities'] = request.form['activities']
        sleepdata['bedtime'] = request.form['bedtime']
        sleepdata['lightsout'] = request.form['lightsout']
        sleepdata['howmanywakeup'] = request.form['howmanywakeup']
        sleepdata['howlongawake'] = request.form['howlongawake']
        sleepdata['wakeuptime'] = request.form['wakeuptime']
        sleepdata['arisetime'] = request.form['arisetime']
        aws.write_to_table(sleepdata)
    return render_template('hello.html')