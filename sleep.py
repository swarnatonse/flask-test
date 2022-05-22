from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from auth import login_required
from aws import (
    form_input_map, get_item_from_table, write_to_table
)

bp = Blueprint('sleep', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def hello():
    if request.method == 'POST':
        sleepdata = {};
        for arg in form_input_map.keys():
            sleepdata[arg] = request.form[arg]
        finalsleepdata = merge(sleepdata)
        write_to_table(finalsleepdata)
    return render_template('hello.html')
    
def merge(sleepdata):
    dateddbitem = get_item_from_table(sleepdata['updatedate'])
    
    if dateddbitem.get('Item'):
        finalsleepdata = construct_o_sleepdata(dateddbitem.get('Item'))
        for arg in form_input_map.keys():
            if sleepdata.get(arg):
                finalsleepdata[arg] = sleepdata[arg]
    else:
        finalsleepdata = sleepdata
                
    return finalsleepdata
        
        
def construct_o_sleepdata(dateddbitem):
    osleepdata = {}
    for key, value in form_input_map.items():
        if dateddbitem.get(value):
            osleepdata[key] = dateddbitem[value]['S']
        else:
            osleepdata[key] = None
            
    return osleepdata
    