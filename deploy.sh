#!/bin/bash

# Google Cloud Run deployment script for Approval Workflow App
# Make sure you have gcloud CLI installed and authenticated

set -e

# Configuration variables
PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
SERVICE_NAME="approval-workflow"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Deploying Approval Workflow to Google Cloud Run..."
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

# Build and tag the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Push the image to Google Container Registry
echo "Pushing image to Container Registry..."
docker push $IMAGE_NAME

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --platform managed \
    --port 5000 \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --timeout 300 \
    --project $PROJECT_ID

echo "Deployment completed!"
echo "Your app will be available at the URL shown above."
echo ""
echo "The app uses SQLite database which is automatically created and managed within the container."
echo "Data will persist during the container's lifecycle. For permanent data persistence across deployments,"
echo "consider using Cloud Storage or Cloud SQL if needed."