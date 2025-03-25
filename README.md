# User Management API

## Overview
A secure, tested Python REST API for user management built with FastAPI and MariaDB.

## Prerequisites
- Python 3.9+
- MariaDB Server
- pip

## Database Setup

### MariaDB Configuration
1. Install MariaDB Server
2. Create a database for the application:
```sql
CREATE DATABASE user_management;
CREATE USER 'youruser'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON user_management.* TO 'youruser'@'localhost';
FLUSH PRIVILEGES;
```

### Environment Variables
Configure database connection using environment variables:
- `DB_USERNAME`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 3306)
- `DB_NAME`: Database name (default: user_management)

Example:
```bash
export DB_USERNAME=youruser
export DB_PASSWORD=yourpassword
export DB_HOST=localhost
export DB_NAME=user_management
```

## Local Development Setup
1. Clone the repository
2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

4. Install Python dependencies
```bash
pip install -r requirements.txt
```

## Docker Deployment
```bash
docker build -t user-management-api .
docker run -e DB_USERNAME=youruser \
           -e DB_PASSWORD=yourpassword \
           -e DB_HOST=your_mariadb_host \
           -p 8000:8000 user-management-api
```

## Additional Notes for MariaDB
- Ensure MariaDB server is running before starting the application
- The application uses connection pooling for improved performance
- Connections are recycled every 30 minutes to prevent stale connections