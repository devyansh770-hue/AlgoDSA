"""
Judge0 API integration service.

Supports both real Judge0 API (via RapidAPI) and a mock mode
for local development without an API key.
"""
import time
import json
import random
import requests
from django.conf import settings


# Judge0 language IDs
LANGUAGE_IDS = {
    'python': 71,      # Python 3
    'javascript': 63,  # Node.js
    'cpp': 54,         # C++ (GCC)
    'java': 62,        # Java (OpenJDK)
}


class Judge0Service:
    """Service for executing code via Judge0 API."""

    def __init__(self):
        self.api_url = settings.JUDGE0_API_URL
        self.api_key = settings.JUDGE0_API_KEY
        self.mock = settings.JUDGE0_MOCK
        self.headers = {
            'Content-Type': 'application/json',
        }
        if self.api_key:
            self.headers['X-RapidAPI-Key'] = self.api_key
            self.headers['X-RapidAPI-Host'] = 'judge0-ce.p.rapidapi.com'

    def execute(self, code, language, test_cases):
        """
        Execute code against test cases.

        Args:
            code: Source code string
            language: Language key (python, javascript, cpp, java)
            test_cases: List of TestCase model instances

        Returns:
            dict with keys: status, results, runtime_ms, memory_kb,
                           test_cases_passed, test_cases_total, stdout, stderr
        """
        if self.mock:
            return self._mock_execute(code, language, test_cases)
        return self._real_execute(code, language, test_cases)

    def _real_execute(self, code, language, test_cases):
        """Execute via real Judge0 API."""
        language_id = LANGUAGE_IDS.get(language, 71)
        results = []
        total_runtime = 0
        total_memory = 0
        passed = 0

        for tc in test_cases:
            payload = {
                'source_code': code,
                'language_id': language_id,
                'stdin': tc.input_data,
                'expected_output': tc.expected_output,
                'cpu_time_limit': 5,
                'memory_limit': 128000,
            }

            try:
                # Submit
                response = requests.post(
                    f"{self.api_url}/submissions?base64_encoded=false&wait=true",
                    json=payload,
                    headers=self.headers,
                    timeout=30
                )
                result = response.json()

                status_id = result.get('status', {}).get('id', 0)
                actual_output = (result.get('stdout') or '').strip()
                expected = tc.expected_output.strip()
                runtime = float(result.get('time') or 0) * 1000
                memory = float(result.get('memory') or 0)

                total_runtime += runtime
                total_memory = max(total_memory, memory)

                tc_result = {
                    'input': tc.input_data,
                    'expected': expected,
                    'actual': actual_output,
                    'passed': status_id == 3 or actual_output == expected,
                    'runtime_ms': round(runtime, 2),
                    'stderr': result.get('stderr') or '',
                    'compile_output': result.get('compile_output') or '',
                    'is_sample': tc.is_sample,
                }

                if tc_result['passed']:
                    passed += 1

                results.append(tc_result)

            except Exception as e:
                results.append({
                    'input': tc.input_data,
                    'expected': tc.expected_output,
                    'actual': '',
                    'passed': False,
                    'runtime_ms': 0,
                    'stderr': str(e),
                    'compile_output': '',
                    'is_sample': tc.is_sample,
                })

        all_passed = passed == len(test_cases)
        status = 'accepted' if all_passed else 'wrong_answer'

        # Check for specific error types
        for r in results:
            if r.get('compile_output'):
                status = 'compilation_error'
                break
            if r.get('stderr') and 'runtime' in r['stderr'].lower():
                status = 'runtime_error'
                break

        return {
            'status': status,
            'results': results,
            'runtime_ms': round(total_runtime / max(len(test_cases), 1), 2),
            'memory_kb': round(total_memory, 2),
            'test_cases_passed': passed,
            'test_cases_total': len(test_cases),
            'stdout': results[0].get('actual', '') if results else '',
            'stderr': results[0].get('stderr', '') if results else '',
        }

    def _mock_execute(self, code, language, test_cases):
        """Mock execution for development without Judge0 API."""
        results = []
        passed = 0

        for tc in test_cases:
            # Simple mock: check if code is non-empty and simulate execution
            # In mock mode, we'll do a basic Python eval for simple cases
            actual_output = ''
            tc_passed = False
            stderr = ''

            if language == 'python' and code.strip():
                try:
                    # Try to actually run the Python code locally
                    import subprocess
                    import tempfile
                    import os

                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py',
                                                      delete=False) as f:
                        f.write(code)
                        f.flush()
                        temp_path = f.name

                    try:
                        proc = subprocess.run(
                            ['python', temp_path],
                            input=tc.input_data,
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        actual_output = proc.stdout.strip()
                        stderr = proc.stderr.strip()
                        tc_passed = actual_output == tc.expected_output.strip()
                    finally:
                        os.unlink(temp_path)

                except subprocess.TimeoutExpired:
                    stderr = 'Time Limit Exceeded'
                except Exception as e:
                    stderr = str(e)
            else:
                # For non-Python or empty code, simulate
                tc_passed = bool(code.strip()) and random.random() > 0.3
                actual_output = tc.expected_output.strip() if tc_passed else 'mock_output'

            if tc_passed:
                passed += 1

            results.append({
                'input': tc.input_data,
                'expected': tc.expected_output.strip(),
                'actual': actual_output,
                'passed': tc_passed,
                'runtime_ms': round(random.uniform(10, 200), 2),
                'stderr': stderr,
                'compile_output': '',
                'is_sample': tc.is_sample,
            })

        all_passed = passed == len(test_cases)

        # Determine status
        status = 'accepted' if all_passed else 'wrong_answer'
        if any(r['stderr'] and 'Time Limit' in r['stderr'] for r in results):
            status = 'time_limit'
        elif any(r['stderr'] and r['stderr'] and 'Error' in r['stderr'] for r in results):
            status = 'runtime_error'

        return {
            'status': status,
            'results': results,
            'runtime_ms': round(sum(r['runtime_ms'] for r in results) / max(len(results), 1), 2),
            'memory_kb': round(random.uniform(5000, 30000), 2),
            'test_cases_passed': passed,
            'test_cases_total': len(test_cases),
            'stdout': results[0].get('actual', '') if results else '',
            'stderr': results[0].get('stderr', '') if results else '',
        }
