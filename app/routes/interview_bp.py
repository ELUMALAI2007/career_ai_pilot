"""
CareerPilot AI - Mock Interview Blueprint (`/interview`)
Controller for AI-powered mock interview practice, turn evaluations, and scores scorecard.
"""

import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.interview import InterviewSession, InterviewTurn
from app.services.interview_service import InterviewService

interview_bp = Blueprint('interview', __name__)
interview_service = InterviewService()

PREDEFINED_ROLES = [
    "Software Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer"
]

PREDEFINED_COMPANIES = [
    "TCS",
    "Infosys",
    "Accenture",
    "Amazon",
    "Microsoft",
    "Google",
    "Other"
]


@interview_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Mock interview setup form and history dashboard."""
    if request.method == 'POST':
        role = request.form.get('target_role', '').strip()
        interview_type = request.form.get('interview_type', '').strip()
        difficulty = request.form.get('difficulty', '').strip()
        company = request.form.get('target_company', '').strip()
        total_questions = interview_service.resolve_question_count(difficulty)
        resume_based_questions = request.form.get('resume_based_questions') == 'on'

        resume_id = None
        resume_file = request.files.get('resume_file')

        if resume_file and resume_file.filename != '':
            from app.utils.validators import validate_file_extension
            if not validate_file_extension(resume_file.filename):
                flash("Invalid file format. Please upload a PDF or DOCX document.", "danger")
                return redirect(url_for('interview.index'))

            from werkzeug.utils import secure_filename
            filename = secure_filename(resume_file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"user_{current_user.id}_{filename}")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            resume_file.save(save_path)

            try:
                # Process resume text and store parsed evaluation
                from app.services.resume_service import ResumeService
                resume_service_inst = ResumeService()
                analysis = resume_service_inst.process_and_evaluate_resume(
                    user_id=current_user.id,
                    file_path=save_path,
                    filename=filename,
                    target_role=role or "Software Developer",
                    target_company=company or "General Placement"
                )
                resume_id = analysis.resume_id
            except Exception as e:
                flash(f"Error parsing resume: {str(e)}", "danger")
                return redirect(url_for('interview.index'))
        else:
            # Reuse already-uploaded resume from dropdown selection
            resume_id_str = request.form.get('resume_id')
            if resume_id_str:
                try:
                    resume_id = int(resume_id_str)
                except ValueError:
                    resume_id = None

        if not resume_id:
            # Automatic fallback: select the user's latest upload
            from app.services.resume_service import ResumeService
            user_resumes = ResumeService.get_user_resumes(current_user.id)
            if user_resumes:
                resume_id = user_resumes[0].id
            else:
                flash("A resume upload is required before starting the AI Interview.", "danger")
                return redirect(url_for('interview.index'))

        try:
            session = interview_service.create_session(
                user_id=current_user.id,
                resume_id=resume_id,
                role=role or "Software Developer",
                company=company or "General",
                difficulty=difficulty or "Medium",
                interview_type=interview_type or "Technical",
                total_questions=total_questions,
                resume_based_questions=resume_based_questions
            )
            flash("Mock Interview session started!", "success")
            return redirect(url_for('interview.session', session_id=session.id))
        except Exception as e:
            flash(f"Error starting interview: {str(e)}", "danger")
            return redirect(url_for('interview.index'))

    # Load resources for lobby page
    from app.services.resume_service import ResumeService
    user_resumes = ResumeService.get_user_resumes(current_user.id)
    history_sessions = InterviewSession.query.filter_by(user_id=current_user.id).order_by(InterviewSession.created_at.desc()).all()

    return render_template(
        'interview/index.html',
        roles=PREDEFINED_ROLES,
        companies=PREDEFINED_COMPANIES,
        user_resumes=user_resumes,
        history=history_sessions
    )


@interview_bp.route('/session/<int:session_id>')
@login_required
def session(session_id):
    """Renders active mock interview simulation room."""
    session_obj = db.session.get(InterviewSession, session_id)
    if not session_obj or session_obj.user_id != current_user.id:
        flash("Mock interview session not found.", "danger")
        return redirect(url_for('interview.index'))

    if session_obj.status == 'Completed':
        flash("This session has already been completed.", "info")
        return redirect(url_for('interview.report', session_id=session_obj.id))

    return render_template('interview/session.html', session=session_obj)


@interview_bp.route('/report/<int:session_id>')
@login_required
def report(session_id):
    """Renders final evaluation report scorecard."""
    session_obj = db.session.get(InterviewSession, session_id)
    if not session_obj or session_obj.user_id != current_user.id:
        flash("Mock interview report not found.", "danger")
        return redirect(url_for('interview.index'))

    if session_obj.status != 'Completed':
        flash("This session is still in progress.", "warning")
        return redirect(url_for('interview.session', session_id=session_obj.id))

    turns = InterviewTurn.query.filter_by(session_id=session_obj.id).order_by(InterviewTurn.sequence_number.asc()).all()
    feedback = session_obj.get_final_feedback()

    return render_template(
        'interview/report.html',
        session=session_obj,
        turns=turns,
        feedback=feedback
    )


# API endpoints
@interview_bp.route('/api/submit-answer', methods=['POST'])
@login_required
def submit_answer():
    """Stores an answer and returns only the next queued question."""
    data = request.get_json() or {}
    session_id = data.get('session_id')
    answer = data.get('answer', '').strip()

    if not session_id:
        return jsonify({"success": False, "error": "Missing session_id parameter."}), 400

    if not answer:
        return jsonify({"success": False, "error": "Answer content cannot be empty."}), 400

    try:
        result = interview_service.submit_answer(session_id, answer)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error in submit-answer API: {e}")
        return jsonify({"success": False, "error": "Failed to evaluate response. Please try again."}), 500


@interview_bp.route('/api/finish-session', methods=['POST'])
@login_required
def finish_session():
    """Closes the room immediately while final scoring continues in the background."""
    data = request.get_json() or {}
    session_id = data.get('session_id')

    if not session_id:
        return jsonify({"success": False, "error": "Missing session_id parameter."}), 400

    try:
        session_obj = db.session.get(InterviewSession, session_id)
        if not session_obj or session_obj.user_id != current_user.id:
            return jsonify({"success": False, "error": "Interview session not found."}), 404
        interview_service.finalize_session_async(session_id, current_app._get_current_object())
        return jsonify({"success": True, "report_url": url_for('interview.report', session_id=session_id)})
    except Exception as e:
        current_app.logger.error(f"Error in finish-session API: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@interview_bp.route('/api/session/<int:session_id>', methods=['GET'])
@login_required
def get_session_api(session_id):
    """Fetches session metadata, history timeline, and current active question."""
    session_obj = db.session.get(InterviewSession, session_id)
    if not session_obj or session_obj.user_id != current_user.id:
        return jsonify({"success": False, "error": "Interview session not found."}), 404

    turns = InterviewTurn.query.filter_by(session_id=session_obj.id).order_by(InterviewTurn.sequence_number.asc()).all()
    history = []
    active_question = ""
    active_question_type = "Technical"
    active_turn_id = None

    for t in turns:
        if t.candidate_answer is not None:
            history.append({
                "question": t.question,
                "answer": t.candidate_answer,
                "question_type": t.question_type
            })
        else:
            active_question = t.question
            active_question_type = t.question_type or "Technical"
            active_turn_id = t.id

    return jsonify({
        "success": True,
        "session_id": session_obj.id,
        "role": session_obj.role,
        "company": session_obj.company,
        "difficulty": session_obj.difficulty,
        "interview_type": session_obj.interview_type,
        "total_questions": session_obj.total_questions,
        "current_question_no": session_obj.current_question_no,
        "status": session_obj.status,
        "active_question": active_question,
        "active_question_type": active_question_type,
        "active_turn_id": active_turn_id,
        "follow_up_count": session_obj.follow_up_count or 0,
        "max_follow_ups": interview_service.MAX_FOLLOW_UPS,
        "history": history
    })
