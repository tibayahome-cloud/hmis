from flask import Blueprint, render_template

visits_bp = Blueprint(
    'visits',
    __name__,
    url_prefix='/visits'
)


@visits_bp.route('/')
def queue():
    return render_template('visits/queue.html')

@visits_bp.route('/list')
def list():
    return render_template('visits/list.html')

@visits_bp.route('/new')
def new():
    return render_template('visits/new.html')
