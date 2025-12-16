"""Supported programming languages configuration."""

import os

def _get_basename_without_ext(file, ext):
    """Get basename without extension."""
    return os.path.basename(file).replace(ext, '')

LANGUAGES = {
    'python': {
        'name': 'Python 3',
        'extension': '.py',
        'command': 'python',
        'compile_command': None,
        'run_command': lambda file: ['python', os.path.basename(file)],
    },
    'java': {
        'name': 'Java',
        'extension': '.java',
        'command': 'javac',
        'compile_command': lambda file: ['javac', os.path.basename(file)],
        'run_command': lambda file: ['java', _get_basename_without_ext(file, '.java')],
    },
    'javascript': {
        'name': 'JavaScript',
        'extension': '.js',
        'command': 'node',
        'compile_command': None,
        'run_command': lambda file: ['node', os.path.basename(file)],
    },
}

def get_language(lang_code):
    """Get language configuration by code."""
    return LANGUAGES.get(lang_code.lower())

def is_compiled_language(lang_code):
    """Check if language requires compilation."""
    lang = get_language(lang_code)
    return lang and lang['compile_command'] is not None
