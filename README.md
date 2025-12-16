# Online Code Editor with Secure Execution Environment

A comprehensive web-based code editor built with Django, featuring secure server-side code execution, user authentication, and execution history tracking. Designed for academic projects with focus on security, system design, and correctness.

## Features

### Core Features
- **User Authentication**: Register, login, logout with secure password handling
- **User Profiles**: Customizable user profiles with bio and avatar
- **Code Editor**: Web-based editor with syntax highlighting
- **Multi-Language Support**: Python, C, C++, Java (extensible)
- **Secure Execution**: Isolated code execution with resource limits
- **Execution History**: Track all code executions with results
- **Code Snippets**: Save and manage code snippets
- **Admin Dashboard**: Django Admin for user and execution management

### Security Features
- **Resource Limits**: CPU timeout, memory limits, output size limits
- **Isolated Execution**: Temporary file-based execution
- **Input Validation**: CSRF protection, SQL injection prevention
- **Authentication**: Session-based authentication with login required
- **Error Handling**: Graceful error handling without exposing system details

## Project Structure

```
code_editor/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
├── code_editor/             # Main Django project
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── editor/                  # Main editor app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URLs
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin configuration
│   └── templates/           # HTML templates
├── api/                     # REST API app
│   ├── views.py             # API views
│   ├── serializers.py       # DRF serializers
│   └── urls.py              # API URLs
├── accounts/                # User authentication app
│   ├── views.py             # Auth views
│   ├── forms.py             # Auth forms
│   ├── urls.py              # Auth URLs
│   └── templates/           # Auth templates
├── executor/                # Code execution engine
│   ├── runner.py            # High-level runner
│   ├── sandbox.py           # Secure sandbox
│   └── languages.py         # Language configurations
└── templates/               # Base templates
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git
- C/C++ compiler (gcc, g++) for compiled language support
- Java JDK (optional, for Java support)

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd code_editor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration

```bash
# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env with your settings
# Important: Change SECRET_KEY in production
```

### Step 3: Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### Step 4: Run Development Server

```bash
# Start the development server
python manage.py runserver

# Access the application
# Open browser: http://localhost:8000
# Admin panel: http://localhost:8000/admin
```

## Usage

### User Registration & Login
1. Navigate to `/accounts/register/` to create a new account
2. Fill in username, email, and password
3. Login at `/accounts/login/`

### Using the Code Editor
1. Go to `/editor/` after logging in
2. Select programming language from dropdown
3. Write code in the editor
4. Click "Execute" to run the code
5. View output in the output panel

### Managing Snippets
1. Click "New Snippet" to save code
2. Give it a title and description
3. Snippets appear in the sidebar for quick access
4. Click on a snippet to load it

### Viewing History
1. Go to `/editor/history/` to see all executions
2. Filter by language
3. Click "View" to see execution details

### User Profile
1. Go to `/editor/profile/` to view your profile
2. Edit bio and upload avatar
3. View statistics (total snippets and executions)

## API Endpoints

### Authentication
- `POST /accounts/login/` - User login
- `POST /accounts/register/` - User registration
- `GET /accounts/logout/` - User logout

### Code Snippets
- `GET /api/snippets/` - List user's snippets
- `POST /api/snippets/` - Create new snippet
- `GET /api/snippets/{id}/` - Get snippet details
- `PUT /api/snippets/{id}/` - Update snippet
- `DELETE /api/snippets/{id}/` - Delete snippet

### Code Execution
- `POST /api/execution/execute/` - Execute code
  ```json
  {
    "code": "print('Hello')",
    "language": "python",
    "stdin": "",
    "snippet_id": null
  }
  ```
- `GET /api/execution/history/` - Get execution history

## Configuration

### Environment Variables (.env)

```
DEBUG=True                          # Debug mode (False in production)
SECRET_KEY=your-secret-key         # Django secret key
ALLOWED_HOSTS=localhost,127.0.0.1  # Allowed hosts
DATABASE_URL=sqlite:///db.sqlite3  # Database URL
EXECUTION_TIMEOUT=10               # Code execution timeout (seconds)
MAX_MEMORY_MB=256                  # Maximum memory (MB)
MAX_OUTPUT_SIZE=10000              # Maximum output size (characters)
```

### Supported Languages

| Language | Extension | Compiled | Command |
|----------|-----------|----------|---------|
| Python   | .py       | No       | python  |
| C        | .c        | Yes      | gcc     |
| C++      | .cpp      | Yes      | g++     |
| Java     | .java     | Yes      | javac   |

### Adding New Languages

Edit `executor/languages.py`:

```python
LANGUAGES = {
    'rust': {
        'name': 'Rust',
        'extension': '.rs',
        'command': 'rustc',
        'compile_command': lambda file: ['rustc', '-o', file.replace('.rs', ''), file],
        'run_command': lambda file: [file.replace('.rs', '')],
    },
}
```

## Security Considerations

### Resource Limits
- **Execution Timeout**: Default 10 seconds (configurable)
- **Memory Limit**: Default 256 MB (configurable)
- **Output Size**: Default 10,000 characters (configurable)

### Isolation
- Code runs in temporary files
- Temporary files are cleaned up after execution
- No access to system files or other users' data

### Best Practices
1. Always use HTTPS in production
2. Change SECRET_KEY in production
3. Set DEBUG=False in production
4. Use strong database passwords
5. Regularly update dependencies
6. Monitor execution logs for abuse

## Admin Dashboard

Access Django Admin at `/admin/`:

### Manage Users
- View all registered users
- Edit user information
- Manage permissions
- View user statistics

### Monitor Executions
- View all code executions
- Filter by language, status, date
- See execution details (code, output, errors)
- Monitor resource usage

### Manage Snippets
- View all code snippets
- Filter by user, language, privacy
- Delete inappropriate content

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'django'"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: "python: command not found"
```bash
# Solution: Use python3 instead
python3 manage.py runserver
```

**Issue**: "Port 8000 already in use"
```bash
# Solution: Use different port
python manage.py runserver 8001
```

**Issue**: "No such file or directory: 'gcc'"
```bash
# Solution: Install C compiler
# Windows: Install MinGW or Visual Studio Build Tools
# macOS: xcode-select --install
# Linux: sudo apt-get install build-essential
```

**Issue**: Database locked error
```bash
# Solution: Delete db.sqlite3 and run migrations again
rm db.sqlite3
python manage.py migrate
```

## Performance Optimization

### For Production
1. Use PostgreSQL instead of SQLite
2. Enable caching with Redis
3. Use Gunicorn/uWSGI as application server
4. Use Nginx as reverse proxy
5. Enable GZIP compression
6. Minify static files

### Database Optimization
1. Add database indexes (already configured)
2. Use connection pooling
3. Archive old execution history
4. Optimize queries with select_related/prefetch_related

## Testing

### Run Tests
```bash
python manage.py test
```

### Test Code Execution
```python
from executor.runner import CodeRunner

result = CodeRunner.run(
    code='print("Hello")',
    language='python'
)
print(result)
```

## Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn code_editor.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "code_editor.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t code-editor .
docker run -p 8000:8000 code-editor
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is provided as-is for educational purposes.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Check executor module documentation
4. Contact the development team

## Future Enhancements

- [ ] Monaco Editor integration
- [ ] Real-time collaboration
- [ ] Code sharing with public links
- [ ] Docker-based execution
- [ ] More programming languages
- [ ] Code formatting and linting
- [ ] Debugging support
- [ ] Performance analytics
- [ ] Team workspaces
- [ ] API rate limiting

## Academic Project Notes

This project is designed for final-year academic projects with emphasis on:
- **Security**: Secure code execution with resource limits
- **System Design**: Modular architecture with clear separation of concerns
- **Correctness**: Comprehensive error handling and validation
- **Documentation**: Well-documented code and API
- **Scalability**: Extensible design for adding features

## Version History

- **v1.0.0** (2024): Initial release
  - User authentication
  - Code editor with syntax highlighting
  - Multi-language support (Python, C, C++, Java)
  - Secure execution environment
  - Execution history and snippets
  - Admin dashboard
