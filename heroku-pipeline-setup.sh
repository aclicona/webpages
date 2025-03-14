#!/bin/bash
# Heroku Pipeline Setup Script for Monorepo Projects
# This script sets up a complete Heroku pipeline for a monorepo with separate backend and frontend deployments

# ============= CONFIGURATION =============
# Edit these variables to match your project
REPO_NAME="your-username/your-repo-name"
PROJECT_NAME="my-project"
BACKEND_PATH="backend"
FRONTEND_PATH="frontend"

# Environment files
BACKEND_ENV_FILE="prod.env"
FRONTEND_ENV_FILE="prod.env"

# Backend specifics
BACKEND_APP="${PROJECT_NAME}-backend"
BACKEND_BUILDPACK="heroku/python"  # Change if you're using something other than Python
# These are fallback variables if env file is not found
BACKEND_ENV_VARS=(
  "SECRET_KEY=change_this_to_a_strong_secret"
  "DEBUG=False"
  "ALLOWED_HOSTS=${BACKEND_APP}.herokuapp.com"
)

# Frontend specifics
FRONTEND_APP="${PROJECT_NAME}-frontend"
FRONTEND_BUILDPACK="heroku/nodejs"  # Change if you're using something other than Node.js
# These are fallback variables if env file is not found
FRONTEND_ENV_VARS=(
  "API_URL=https://${BACKEND_APP}.herokuapp.com"
  "NODE_ENV=production"
)
# =========================================

# Print header
echo "=========================================================="
echo "  Heroku Pipeline Setup for Monorepo Projects"
echo "  Project: ${PROJECT_NAME}"
echo "  Repository: ${REPO_NAME}"
echo "=========================================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Error: Heroku CLI is not installed."
    echo "Please install it first: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged in to Heroku
echo "Checking Heroku authentication..."
heroku auth:whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error: You're not logged in to Heroku CLI."
    echo "Please run 'heroku login' first."
    exit 1
fi

# Create backend app if it doesn't exist
echo -e "\n[1/9] Creating backend app: ${BACKEND_APP}"
heroku apps:info -a "${BACKEND_APP}" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Creating new app: ${BACKEND_APP}"
    heroku create "${BACKEND_APP}"
else
    echo "App ${BACKEND_APP} already exists."
fi

# Create frontend app if it doesn't exist
echo -e "\n[2/9] Creating frontend app: ${FRONTEND_APP}"
heroku apps:info -a "${FRONTEND_APP}" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Creating new app: ${FRONTEND_APP}"
    heroku create "${FRONTEND_APP}"
else
    echo "App ${FRONTEND_APP} already exists."
fi

# Create pipeline if it doesn't exist
echo -e "\n[3/9] Creating pipeline: ${PROJECT_NAME}-pipeline"
heroku pipelines:info "${PROJECT_NAME}-pipeline" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Creating new pipeline: ${PROJECT_NAME}-pipeline"
    heroku pipelines:create "${PROJECT_NAME}-pipeline"
else
    echo "Pipeline ${PROJECT_NAME}-pipeline already exists."
fi

# Add apps to pipeline
echo -e "\n[4/9] Adding apps to pipeline"
echo "Adding ${BACKEND_APP} to pipeline as production"
heroku pipelines:add "${PROJECT_NAME}-pipeline" -a "${BACKEND_APP}" -s production || true
echo "Adding ${FRONTEND_APP} to pipeline as production"
heroku pipelines:add "${PROJECT_NAME}-pipeline" -a "${FRONTEND_APP}" -s production || true

# Configure buildpacks for backend
echo -e "\n[5/9] Configuring buildpacks for backend app"
echo "Clearing existing buildpacks for ${BACKEND_APP}"
heroku buildpacks:clear -a "${BACKEND_APP}" || true
echo "Adding subdir buildpack for ${BACKEND_APP}"
heroku buildpacks:add -a "${BACKEND_APP}" https://github.com/timanovsky/subdir-heroku-buildpack || true
echo "Setting PROJECT_PATH=${BACKEND_PATH} for ${BACKEND_APP}"
heroku config:set -a "${BACKEND_APP}" PROJECT_PATH="${BACKEND_PATH}" || true
echo "Adding ${BACKEND_BUILDPACK} buildpack for ${BACKEND_APP}"
heroku buildpacks:add -a "${BACKEND_APP}" "${BACKEND_BUILDPACK}" || true

# Configure environment variables for backend
echo -e "\n[6/9] Setting environment variables for backend app"
if [ -f "${BACKEND_ENV_FILE}" ]; then
    echo "Found environment file: ${BACKEND_ENV_FILE}"
    while IFS='=' read -r key value || [ -n "$key" ]; do
        # Skip empty lines and comments
        if [[ -z "$key" || "$key" == \#* ]]; then
            continue
        fi
        # Remove any leading/trailing whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        echo "Setting ${key} for ${BACKEND_APP}"
        heroku config:set -a "${BACKEND_APP}" "${key}=${value}" || true
    done < "${BACKEND_ENV_FILE}"
    echo "Environment variables from ${BACKEND_ENV_FILE} have been set"
else
    echo "Environment file ${BACKEND_ENV_FILE} not found, using default variables"
    for env_var in "${BACKEND_ENV_VARS[@]}"; do
        key=$(echo $env_var | cut -d= -f1)
        value=$(echo $env_var | cut -d= -f2-)
        echo "Setting ${key} for ${BACKEND_APP}"
        heroku config:set -a "${BACKEND_APP}" "${key}=${value}" || true
    done
fi

# Configure buildpacks for frontend
echo -e "\n[7/9] Configuring buildpacks for frontend app"
echo "Clearing existing buildpacks for ${FRONTEND_APP}"
heroku buildpacks:clear -a "${FRONTEND_APP}" || true
echo "Adding subdir buildpack for ${FRONTEND_APP}"
heroku buildpacks:add -a "${FRONTEND_APP}" https://github.com/timanovsky/subdir-heroku-buildpack || true
echo "Setting PROJECT_PATH=${FRONTEND_PATH} for ${FRONTEND_APP}"
heroku config:set -a "${FRONTEND_APP}" PROJECT_PATH="${FRONTEND_PATH}" || true
echo "Adding ${FRONTEND_BUILDPACK} buildpack for ${FRONTEND_APP}"
heroku buildpacks:add -a "${FRONTEND_APP}" "${FRONTEND_BUILDPACK}" || true

# Configure environment variables for frontend
echo -e "\n[8/9] Setting environment variables for frontend app"
if [ -f "${FRONTEND_ENV_FILE}" ]; then
    echo "Found environment file: ${FRONTEND_ENV_FILE}"
    while IFS='=' read -r key value || [ -n "$key" ]; do
        # Skip empty lines and comments
        if [[ -z "$key" || "$key" == \#* ]]; then
            continue
        fi
        # Remove any leading/trailing whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        echo "Setting ${key} for ${FRONTEND_APP}"
        heroku config:set -a "${FRONTEND_APP}" "${key}=${value}" || true
    done < "${FRONTEND_ENV_FILE}"
    echo "Environment variables from ${FRONTEND_ENV_FILE} have been set"
else
    echo "Environment file ${FRONTEND_ENV_FILE} not found, using default variables"
    for env_var in "${FRONTEND_ENV_VARS[@]}"; do
        key=$(echo $env_var | cut -d= -f1)
        value=$(echo $env_var | cut -d= -f2-)
        echo "Setting ${key} for ${FRONTEND_APP}"
        heroku config:set -a "${FRONTEND_APP}" "${key}=${value}" || true
    done
fi

# Connect pipeline to GitHub
echo -e "\n[9/9] Connecting pipeline to GitHub repository"
read -p "Do you want to connect the pipeline to GitHub now? (y/n): " connect_github
if [[ $connect_github == "y" || $connect_github == "Y" ]]; then
    heroku pipelines:connect "${PROJECT_NAME}-pipeline" --repo "${REPO_NAME}" || {
        echo "Couldn't connect to GitHub automatically."
        echo "Please connect manually through the Heroku Dashboard:"
        echo "https://dashboard.heroku.com/pipelines/${PROJECT_NAME}-pipeline"
    }
else
    echo "Skipping GitHub connection. You can do this later through the Heroku Dashboard."
    echo "https://dashboard.heroku.com/pipelines/${PROJECT_NAME}-pipeline"
fi

# Setup automatic deploys
echo -e "\nSetting up automatic deploys..."
read -p "Do you want to enable automatic deploys for both apps? (y/n): " enable_auto_deploy
if [[ $enable_auto_deploy == "y" || $enable_auto_deploy == "Y" ]]; then
    echo "Please enable automatic deploys manually through the Heroku Dashboard for each app:"
    echo "Backend: https://dashboard.heroku.com/apps/${BACKEND_APP}/deploy/github"
    echo "Frontend: https://dashboard.heroku.com/apps/${FRONTEND_APP}/deploy/github"
    echo "Note: Automatic deploys can only be enabled through the web interface."
fi

# Final instructions
echo -e "\n=========================================================="
echo "  Setup Complete!"
echo "=========================================================="
echo "Your Heroku pipeline is now configured for your monorepo project."
echo ""
echo "Next steps:"
echo "1. Make sure your backend has a Procfile in the ${BACKEND_PATH} directory"
echo "2. Make sure your frontend has the correct start script in package.json"
echo "3. Push your code to GitHub to trigger the first deployment"
echo ""
echo "Backend URL: https://${BACKEND_APP}.herokuapp.com"
echo "Frontend URL: https://${FRONTEND_APP}.herokuapp.com"
echo "Pipeline URL: https://dashboard.heroku.com/pipelines/${PROJECT_NAME}-pipeline"
echo "=========================================================="