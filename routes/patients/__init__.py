from flask import Blueprint, render_template

patients_bp = Blueprint(
    'patients',
    __name__,
    url_prefix='/patients'
)

@patients_bp.route('/new')
def new():
    return render_template('patients/new.html')

@patients_bp.route('/')
def list():
    return render_template('patients/list.html')

@patients_bp.route('/triage')
def triage():
    return render_template('patients/triage.html')

@patients_bp.route('/sick-leave')
def sick_leave():
    return render_template('patients/sick_leave.html')

@patients_bp.route('/death-register')
def death_register():
    return render_template('patients/death_register.html')