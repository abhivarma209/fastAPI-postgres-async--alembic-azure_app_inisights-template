# FastAPI + PostgreSQL + Alembic + Azure App Insights Template

A production-ready FastAPI template with async PostgreSQL, database migrations, and Azure Application Insights monitoring. This template provides a solid foundation for building scalable REST APIs with modern Python technologies.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs with Python
- **Async PostgreSQL** - Asynchronous database operations using `asyncpg` and SQLAlchemy 2.0
- **Database Migrations** - Alembic for database schema versioning and migrations
- **Azure Application Insights** - Comprehensive monitoring and telemetry with OpenTelemetry
- **Pydantic Settings** - Environment-based configuration management
- **Health Checks** - Built-in health check endpoints
- **Development Tools** - Pre-configured development dependencies

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL database
- Azure Application Insights resource (optional, for monitoring)

## 🛠️ Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd My-Inventory
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Database Configuration
POSTGRES_DB=your_database_name
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

# Azure Application Insights (Optional)
APPLICATIONINSIGHTS_CONNECTION_STRING=your_connection_string

# OpenTelemetry (Optional)
OTEL_EXPERIMENTAL_RESOURCE_DETECTORS=azure_app_service
```

### 3. Database Setup

```bash
# Run database migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development
python main.py

# Or with uvicorn
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
My-Inventory/
├── alembic/                    # Database migration files
│   ├── versions/              # Migration scripts
│   └── env.py                 # Alembic configuration
├── dependencies/              # FastAPI dependencies
│   └── database.py           # Database connection management
├── models/                    # Pydantic/SQLAlchemy models
│   ├── restaurant.py
│   └── menu_item.py
├── routes/                    # API route handlers
│   ├── restaurant_route.py
│   └── menu_item_route.py
├── config.py                  # Application configuration
├── db_models.py              # Database model definitions
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── alembic.ini              # Alembic configuration
```

## 🔧 Configuration

The application uses Pydantic Settings for configuration management. All settings can be configured via environment variables or the `.env` file.

### Key Configuration Options

- `APP_NAME`: Application name (default: "Inventory Analyzer Service")
- `APP_VERSION`: Application version (default: "1.0.0")
- `POSTGRES_*`: Database connection parameters
- `APPLICATIONINSIGHTS_CONNECTION_STRING`: Azure monitoring (optional)

## 📊 Monitoring with Azure Application Insights

This template includes pre-configured Azure Application Insights integration using OpenTelemetry:

1. **Automatic Instrumentation**: FastAPI requests are automatically traced
2. **Custom Telemetry**: Add custom metrics and traces using the OpenTelemetry SDK
3. **Performance Monitoring**: Monitor response times, dependencies, and exceptions

To enable monitoring, set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable.

## 🗄️ Database Operations

### Creating Migrations

```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### Database Models

The template includes sample models for restaurants and menu items. Modify or replace these models based on your application needs:

- `models/restaurant.py` - Pydantic models for API serialization
- `models/menu_item.py` - Pydantic models for API serialization
- `db_models.py` - SQLAlchemy models for database operations

## 🛣️ API Routes

The template includes sample CRUD operations:

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- Restaurant endpoints (example implementation)
- Menu item endpoints (example implementation)

## 🧪 Development

### Installing Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Add your test framework and run tests
pytest
```

## 🚀 Deployment

### Environment Variables for Production

Ensure the following environment variables are set:

```env
POSTGRES_DB=production_db
POSTGRES_HOST=your-prod-host
POSTGRES_PORT=5432
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=secure_password
APPLICATIONINSIGHTS_CONNECTION_STRING=your_prod_connection_string
```

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Customization

To customize this template for your project:

1. **Update Models**: Modify or replace the sample models in `models/` and `db_models.py`
2. **Add Routes**: Create new route files in `routes/` and include them in `main.py`
3. **Configure Settings**: Update `config.py` with your application-specific settings
4. **Database Schema**: Create new Alembic migrations for your database schema
5. **Dependencies**: Add any additional dependencies to `requirements.txt`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This template is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For questions or issues:
1. Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
2. Review [SQLAlchemy async documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
3. Consult [Azure Application Insights documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)

---

**Happy coding!** 🎉 