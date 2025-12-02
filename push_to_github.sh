#!/bin/bash

# Script to push coding portfolio to GitHub
# Usage: ./push_to_github.sh <your-github-username> <repository-name>

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./push_to_github.sh <your-github-username> <repository-name>"
    echo "Example: ./push_to_github.sh johndoe coding-portfolio"
    exit 1
fi

GITHUB_USER=$1
REPO_NAME=$2

# Add remote (if not already added)
git remote remove origin 2>/dev/null
git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "Done! Your portfolio is now on GitHub at:"
echo "https://github.com/${GITHUB_USER}/${REPO_NAME}"

