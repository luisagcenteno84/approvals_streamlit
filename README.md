# IT Request Approval System

A Streamlit-based web application for managing IT request approvals with a three-team approval workflow (Data, Security, and Legal teams).

## Features

- **Request Submission**: Simple form interface for submitting IT requests
- **Multi-Team Approval**: Three independent approval teams (Data, Security, Legal)
- **Real-time Dashboard**: Live status tracking and metrics
- **Persistent Storage**: PostgreSQL database for data persistence
- **Cloud-Ready**: Docker container optimized for Google Cloud Run

## Architecture

- **Frontend**: Streamlit web framework
- **Backend**: Python with SQLAlchemy ORM
- **Database**: SQLite
- **Deployment**: Docker containerized for cloud deployment

## Local Development

### Prerequisites

- Python 3.11+
- uv package manager (or pip)

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the application:
   ```bash
   streamlit run app.py --server.port 5000
   ```

The SQLite database will be automatically created in the `data/` directory when you first run the application.

## Google Cloud Run Deployment

### Prerequisites

- Google Cloud Project with billing enabled
- Docker installed locally
- Google Cloud SDK (gcloud) installed and authenticated

### Quick Deployment

1. Make the deployment script executable:
   ```bash
   chmod +x deploy.sh
   ```

2. Run the deployment script:
   ```bash
   ./deploy.sh YOUR_PROJECT_ID us-central1
   ```

### Manual Deployment

1. Build the Docker image:
   ```bash
   docker build -t gcr.io/YOUR_PROJECT_ID/approval-workflow .
   ```

2. Push to Google Container Registry:
   ```bash
   docker push gcr.io/YOUR_PROJECT_ID/approval-workflow
   ```

3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy approval-workflow \
     --image gcr.io/YOUR_PROJECT_ID/approval-workflow \
     --region us-central1 \
     --platform managed \
     --port 5000 \
     --allow-unauthenticated \
     --set-env-vars PORT=5000
   ```

## Environment Variables

- `PORT`: Application port (default: 5000)

## Data Persistence

The app uses SQLite database which is stored in the container. For production deployments where data persistence across container restarts is needed, consider:

- Mounting persistent volumes in Cloud Run
- Using Cloud Storage for database backups
- Migrating to Cloud SQL if needed for high availability

## Usage

1. **Submit Request**: Use the "Submit Request" tab to create new IT requests
2. **View Dashboard**: Monitor all submissions and their approval status
3. **Approve Requests**: Team members can approve/reject requests in the "Approve Requests" tab

## Data Model

The application uses a single `submissions` table with the following fields:

- `id`: Unique identifier
- `name`: Request name
- `description`: Detailed description
- `purpose`: Request category
- `timestamp`: Submission time
- `data_approval`: Data team approval status
- `security_approval`: Security team approval status
- `legal_approval`: Legal team approval status
- `overall_status`: Calculated overall status

## Contributing

1. Follow the existing code structure
2. Update documentation for any architectural changes
3. Test thoroughly before deployment

## License

This project is for internal use and demonstration purposes.