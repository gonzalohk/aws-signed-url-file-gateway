# S3 File Gateway - Serverless API (Lab 4)

This project implements a secure, serverless file gateway using **AWS SAM**. It allows users to upload and download files through **S3 Pre-signed URLs**, ensuring that the storage bucket remains private and inaccessible to the public internet.

---

## 1. Architecture & CI/CD Flow
The system follows a decoupled architecture where the API acts as the **Control Plane** and S3 acts as the **Data Plane**. 

**Automation:** This project is automatically deployed via **GitHub Actions** whenever a change is pushed to the `main` branch.



---

## 2. Prerequisites & Configuration

### **AWS Infrastructure**
* **Security (Least Privilege):** The Lambda functions use a dedicated IAM Role (`FileGatewayS3Role`) with restricted access (`s3:PutObject`, `s3:GetObject`, `s3:ListBucket`).
* **S3 Access:** Access is only granted via cryptographic signatures.

### **GitHub Secrets**
To run the deployment pipeline, the following secrets must be configured in your GitHub repository:
* `AWS_ACCOUNT_ID`: Your AWS IAM user key

---

## 3. Deployment Steps (CI/CD)

The deployment is fully automated. However, to trigger it manually or locally:

1. **Automated Deployment:**
   - Push your changes to the `main` branch.
   - Monitor the progress in the **Actions** tab of your GitHub repository.

```
sam deploy \
            --stack-name aws-final-project \
            --region us-east-1 \
            --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM\
            --resolve-s3 \
            --no-confirm-changeset \
            --no-fail-on-empty-changeset
```


## 4. How to Test (API Interaction)
Replace <API_ID> and <REGION> with your specific deployment values (found in the GitHub Actions logs or CloudFormation Outputs).

### A. Generate an Upload URL (POST)
```
curl -X POST https://<API_ID>.execute-api.<REGION>[.amazonaws.com/Prod/files] \
     -H "Content-Type: application/json" \
     -d '{"filename": "lab4-test.txt"}'
```
### B. Upload a File (PUT)
Use the uploadUrl from the previous response:

```
curl -X PUT --upload-file "lab4-test.txt" "PASTE_UPLOAD_URL_HERE"
```
### C. Download a File (GET with Redirect)
Use -L to follow the HTTP 307 Redirect:

```
curl -i -L https://<API_ID>.execute-api.<REGION>[.amazonaws.com/Prod/files/lab4-test.txt]
```