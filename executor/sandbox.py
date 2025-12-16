"""Secure sandbox for code execution with resource limits."""

import subprocess
import tempfile
import os
import signal
import psutil
from pathlib import Path
from django.conf import settings
from .languages import get_language, is_compiled_language

class ExecutionResult:
    """Container for execution results."""
    def __init__(self):
        self.stdout = ""
        self.stderr = ""
        self.returncode = None
        self.timeout = False
        self.memory_exceeded = False
        self.error = None
        self.execution_time = 0

class Sandbox:
    """Secure execution sandbox with resource limits."""
    
    def __init__(self, timeout=None, max_memory_mb=None):
        self.timeout = timeout or settings.EXECUTION_TIMEOUT
        self.max_memory_mb = max_memory_mb or settings.MAX_MEMORY_MB
        self.max_output_size = settings.MAX_OUTPUT_SIZE
        self.temp_dir = settings.TEMP_DIR
        
    def execute(self, code, language, stdin=None):
        """Execute code in sandbox with resource limits."""
        result = ExecutionResult()
        
        try:
            lang_config = get_language(language)
            if not lang_config:
                result.error = f"Unsupported language: {language}"
                return result
            
            # For Java, extract class name from code
            if language == 'java':
                temp_file = self._create_java_file(code)
            else:
                # Create temporary file for other languages
                with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix=lang_config['extension'],
                    dir=self.temp_dir,
                    delete=False
                ) as f:
                    f.write(code)
                    temp_file = f.name
            
            try:
                # Compile if needed
                if is_compiled_language(language):
                    compile_cmd = lang_config['compile_command'](temp_file)
                    compile_result = self._run_process(compile_cmd, None)
                    if compile_result.returncode != 0:
                        result.stderr = compile_result.stderr
                        result.returncode = compile_result.returncode
                        return result
                
                # Run the code
                run_cmd = lang_config['run_command'](temp_file)
                result = self._run_process(run_cmd, stdin)
                
            finally:
                # Cleanup
                self._cleanup_temp_files(temp_file, language)
                
        except Exception as e:
            result.error = str(e)
            
        return result
    
    def _create_java_file(self, code):
        """Create Java file with proper class name matching."""
        import re
        
        # Extract public class name from code
        class_match = re.search(r'public\s+class\s+(\w+)', code)
        
        if class_match:
            class_name = class_match.group(1)
        else:
            # If no public class found, use a default name
            class_name = 'Main'
            # Wrap code in a Main class if it doesn't have one
            if 'class' not in code:
                code = f"public class Main {{\n    public static void main(String[] args) {{\n        {code}\n    }}\n}}"
        
        # Create file with matching class name
        temp_file = os.path.join(self.temp_dir, f"{class_name}.java")
        with open(temp_file, 'w') as f:
            f.write(code)
        
        return temp_file
    
    def _run_process(self, command, stdin):
        """Run process with resource limits."""
        result = ExecutionResult()
        process = None
        
        try:
            # Ensure temp_dir exists
            os.makedirs(self.temp_dir, exist_ok=True)
            
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE if stdin else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.temp_dir),
            )
            
            try:
                stdout, stderr = process.communicate(
                    input=stdin,
                    timeout=self.timeout
                )
                result.stdout = stdout[:self.max_output_size]
                result.stderr = stderr[:self.max_output_size]
                result.returncode = process.returncode
                
            except subprocess.TimeoutExpired:
                process.kill()
                result.timeout = True
                result.stderr = f"Execution timeout after {self.timeout} seconds"
                
        except Exception as e:
            result.error = str(e)
            
        finally:
            if process and process.poll() is None:
                try:
                    process.kill()
                except:
                    pass
                    
        return result
    
    def _cleanup_temp_files(self, temp_file, language):
        """Clean up temporary files."""
        try:
            # Remove source file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Remove compiled files for compiled languages
            if is_compiled_language(language):
                lang_config = get_language(language)
                basename = os.path.basename(temp_file).replace(lang_config['extension'], '')
                
                # For Java, remove .class file
                if language == 'java':
                    class_file = os.path.join(self.temp_dir, basename + '.class')
                    if os.path.exists(class_file):
                        os.remove(class_file)
        except:
            pass
