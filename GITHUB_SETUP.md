# GitHub Repository Setup Instructions

Your local git repository is ready! Follow these steps to create a GitHub repository and push your code.

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **+** icon in the top right corner
3. Select **New repository**
4. Fill in the details:
   - **Repository name**: `coding-portfolio` (or your preferred name)
   - **Description**: "Semester 3 Coding Portfolio - CSSci"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **Create repository**

## Step 2: Push Your Code

### Option A: Using the provided script (easiest)

```bash
cd /Users/uliwintersperger/Desktop/uni/cssci/semester-03/individual_assignments_s3/coding_portfolio
./push_to_github.sh YOUR_GITHUB_USERNAME YOUR_REPO_NAME
```

Replace:
- `YOUR_GITHUB_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with the repository name you created

### Option B: Manual commands

```bash
cd /Users/uliwintersperger/Desktop/uni/cssci/semester-03/individual_assignments_s3/coding_portfolio

# Add the remote (replace with your username and repo name)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 3: Verify

After pushing, visit your repository on GitHub to verify all files are there:
`https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`

## Troubleshooting

### Authentication Issues
If you get authentication errors, you may need to:
1. Use a Personal Access Token instead of password
2. Set up SSH keys
3. Use GitHub CLI: `gh auth login`

### Large Files
If you have issues with large CSV/data files, consider:
- Using Git LFS: `git lfs install` and `git lfs track "*.csv.gz"`
- Or add them to .gitignore if they're too large

## Next Steps

- Add more commits as you complete assignments
- Use `git add .`, `git commit -m "message"`, `git push` to update

