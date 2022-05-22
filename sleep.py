from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from auth import login_required
import aws

bp = Blueprint('sleep', __name__)

form_input_arg = ['updatedate', 'phonedown', 'activities', 'bedtime', 'lightsout', 'howmanywakeup', 'howlongawake', 'wakeuptime', 'arisetime']

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
        finalsleepdata = merge(sleepdata)
        aws.write_to_table(finalsleepdata)
    return render_template('hello.html')
    
def merge(sleepdata):
    dateddbitem = aws.get_item_from_table(sleepdata['updatedate'])
    
    if dateddbitem.get('Item'):
        finalsleepdata = construct_o_sleepdata(dateddbitem.get('Item'))
        for arg in form_input_arg:
            if sleepdata[arg]:
                finalsleepdata[arg] = sleepdata[arg]
    else:
        finalsleepdata = sleepdata
                
    return finalsleepdata
        
        
def construct_o_sleepdata(dateddbitem):
    osleepdata = {}
    osleepdata['updatedate'] = dateddbitem['updatedate']['S']
    osleepdata['phonedown'] = dateddbitem['PhoneDownTime']['S']
    osleepdata['activities'] = dateddbitem['Activities']['S']
    osleepdata['bedtime'] = dateddbitem['Bedtime']['S']
    osleepdata['lightsout'] = dateddbitem['LightsOutTime']['S']
    osleepdata['howmanywakeup'] = dateddbitem['WakeUpCount']['S']
    osleepdata['howlongawake'] = dateddbitem['WakeUpDuration']['S']
    osleepdata['wakeuptime'] = dateddbitem['FinalWakeUpTime']['S']
    osleepdata['arisetime'] = dateddbitem['AriseTime']['S']
    return osleepdata
    