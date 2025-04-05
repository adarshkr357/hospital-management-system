# Hospital Management System Backend

A FastAPI-based backend system for hospital management with PostgreSQL database.

## Features

- 🏥 Complete hospital management system
- 🔐 JWT Authentication and Authorization
- 📊 PostgreSQL Database Integration
- 🔄 CORS Support
- ✅ Input Validation
- 📧 Email Notifications
- 📝 Logging System

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Project Structure

```
backend/
├── .env                       
├── requirements.txt           
└── app/
    ├── __init__.py
    ├── main.py                
    ├── config/
    │   ├── __init__.py
    │   ├── database.py        
    │   └── settings.py        
    ├── api/
    │   ├── __init__.py
    │   └── v1/
    │       ├── __init__.py
    │       ├── api.py
    │       └── endpoints/
    │           ├── __init__.py
    │           ├── auth.py
    │           ├── patient.py
    │           ├── staff.py
    │           ├── finance.py
    │           ├── department.py
    │           ├── appointment.py
    │           ├── admission.py
    │           └── notification.py
    ├── core/
    │   ├── __init__.py
    │   ├── security.py       
    │   └── errors.py         
    ├── utils/
    │   ├── __init__.py
    │   ├── db_utils.py       
    │   ├── email_utils.py    
    │   ├── date_utils.py     
    │   └── validators.py     
    └── sql/
        ├── __init__.py
        ├── tables/
        │   ├── __init__.py
        │   ├── users.py
        │   ├── patient.py
        │   ├── staff.py
        │   ├── finance.py
        │   └── notification.py
        └── queries/
            ├── __init__.py
            ├── auth_queries.py
            ├── patient_queries.py
            ├── staff_queries.py
            ├── finance_queries.py
            ├── department_queries.py
            ├── appointment_queries.py
            ├── admission_queries.py
            └── notification_queries.py
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/adarshkr357/hospital-management-system.git
cd hospital-management-system/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a PostgreSQL database:
```sql
CREATE DATABASE hospital_db;
```

6. Set up environment variables in `.env`:
```env
# Database
DB_USER='user'
DB_PASSWORD='pass'
DB_HOST='host'
DB_PORT='5432'
DB_NAME='hospital_db' # Do not edit this

# Security
SECRET_KEY=your-256-bit-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME="Hospital Management System"
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
```

## Running the Application

1. Using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Using the run script:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## Main Endpoints

- `GET /`: Welcome message and API status
- `GET /health`: Health check endpoint
- `POST /api/v1/auth/login`: User login
- `POST /api/v1/auth/register`: User registration
- `GET /api/v1/patients/`: List all patients
- `GET /api/v1/staff/`: List all staff members
- `GET /api/v1/appointments/`: List all appointments

## Security

- API is protected with JWT authentication
- Passwords are hashed using bcrypt
- CORS is configured for frontend access
- Input validation using Pydantic
- SQL injection prevention
- Rate limiting for API endpoints

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the [MIT License](../LICENSE) - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. Database Connection Errors
```bash
# Check if PostgreSQL is running
service postgresql status

# Verify database credentials in .env
# Ensure DATABASE_URL is correct
```

2. Port Already in Use
```bash
# Check what's using port 8000
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Kill the process
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

3. Dependencies Issues
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Create new virtual environment if needed
python -m venv venv_new
```

### Environment Setup Issues

1. Python Version Mismatch
```bash
# Check Python version
python --version

# Should be 3.8 or higher
```

2. PostgreSQL Connection
```bash
# Test PostgreSQL connection
psql -U username -d hospital_db

# Common fixes:
# - Check PostgreSQL service is running
# - Verify password in .env
# - Check database exists
```

## Deployment

### Server Requirements

- CPU: 2+ cores
- RAM: 4GB minimum
- Storage: 20GB minimum
- OS: Ubuntu 20.04 LTS (recommended)

### Monitoring

- Use logging for debugging
- Monitor API endpoints performance
- Track database queries
- Set up error notifications

## API Testing Guide

### Curl Examples

1. Health Check
```bash
curl http://localhost:8000/health
```

2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

3. Get Patients List
```bash
curl http://localhost:8000/api/v1/patients \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Performance Optimization

1. Database Optimization
- Index frequently queried columns
- Regular VACUUM operations
- Connection pooling

2. API Response Time
- Implement caching
- Optimize database queries
- Use async operations

3. Resource Management
- Implement pagination
- Limit request sizes
- Optimize file uploads

## Acknowledgments

- FastAPI documentation
- PostgreSQL community
- Python community
- Open-source contributors

### Technical Improvements

1. Infrastructure
- Containerization improvements
- Microservices architecture
- Cloud deployment options

2. Security
- Advanced authentication methods
- Enhanced encryption
- Regular security audits

3. Performance
- Query optimization
- Caching improvements
- Load balancing