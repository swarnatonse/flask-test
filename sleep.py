from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from auth import login_required
import aws

bp = Blueprint('sleep', __name__)

@bp.route('/')
@login_required
def hello():
    aws.write_to_table()
    return render_template('hello.html')