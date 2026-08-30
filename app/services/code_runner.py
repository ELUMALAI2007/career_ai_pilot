"""
CareerPilot AI - Code Runner Execution Service
Provides sandboxed multi-language compilation, execution, and test evaluation.
Supports Python, JavaScript, Java, and C++ with extensible runner abstractions.
"""

import os
import sys
import time
import shutil
import tempfile
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ExecutionResult:
    """Standardized single-run execution output."""
    status: str  # 'Success', 'Compilation Error', 'Runtime Error', 'Time Limit Exceeded', 'System Error'
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    execution_time_ms: float = 0.0
    memory_mb: Optional[float] = None


class BaseCodeRunner(ABC):
    """Abstract interface for code execution engines (Local subprocess, Docker container, etc.)."""

    @abstractmethod
    def execute(self, code: str, language: str, stdin_data: str = "", timeout_seconds: float = 3.0) -> ExecutionResult:
        """Executes code string with given standard input within timeout."""
        pass


class LocalRunner(BaseCodeRunner):
    """
    Local development execution runner using isolated temporary directories and subprocesses.
    Enforces process timeouts and captures output streams safely.
    """

    SUPPORTED_LANGUAGES = {'python', 'javascript', 'java', 'cpp'}

    def __init__(self):
        self.python_exec = sys.executable or 'python'
        self.node_exec = shutil.which('node') or 'node'
        self.javac_exec = shutil.which('javac') or 'javac'
        self.java_exec = shutil.which('java') or 'java'
        self.cpp_exec = shutil.which('g++') or shutil.which('clang++')

    def execute(self, code: str, language: str, stdin_data: str = "", timeout_seconds: float = 3.0) -> ExecutionResult:
        lang = (language or '').lower().strip()
        if lang not in self.SUPPORTED_LANGUAGES:
            return ExecutionResult(
                status='System Error',
                stderr=f"Language '{language}' is not supported. Supported: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )

        with tempfile.TemporaryDirectory(prefix="careerpilot_run_") as temp_dir:
            if lang == 'python':
                return self._run_python(code, temp_dir, stdin_data, timeout_seconds)
            elif lang == 'javascript':
                return self._run_javascript(code, temp_dir, stdin_data, timeout_seconds)
            elif lang == 'java':
                return self._run_java(code, temp_dir, stdin_data, timeout_seconds)
            elif lang == 'cpp':
                return self._run_cpp(code, temp_dir, stdin_data, timeout_seconds)

        return ExecutionResult(status='System Error', stderr="Execution context failed to initialize.")

    def _run_python(self, code: str, temp_dir: str, stdin_data: str, timeout: float) -> ExecutionResult:
        file_path = os.path.join(temp_dir, "solution.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        start_time = time.perf_counter()
        try:
            proc = subprocess.run(
                [self.python_exec, file_path],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1"}
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            
            if proc.returncode == 0:
                return ExecutionResult(
                    status='Success',
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    exit_code=proc.returncode,
                    execution_time_ms=round(elapsed_ms, 2)
                )
            else:
                return ExecutionResult(
                    status='Runtime Error',
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    exit_code=proc.returncode,
                    execution_time_ms=round(elapsed_ms, 2)
                )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status='Time Limit Exceeded',
                stderr=f"Time limit of {timeout}s exceeded.",
                execution_time_ms=timeout * 1000.0
            )
        except Exception as e:
            return ExecutionResult(status='System Error', stderr=str(e))

    def _run_javascript(self, code: str, temp_dir: str, stdin_data: str, timeout: float) -> ExecutionResult:
        file_path = os.path.join(temp_dir, "solution.js")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        start_time = time.perf_counter()
        try:
            proc = subprocess.run(
                [self.node_exec, file_path],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            if proc.returncode == 0:
                return ExecutionResult(
                    status='Success',
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    exit_code=proc.returncode,
                    execution_time_ms=round(elapsed_ms, 2)
                )
            else:
                return ExecutionResult(
                    status='Runtime Error',
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    exit_code=proc.returncode,
                    execution_time_ms=round(elapsed_ms, 2)
                )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status='Time Limit Exceeded',
                stderr=f"Time limit of {timeout}s exceeded.",
                execution_time_ms=timeout * 1000.0
            )
        except FileNotFoundError:
            return ExecutionResult(
                status='System Error',
                stderr="Node.js runtime was not found on the host environment."
            )
        except Exception as e:
            return ExecutionResult(status='System Error', stderr=str(e))

    def _run_java(self, code: str, temp_dir: str, stdin_data: str, timeout: float) -> ExecutionResult:
        # Detect class name or default to Main / Solution
        class_name = "Solution"
        if "class Main" in code or "public class Main" in code:
            class_name = "Main"
        
        file_path = os.path.join(temp_dir, f"{class_name}.java")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 1. Compile
        try:
            compile_proc = subprocess.run(
                [self.javac_exec, f"{class_name}.java"],
                capture_output=True,
                text=True,
                timeout=5.0,
                cwd=temp_dir
            )
            if compile_proc.returncode != 0:
                return ExecutionResult(
                    status='Compilation Error',
                    stderr=compile_proc.stderr or compile_proc.stdout,
                    exit_code=compile_proc.returncode
                )
        except subprocess.TimeoutExpired:
            return ExecutionResult(status='Compilation Error', stderr="Java compilation timed out.")
        except FileNotFoundError:
            return ExecutionResult(status='System Error', stderr="JDK 'javac' was not found on the host environment.")

        # 2. Execute
        start_time = time.perf_counter()
        try:
            run_proc = subprocess.run(
                [self.java_exec, "-Xmx128m", class_name],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            if run_proc.returncode == 0:
                return ExecutionResult(
                    status='Success',
                    stdout=run_proc.stdout,
                    stderr=run_proc.stderr,
                    exit_code=run_proc.returncode,
                    execution_time_ms=round(elapsed_ms, 2)
                )
            else:
                return ExecutionResult(
                    status='Runtime Error',
                    stdout=run_proc.stdout,
                    stderr=run_proc.stderr,
                    exit_code=run_proc.returncode,
                    execution_time_ms=round(elapsed_ms, 2)
                )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status='Time Limit Exceeded',
                stderr=f"Time limit of {timeout}s exceeded.",
                execution_time_ms=timeout * 1000.0
            )
        except Exception as e:
            return ExecutionResult(status='System Error', stderr=str(e))

    def _run_cpp(self, code: str, temp_dir: str, stdin_data: str, timeout: float) -> ExecutionResult:
        if not self.cpp_exec:
            return ExecutionResult(
                status='System Error',
                stderr="C++ compiler (g++/clang++) is not detected in local environment. Please install MinGW/GCC or use Docker runner."
            )

        src_path = os.path.join(temp_dir, "solution.cpp")
        bin_name = "solution.exe" if os.name == 'nt' else "solution.out"
        bin_path = os.path.join(temp_dir, bin_name)

        with open(src_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 1. Compile
        try:
            compile_proc = subprocess.run(
                [self.cpp_exec, "-O2", "-std=c++17", "solution.cpp", "-o", bin_name],
                capture_output=True,
                text=True,
                timeout=6.0,
                cwd=temp_dir
            )
            if compile_proc.returncode != 0:
                return ExecutionResult(
                    status='Compilation Error',
                    stderr=compile_proc.stderr or compile_proc.stdout,
                    exit_code=compile_proc.returncode
                )
        except subprocess.TimeoutExpired:
            return ExecutionResult(status='Compilation Error', stderr="C++ compilation timed out.")
        except Exception as e:
            return ExecutionResult(status='System Error', stderr=f"Compilation error: {str(e)}")

        # 2. Execute
        start_time = time.perf_counter()
        try:
            run_proc = subprocess.run(
                [bin_path],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            if run_proc.returncode == 0:
                return ExecutionResult(
                    status='Success',
                    stdout=run_proc.stdout,
                    stderr=run_proc.stderr,
                    exit_code=run_proc.returncode,
                    execution_time_ms=round(elapsed_ms, 2)
                )
            else:
                return ExecutionResult(
                    status='Runtime Error',
                    stdout=run_proc.stdout,
                    stderr=run_proc.stderr,
                    exit_code=run_proc.returncode,
                    execution_time_ms=round(elapsed_ms, 2)
                )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status='Time Limit Exceeded',
                stderr=f"Time limit of {timeout}s exceeded.",
                execution_time_ms=timeout * 1000.0
            )
        except Exception as e:
            return ExecutionResult(status='System Error', stderr=str(e))


class ContainerRunner(BaseCodeRunner):
    """
    Docker container isolated sandbox runner (for production deployment).
    Executes in ephemeral, unprivileged container with network disabled and strict limits.
    """

    def __init__(self, image_map: dict = None):
        self.image_map = image_map or {
            'python': 'python:3.12-slim',
            'javascript': 'node:20-slim',
            'java': 'openjdk:17-slim',
            'cpp': 'gcc:latest'
        }

    def execute(self, code: str, language: str, stdin_data: str = "", timeout_seconds: float = 3.0) -> ExecutionResult:
        # Ready for Docker integration
        return ExecutionResult(
            status='System Error',
            stderr="Container execution runner requested but Docker daemon is currently not enabled in dev mode."
        )


class CodeRunnerService:
    """
    Orchestration service for code execution and test suite grading.
    Normalizes outputs and evaluates candidate code against sample and hidden test cases.
    """

    def __init__(self, runner: BaseCodeRunner = None):
        self.runner = runner or LocalRunner()

    @staticmethod
    def normalize_output(text: str) -> str:
        """Normalizes newlines, trims trailing whitespace per line and overall string."""
        if text is None:
            return ""
        lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").strip().split("\n")]
        return "\n".join(lines).strip()

    def run_single(self, code: str, language: str, stdin_data: str = "", timeout: float = 3.0, timeout_seconds: float = None) -> ExecutionResult:
        """Executes source code once with provided input."""
        eff_timeout = timeout_seconds if timeout_seconds is not None else timeout
        return self.runner.execute(code, language, stdin_data, eff_timeout)

    def evaluate_test_suite(
        self,
        code: str,
        language: str,
        test_cases: List[Dict[str, Any]],
        is_submission: bool = False,
        timeout_per_test: float = 3.0
    ) -> Dict[str, Any]:
        """
        Executes code against a collection of test cases.
        Calculates pass/fail status, average/max runtime, and formats test report.
        """
        if not test_cases:
            return {
                'status': 'Accepted',
                'passed_tests': 0,
                'total_tests': 0,
                'execution_time_ms': 0.0,
                'memory_mb': None,
                'stdout': '',
                'error_log': '',
                'test_results': []
            }

        passed_count = 0
        total_count = len(test_cases)
        total_time_ms = 0.0
        final_status = 'Accepted'
        error_log = ""
        sample_stdout = ""
        test_reports = []

        for idx, tc in enumerate(test_cases, 1):
            input_val = str(tc.get('input', ''))
            expected_val = str(tc.get('expected_output', ''))
            is_sample = tc.get('is_sample', False)

            res = self.runner.execute(code, language, input_val, timeout_per_test)
            total_time_ms += res.execution_time_ms

            if idx == 1 and res.stdout:
                sample_stdout = res.stdout

            # Check execution health
            if res.status == 'Compilation Error':
                final_status = 'Compilation Error'
                error_log = res.stderr or "Compilation failed."
                test_reports.append({
                    'test_num': idx,
                    'passed': False,
                    'status': 'Compilation Error',
                    'execution_time_ms': res.execution_time_ms,
                    'is_sample': is_sample,
                    'input': input_val if (is_sample or not is_submission) else None,
                    'expected_output': expected_val if (is_sample or not is_submission) else None,
                    'actual_output': res.stdout if (is_sample or not is_submission) else None,
                    'error': res.stderr
                })
                break  # Stop immediately on compilation failure

            elif res.status == 'Time Limit Exceeded':
                final_status = 'Time Limit Exceeded'
                error_log = res.stderr or "Execution exceeded time limit."
                test_reports.append({
                    'test_num': idx,
                    'passed': False,
                    'status': 'Time Limit Exceeded',
                    'execution_time_ms': res.execution_time_ms,
                    'is_sample': is_sample,
                    'input': input_val if (is_sample or not is_submission) else None,
                    'expected_output': expected_val if (is_sample or not is_submission) else None,
                    'actual_output': None,
                    'error': res.stderr
                })
                break

            elif res.status in ('Runtime Error', 'System Error'):
                if final_status == 'Accepted':
                    final_status = 'Runtime Error'
                error_log = res.stderr
                test_reports.append({
                    'test_num': idx,
                    'passed': False,
                    'status': 'Runtime Error',
                    'execution_time_ms': res.execution_time_ms,
                    'is_sample': is_sample,
                    'input': input_val if (is_sample or not is_submission) else None,
                    'expected_output': expected_val if (is_sample or not is_submission) else None,
                    'actual_output': res.stdout if (is_sample or not is_submission) else None,
                    'error': res.stderr
                })

            else:
                # Compare output
                actual_clean = self.normalize_output(res.stdout)
                expected_clean = self.normalize_output(expected_val)
                passed = (actual_clean == expected_clean)

                if passed:
                    passed_count += 1
                    status_str = 'Passed'
                else:
                    if final_status == 'Accepted':
                        final_status = 'Wrong Answer'
                    status_str = 'Wrong Answer'

                test_reports.append({
                    'test_num': idx,
                    'passed': passed,
                    'status': status_str,
                    'execution_time_ms': res.execution_time_ms,
                    'is_sample': is_sample,
                    'input': input_val if (is_sample or not is_submission) else None,
                    'expected_output': expected_val if (is_sample or not is_submission) else None,
                    'actual_output': actual_clean if (is_sample or not is_submission) else None,
                    'error': res.stderr if not passed else ''
                })

        avg_time = round(total_time_ms / max(1, len(test_reports)), 2)

        return {
            'status': final_status,
            'passed_tests': passed_count,
            'total_tests': total_count,
            'execution_time_ms': avg_time,
            'memory_mb': None,
            'stdout': sample_stdout,
            'error_log': error_log,
            'test_results': test_reports
        }
