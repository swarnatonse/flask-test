from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from auth import login_required
from aws import (
    form_input_map, get_item_from_table, update_table, construct_update_item
)
from datetime import datetime

bp = Blueprint('sleep', __name__, url_prefix='/sleep')

@bp.route('/index')
@login_required
def index():
    return redirect(url_for('sleep.data'))

@bp.route('/data', methods=('GET', 'POST'))
@login_required
def data():
    if request.method == 'POST':
        sleepdata = {};
        for arg in form_input_map.keys():
            sleepdata[arg] = request.form[arg]
        print(construct_update_item(sleepdata))
        update_table(sleepdata)
    return render_template('sleep/data.html')
    