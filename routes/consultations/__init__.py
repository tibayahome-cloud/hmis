from flask import Blueprint, render_template

consultations_bp = Blueprint(
    'consultations',
    __name__,
    url_prefix='/consultations'
)


@consultations_bp.route('/')
def queue():
    return render_template('consultations/queue.html')

@consultations_bp.route('/list')
def list():
    return render_template('consultations/list.html')

@consultations_bp.route('/new')
def new():
    return render_template('consultations/new.html')
