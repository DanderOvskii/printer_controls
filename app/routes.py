from flask import render_template, Blueprint


bp = Blueprint("main", __name__)
@bp.route('/')
@bp.route('/index')
def index():
    user =   user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)
