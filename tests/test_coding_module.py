"""
CareerPilot AI - Coding & DSA Module Tests
Tests problem models, runner execution, test suite evaluation, and API endpoints.
"""

import pytest
import json
from app import db
from app.models.coding import CodingProblem, CodingSubmission, CodingBookmark, CodingProgress
from app.models.user import User
from app.services.code_runner import CodeRunnerService, LocalRunner
from app.services.coding_service import CodingService


@pytest.fixture
def auth_client(client, sample_user):
    """Logs in sample_user for client requests."""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(sample_user.id)
        sess['_fresh'] = True
    return client


@pytest.fixture
def seed_test_problem(app):
    """Creates a sample coding problem in database."""
    problem = CodingProblem(
        title="Sample Two Sum",
        slug="sample-two-sum",
        description="Find two numbers summing to target.",
        difficulty="easy",
        topic="Arrays",
        company_tags="Google, Amazon",
        xp_reward=10
    )
    problem.starter_templates = {
        "python": "import sys\nlines = sys.stdin.read().strip().split('\\n')\nnums = list(map(int, lines[0].split()))\ntarget = int(lines[1])\nprint('0 1')\n"
    }
    problem.sample_test_cases = [
        {"input": "2 7 11 15\n9", "expected_output": "0 1", "explanation": "2+7=9"}
    ]
    problem.hidden_test_cases = [
        {"input": "3 2 4\n6", "expected_output": "1 2"}
    ]
    db.session.add(problem)
    db.session.commit()
    return problem


def test_code_runner_python_success():
    """Test LocalRunner successfully executes python code."""
    runner = CodeRunnerService(LocalRunner())
    code = "import sys\nname = sys.stdin.read().strip()\nprint(f'Hello, {name}!')\n"
    res = runner.run_single(code, "python", stdin_data="CareerPilot")
    assert res.status == "Success"
    assert "Hello, CareerPilot!" in res.stdout
    assert res.execution_time_ms >= 0


def test_code_runner_timeout():
    """Test LocalRunner halts on infinite loops."""
    runner = CodeRunnerService(LocalRunner())
    code = "while True:\n    pass\n"
    res = runner.run_single(code, "python", timeout_seconds=1.0)
    assert res.status == "Time Limit Exceeded"


def test_code_runner_runtime_error():
    """Test LocalRunner captures runtime exceptions."""
    runner = CodeRunnerService(LocalRunner())
    code = "x = 1 / 0\n"
    res = runner.run_single(code, "python")
    assert res.status == "Runtime Error"
    assert "ZeroDivisionError" in res.stderr


def test_evaluate_test_suite():
    """Test grading code against test cases."""
    runner = CodeRunnerService(LocalRunner())
    code = "import sys\nnums = list(map(int, sys.stdin.read().split()))\nprint(sum(nums))\n"
    test_cases = [
        {"input": "1 2 3", "expected_output": "6", "is_sample": True},
        {"input": "10 20", "expected_output": "30", "is_sample": False},
        {"input": "5 5", "expected_output": "15", "is_sample": False}  # Will fail
    ]
    res = runner.evaluate_test_suite(code, "python", test_cases, is_submission=True)
    assert res['status'] == 'Wrong Answer'
    assert res['passed_tests'] == 2
    assert res['total_tests'] == 3


def test_coding_index_view(auth_client, seed_test_problem):
    """Test GET /coding/ landing page."""
    response = auth_client.get('/coding/')
    assert response.status_code == 200
    assert b"Coding &amp; DSA Challenges" in response.data or b"Coding & DSA Challenges" in response.data
    assert b"Sample Two Sum" in response.data


def test_coding_problem_detail_view(auth_client, seed_test_problem):
    """Test GET /coding/<slug> problem workspace."""
    response = auth_client.get(f'/coding/{seed_test_problem.slug}')
    assert response.status_code == 200
    assert b"Sample Two Sum" in response.data
    assert b"monaco-editor-container" in response.data


def test_api_run_code(auth_client, seed_test_problem):
    """Test POST /coding/api/run."""
    valid_code = (
        "import sys\n"
        "lines = sys.stdin.read().strip().split('\\n')\n"
        "print('0 1')\n"
    )
    response = auth_client.post('/coding/api/run', json={
        'slug': seed_test_problem.slug,
        'language': 'python',
        'code': valid_code
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Accepted'
    assert data['passed_tests'] == 1


def test_api_submit_solution(auth_client, seed_test_problem, sample_user):
    """Test POST /coding/api/submit and progress updates."""
    # Code passes sample test (returns "0 1") and hidden test (returns "1 2" depending on input)
    smart_code = (
        "import sys\n"
        "lines = sys.stdin.read().strip().split('\\n')\n"
        "if lines[0] == '2 7 11 15':\n"
        "    print('0 1')\n"
        "else:\n"
        "    print('1 2')\n"
    )
    response = auth_client.post('/coding/api/submit', json={
        'slug': seed_test_problem.slug,
        'language': 'python',
        'code': smart_code
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Accepted'
    assert data['passed_tests'] == 2
    assert data['total_tests'] == 2
    assert data['newly_solved'] is True

    # Verify submission record saved in database
    sub = CodingSubmission.query.filter_by(user_id=sample_user.id, problem_id=seed_test_problem.id).first()
    assert sub is not None
    assert sub.status == 'Accepted'


def test_api_toggle_bookmark(auth_client, seed_test_problem, sample_user):
    """Test POST /coding/api/bookmark."""
    response = auth_client.post('/coding/api/bookmark', json={
        'problem_id': seed_test_problem.id
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['is_bookmarked'] is True

    # Toggle again to remove
    response2 = auth_client.post('/coding/api/bookmark', json={
        'problem_id': seed_test_problem.id
    })
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2['is_bookmarked'] is False


def test_submissions_page_view(auth_client, seed_test_problem, sample_user):
    """Test GET /coding/submissions page rendering."""
    # Create sample submission
    sub = CodingSubmission(
        user_id=sample_user.id,
        problem_id=seed_test_problem.id,
        language="python",
        code_body="print('hello')",
        status="Accepted",
        execution_time_ms=10.5,
        passed_tests=2,
        total_tests=2
    )
    db.session.add(sub)
    db.session.commit()

    response = auth_client.get('/coding/submissions')
    assert response.status_code == 200
    assert b"Submission History" in response.data
    assert b"Sample Two Sum" in response.data


def test_leaderboard_page_view(auth_client):
    """Test GET /coding/leaderboard page rendering."""
    response = auth_client.get('/coding/leaderboard')
    assert response.status_code == 200
    assert b"Coding Leaderboard" in response.data


def test_api_proctor_penalty(auth_client, sample_user):
    """Test POST /coding/api/proctor/penalty applies correct XP deductions."""
    from app.models.coding import CodingProgress
    
    # Initialize user progress with some XP
    progress = CodingProgress.query.filter_by(user_id=sample_user.id).first()
    if not progress:
        progress = CodingProgress(user_id=sample_user.id)
        db.session.add(progress)
    progress.total_xp = 120
    db.session.commit()

    # Call penalty endpoint
    response = auth_client.post('/coding/api/proctor/penalty')
    assert response.status_code == 200
    data = response.get_json()
    assert data['old_xp'] == 120
    assert data['new_xp'] == 70
    assert data['deducted'] == 50
    assert data['proctor_flags'] == 2

    # Test penalty caps at 0
    response2 = auth_client.post('/coding/api/proctor/penalty')
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2['new_xp'] == 20
    assert data2['proctor_flags'] == 4

    response3 = auth_client.post('/coding/api/proctor/penalty')
    assert response3.status_code == 200
    data3 = response3.get_json()
    assert data3['new_xp'] == 0
    assert data3['proctor_flags'] == 6

