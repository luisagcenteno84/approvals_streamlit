# Simple Google Cloud Run Deployment

This guide provides the minimal steps to deploy your approval workflow app to Google Cloud Run without any database provisioning.

## Prerequisites

- Google Cloud Project with billing enabled
- Docker installed locally
- Google Cloud SDK installed and authenticated

## Deployment Steps

### 1. Set Project ID
```bash
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID
```

### 2. Enable Cloud Run API
```bash
gcloud services enable run.googleapis.com
```

### 3. Build and Deploy (One Command)
```bash
gcloud run deploy approval-workflow \
  --source . \
  --region us-central1 \
  --platform managed \
  --port 5000 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300
```

That's it! Your app will be deployed with:
- ✅ SQLite database (no external database needed)
- ✅ Automatic HTTPS
- ✅ Auto-scaling from 0 to 10 instances
- ✅ 512Mi memory and 1 CPU allocated
- ✅ Public access (no authentication required)

## Access Your App

After deployment, Google Cloud Run will provide a URL like:
`https://approval-workflow-[hash]-uc.a.run.app`

## Important Notes

- **No database setup required** - SQLite runs inside the container
- **Data is ephemeral** - Data resets with each new deployment
- **Cost-effective** - Scales to zero when not in use
- **No external dependencies** - Everything runs in the container

## Updating Your App

To deploy updates, simply run the same deploy command again:
```bash
gcloud run deploy approval-workflow \
  --source . \
  --region us-central1 \
  --platform managed \
  --port 5000 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300
```

## Cleanup

To delete the service:
```bash
gcloud run services delete approval-workflow --region us-central1
```