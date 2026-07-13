from flask import Blueprint, render_template

ai_help_bp = Blueprint(
    'ai_help',
    __name__,
    url_prefix='/ai_help'
)


@ai_help_bp.route('/')
def queue():
    return render_template('ai_help/patient_overview.html')

@ai_help_bp.route('/image-analysis')
def image_analysis():
    return render_template('ai_help/image_analysis.html')

@ai_help_bp.route('/treatment-plan')
def treatment_plan():
    return render_template('ai_help/treatment_plan.html')
