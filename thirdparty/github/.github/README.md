# Splunk Detection Rules Deployment

This repository enables non-technical users to deploy Splunk detection rules using a simple web-based form in GitHub Issues, with an approval process by designated team members. It eliminates the need for Git knowledge or manual file edits (e.g., `ready_for_prod.csv`) and uses GitHub’s authentication, including SSO if configured.

## Overview

- **Purpose**: Submit detection IDs (from `./detections/*.yaml`) via a GitHub Issues form to trigger deployment to Splunk, with approval from code owners.
- **Key Features**:
  - Non-technical users submit detection IDs through a browser-based form.
  - A pinned issue lists available detection IDs for reference.
  - Deployments require approval from designated code owners (e.g., security team).
  - No Git knowledge or repository write access needed for submitters.
  - No CSV or marker files stored in the repository.
- **Authentication**: Uses GitHub accounts, integrated with your organization’s SSO (e.g., Okta, Azure AD) if enabled.
- **Approval Process**: Code owners defined in `.github/CODEOWNERS` must approve deployments via a pull request.

## User Instructions

### For Non-Technical Users
1. **Access the Form**:
   - Visit the [Issues tab](https://github.com/your-org/your-repo/issues).
   - Log in with your GitHub account (or SSO credentials).
2. **Find Detection IDs**:
   - Open the pinned issue titled “Available Detection IDs” (issue #1).
   - Copy the detection IDs you want to deploy (e.g., `id1,id2`).
3. **Submit Deployment Request**:
   - Click “New Issue” and select “Deploy Detection Rules to Splunk.”
   - Enter comma-separated detection IDs (e.g., `id1,id2`) in the form.
   - Add optional comments and submit.
4. **Wait for Approval**:
   - A pull request is created and sent to code owners for approval.
   - Check the issue for a comment confirming deployment or noting invalid IDs.

**Note**: Contact the security team for assistance.

### For Approvers (Code Owners)
1. **Review Pull Request**:
   - Receive a GitHub notification for a new pull request.
   - Check the detection IDs in the pull request description.
2. **Approve or Reject**:
   - In the [Pull Requests tab](https://github.com/your-org/your-repo/pulls), approve the PR if the IDs are valid, or request changes if not.
3. **Deployment**:
   - Approved PRs trigger the deployment to Splunk, and the issue is updated with the status.

## Installation Steps (For Administrators)

1. **Set Up CODEOWNERS**:
   - Create `.github/CODEOWNERS` to specify approvers (e.g., `@org/security-team`) for the `detections/` folder and `.github/deployment.txt`.
   - Ensure code owners have “Write” permissions in the repository.

2. **Enable Branch Protection**:
   - In Settings > Branches, protect the main branch.
   - Enable “Require pull request reviews before merging” and “Require review from Code Owners.”

3. **Configure Detection ID Listing**:
   - Add a GitHub Action workflow to extract detection IDs from `./detections/*.yaml` and update a pinned issue (#1).
   - Create and pin issue #1 titled “Available Detection IDs.”

4. **Set Up Issue Form**:
   - Create a GitHub Issues form template for submitting detection IDs.
   - Ensure it applies a “deploy” label to trigger the deployment workflow.

5. **Configure Deployment Workflow**:
   - Add a GitHub Action workflow to:
     - Create a pull request for each issue submission.
     - Wait for code owner approval.
     - Process valid detection IDs and run `playbook.yml` to deploy to Splunk.
     - Update the issue with the deployment status.

6. **Grant Permissions**:
   - Give non-technical users “Read” or “Triage” permissions to create issues.
   - Restrict repository write access to developers and code owners.

7. **Share User Guide**:
   - Provide a link to the issue form (e.g., `https://github.com/your-org/your-repo/issues/new?template=deploy-detection.yml`).
   - Instruct users to check pinned issue #1 for valid detection IDs.

## Support
For issues or questions, contact the security team or repository administrators.