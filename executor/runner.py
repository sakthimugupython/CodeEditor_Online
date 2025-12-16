"""High-level code execution runner."""

from .sandbox import Sandbox
from .languages import get_language

class CodeRunner:
    """Execute code with proper error handling."""
    
    @staticmethod
    def run(code, language, stdin=None, timeout=None, max_memory_mb=None):
        """
        Execute code and return results.
        
        Args:
            code: Source code to execute
            language: Programming language (python, cpp, c, java)
            stdin: Optional standard input
            timeout: Execution timeout in seconds
            max_memory_mb: Maximum memory in MB
            
        Returns:
            dict with stdout, stderr, returncode, timeout, error
        """
        if not get_language(language):
            return {
                'stdout': '',
                'stderr': f'Unsupported language: {language}',
                'returncode': 1,
                'timeout': False,
                'error': f'Language {language} not supported'
            }
        
        sandbox = Sandbox(timeout=timeout, max_memory_mb=max_memory_mb)
        result = sandbox.execute(code, language, stdin)
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'timeout': result.timeout,
            'memory_exceeded': result.memory_exceeded,
            'error': result.error,
            'execution_time': result.execution_time,
        }
