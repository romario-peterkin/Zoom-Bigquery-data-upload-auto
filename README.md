# Zoom-Bigquery-data-upload-auto
Use Google Cloud to automate Zoom data export to Bigquery


From Google Cloud editor terminal:

1. Set cloud project instance and the folder that you choose to deploy.


gcloud config set {ENTER_PROJECT_NAME}
cd {PATH_TO_FOLDER}

PROJECT_ID=$(gcloud config get-value project)
echo $PROJECT_ID

DOCKER_IMG="gcr.io/$PROJECT_ID/{PATH_TO_FOLDER}"
echo $DOCKER_IMG


2. Build container using the Docker file in the folder you chose to deploy.

gcloud builds submit --tag $DOCKER_IMG


3. Test to verify that the script is working in a local instance before deploying.


docker pull $DOCKER_IMG
docker run -p 8080:8080 $DOCKER_IMG

4. Set the region.

REGION="{REGION_NAME}"


5. Deploy to Cloud Run.


gcloud run deploy {CLOUD_RUN_DEPLOYMENT_INSTANCE_NAME} \
  --image $DOCKER_IMG \
  --platform managed \
  --region $REGION \
  --no-allow-unauthenticated


