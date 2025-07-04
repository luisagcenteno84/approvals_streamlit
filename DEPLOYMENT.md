# Google Cloud Run Deployment Guide

This guide will help you deploy your approval workflow app to Google Cloud Run.

## Prerequisites

1. **Google Cloud Project**: Create a project with billing enabled
2. **Google Cloud SDK**: Install and authenticate gcloud CLI
3. **Docker**: Install Docker on your local machine
4. **Container Registry API**: Enable in your Google Cloud project

## Quick Setup Commands

### 1. Enable Required APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Set Your Project ID
```bash
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID
```

### 3. Build and Deploy
```bash
# Make the script executable
chmod +x deploy.sh

# Run deployment (replace with your project ID)
./deploy.sh your-project-id us-central1
```

## Manual Deployment Steps

### 1. Build the Docker Image
```bash
docker build -t gcr.io/$PROJECT_ID/approval-workflow .
```

### 2. Push to Container Registry
```bash
docker push gcr.io/$PROJECT_ID/approval-workflow
```

### 3. Deploy to Cloud Run
```bash
gcloud run deploy approval-workflow \
  --image gcr.io/$PROJECT_ID/approval-workflow \
  --region us-central1 \
  --platform managed \
  --port 5000 \
  --allow-unauthenticated \
  --set-env-vars PORT=5000
```

## Database Configuration

The application uses SQLite database which is automatically created and managed within the container. No external database setup is required.

### Data Persistence

**Important**: SQLite data in Cloud Run containers is ephemeral by default. Data will be lost when:
- The container is restarted
- A new deployment is made
- The service scales down to zero

### For Production Data Persistence (Optional)

If you need persistent data across deployments, consider:

1. **Cloud Storage Backup** (Recommended for simple use cases):
```bash
# Add backup functionality to your app or use scheduled Cloud Functions
# to backup the SQLite file to Cloud Storage
```

2. **Persistent Volumes** (Limited support in Cloud Run):
```bash
# Cloud Run has limited support for persistent volumes
# Consider using Cloud SQL for production workloads requiring persistence
```

3. **Migrate to Cloud SQL** (For high availability):
```bash
# If you need full database persistence, consider migrating to Cloud SQL
# Update DATABASE_URL environment variable accordingly
```

## Environment Configuration

### Required Environment Variables

- `PORT`: Application port (automatically set by Cloud Run)
- `DATABASE_URL`: PostgreSQL connection string

### Optional Environment Variables

- `PYTHONUNBUFFERED`: Set to 1 for better logging
- `STREAMLIT_SERVER_HEADLESS`: Set to true for headless mode

## Security Considerations

### 1. Enable Authentication (Optional)
```bash
gcloud run services update approval-workflow \
  --no-allow-unauthenticated \
  --region us-central1
```

### 2. Set up IAM Roles
```bash
# Allow specific users to access the service
gcloud run services add-iam-policy-binding approval-workflow \
  --member="user:user@example.com" \
  --role="roles/run.invoker" \
  --region us-central1
```

## Monitoring and Logging

### View Logs
```bash
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=approval-workflow" --limit 50
```

### Monitor Performance
```bash
gcloud run services describe approval-workflow --region us-central1
```

## Scaling Configuration

### Set Concurrency and CPU
```bash
gcloud run services update approval-workflow \
  --concurrency 100 \
  --cpu 1 \
  --memory 512Mi \
  --region us-central1
```

### Set Min/Max Instances
```bash
gcloud run services update approval-workflow \
  --min-instances 0 \
  --max-instances 10 \
  --region us-central1
```

## Custom Domain (Optional)

### 1. Map Domain
```bash
gcloud run domain-mappings create \
  --service approval-workflow \
  --domain your-domain.com \
  --region us-central1
```

### 2. Verify Domain
Follow the verification instructions provided by the command above.

## Troubleshooting

### Common Issues

1. **Build Fails**: Check Dockerfile syntax and dependencies
2. **Database Connection**: Verify DATABASE_URL format and network access
3. **Port Issues**: Ensure PORT environment variable is properly configured
4. **Memory Issues**: Increase memory allocation if needed

### Debug Deployment
```bash
# View service details
gcloud run services describe approval-workflow --region us-central1

# Check recent deployments
gcloud run revisions list --service approval-workflow --region us-central1

# View logs
gcloud logs tail "resource.type=cloud_run_revision AND resource.labels.service_name=approval-workflow"
```

## Cost Optimization

- Use `--min-instances 0` to scale to zero when not in use
- Choose appropriate CPU and memory allocations
- Consider using Cloud SQL with automatic scaling

## Cleanup

To delete all resources:

```bash
# Delete Cloud Run service
gcloud run services delete approval-workflow --region us-central1

# Delete Cloud SQL instance (if created)
gcloud sql instances delete approval-db

# Delete container images
gcloud container images delete gcr.io/$PROJECT_ID/approval-workflow
```

Your approval workflow app is now ready for production deployment on Google Cloud Run!