"""
CareerPilot AI - Resume Intelligence Blueprint (`/resume`)
Controller for Resume Uploads, ATS Evaluation, Version History, Questions, Interactive Interview Mode, and PDF Download.
"""

import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_file, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.models.resume import ResumeUpload, ResumeAnalysis, ResumeQuestion, ResumeInterviewSession, ResumeInterviewMessage
from app.models.company_prep import CompanyProfile
from app.services.resume_service import ResumeService
from app.services.resume_version_service import ResumeVersionService
from app.services.resume_interview_service import ResumeInterviewService
from app.services.resume_pdf_report import ResumePdfReportGenerator
from app.utils.validators import validate_file_extension

resume_bp = Blueprint('resume', __name__)
resume_service = ResumeService()

PREDEFINED_ROLES = [
    "Data Analyst", "Data Scientist", "AI/ML Engineer", "Software Engineer",
    "Full Stack Developer", "Backend Developer", "Frontend Developer",
    "Business Analyst", "Cloud Engineer", "Cybersecurity Analyst", "Product Analyst"
]


@resume_bp.route('/', methods=['GET'])
@login_required
def index():
    """Main Resume Intelligence portal listing upload box, version history, and latest analysis."""
    user_resumes = resume_service.get_user_resumes(current_user.id)
    latest_analysis = resume_service.get_latest_analysis(current_user.id)
    companies = CompanyProfile.query.order_by(CompanyProfile.name.asc()).all()

    return render_template(
        'resume/index.html',
        roles=PREDEFINED_ROLES,
        companies=companies,
        user_resumes=user_resumes,
        latest_analysis=latest_analysis
    )


@resume_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Processes resume file upload, target role, company, and optional JD."""
    file = request.files.get('resume_file')
    if not file or file.filename == '':
        flash('No file selected for upload.', 'danger')
        return redirect(url_for('resume.index'))

    original_name = file.filename
    if not validate_file_extension(original_name):
        flash('Invalid file format. Please upload a PDF or DOCX document.', 'danger')
        return redirect(url_for('resume.index'))

    target_role = request.form.get('target_role', 'Software Engineer').strip()
    custom_role = request.form.get('custom_role', '').strip()
    if target_role == 'Custom' and custom_role:
        target_role = custom_role

    target_company = request.form.get('target_company', 'General Placement').strip()
    job_description = request.form.get('job_description', '').strip()

    filename = secure_filename(original_name)
    if not filename or '.' not in filename:
        ext = original_name.rsplit('.', 1)[-1].lower() if '.' in original_name else 'pdf'
        filename = f"resume.{ext}"

    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"user_{current_user.id}_{filename}")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    file.save(save_path)

    try:
        analysis = resume_service.process_and_evaluate_resume(
            user_id=current_user.id,
            file_path=save_path,
            filename=filename,
            target_role=target_role,
            target_company=target_company,
            job_description=job_description
        )
        flash('Resume uploaded and evaluated successfully with CareerPilot AI Intelligence Engine!', 'success')
        return redirect(url_for('resume.analysis_detail', analysis_id=analysis.id))
    except Exception as e:
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
            except Exception:
                pass
        current_app.logger.error(f"Resume Evaluation Failed: {e}")
        flash(f"Failed to process resume: {str(e)}", "danger")
        return redirect(url_for('resume.index'))


@resume_bp.route('/analysis/<int:analysis_id>')
@login_required
def analysis_detail(analysis_id: int):
    """Detailed multidimensional Resume Intelligence & ATS analysis dashboard."""
    analysis = db.session.get(ResumeAnalysis, analysis_id)
    if not analysis or analysis.resume.user_id != current_user.id:
        flash('Analysis report not found or access denied.', 'danger')
        return redirect(url_for('resume.index'))

    questions = ResumeQuestion.query.filter_by(resume_id=analysis.resume.id).all()
    user_resumes = resume_service.get_user_resumes(current_user.id)

    return render_template(
        'resume/analysis.html',
        analysis=analysis,
        questions=questions,
        user_resumes=user_resumes,
        roles=PREDEFINED_ROLES
    )


@resume_bp.route('/compare', methods=['GET'])
@login_required
def compare_versions():
    """Side-by-side comparison between two uploaded resume versions."""
    v1_id = request.args.get('v1', type=int)
    v2_id = request.args.get('v2', type=int)

    if not v1_id or not v2_id:
        flash('Please select two valid resume versions to compare.', 'warning')
        return redirect(url_for('resume.index'))

    v1_analysis = ResumeAnalysis.query.join(ResumeUpload).filter(ResumeUpload.id == v1_id, ResumeUpload.user_id == current_user.id).first()
    v2_analysis = ResumeAnalysis.query.join(ResumeUpload).filter(ResumeUpload.id == v2_id, ResumeUpload.user_id == current_user.id).first()

    if not v1_analysis or not v2_analysis:
        flash('Selected resume versions not found.', 'danger')
        return redirect(url_for('resume.index'))

    matrix = ResumeVersionService.compare_versions(v1_analysis, v2_analysis)

    return render_template(
        'resume/compare.html',
        matrix=matrix,
        v1_analysis=v1_analysis,
        v2_analysis=v2_analysis
    )


@resume_bp.route('/interview/start/<int:resume_id>', methods=['POST'])
@login_required
def start_interview(resume_id: int):
    """Launches an interactive 'Interview Me From My Resume' mock session."""
    upload = db.session.get(ResumeUpload, resume_id)
    if not upload or upload.user_id != current_user.id:
        return jsonify({"error": "Unauthorized or resume not found."}), 403

    session = ResumeInterviewService.start_interview_session(current_user.id, upload.id, upload.target_role)
    first_msg = ResumeInterviewMessage.query.filter_by(session_id=session.id, sender="interviewer").first()

    return jsonify({
        "session_id": session.id,
        "target_role": session.target_role,
        "greeting": first_msg.message if first_msg else "Interview session launched!"
    })


@resume_bp.route('/interview/respond/<int:session_id>', methods=['POST'])
@login_required
def respond_interview(session_id: int):
    """Evaluates candidate response during interactive mock interview session."""
    answer = request.json.get('answer', '').strip()
    if not answer:
        return jsonify({"error": "Answer text cannot be empty."}), 400

    result = ResumeInterviewService.process_candidate_response(session_id, current_user.id, answer)
    return jsonify(result)


@resume_bp.route('/download-report/<int:analysis_id>')
@login_required
def download_report(analysis_id: int):
    """Generates and downloads a clean PDF analysis report."""
    analysis = db.session.get(ResumeAnalysis, analysis_id)
    if not analysis or analysis.resume.user_id != current_user.id:
        flash('Analysis report not found.', 'danger')
        return redirect(url_for('resume.index'))

    pdf_buffer = ResumePdfReportGenerator.generate_pdf(analysis)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"CareerPilot_Resume_Report_v{analysis.resume.version_number}.pdf",
        mimetype='application/pdf'
    )


@resume_bp.route('/delete/<int:resume_id>', methods=['POST'])
@login_required
def delete_resume(resume_id: int):
    """Securely deletes resume file from disk and database records."""
    success = resume_service.delete_resume(current_user.id, resume_id)
    if success:
        flash('Resume version deleted successfully.', 'success')
    else:
        flash('Failed to delete resume file or record not found.', 'danger')
    return redirect(url_for('resume.index'))
