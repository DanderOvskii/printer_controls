from flask import render_template, Blueprint
from flask_login import login_required, current_user


bp = Blueprint("main", __name__)
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user =   user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)
