# Asana Social Media Scheduler

This is an automated, serverless application that schedules and posts social media content from a designated Asana project. The script is designed to be deployed on AWS Lambda and triggered on a recurring schedule.

### Key Features
- **Scheduled Posting:** Uses custom date and time fields in Asana for precise scheduling.
- **Modular Architecture:** Logic is cleanly separated into services for Asana and social media platforms.
- **Robust Error Handling:** Failures during the posting process are caught and reported back as a comment on the original Asana task.
- **Serverless & Cost-Effective:** Built to run on the AWS Lambda free tier, making it virtually free for most use cases.
- **Deployable via AWS SAM:** Uses the AWS Serverless Application Model for easy, repeatable deployments.

***

## 📝 Part 1: Asana Project Configuration

Before running the code, your Asana project must be configured with the following structure.

### 1. Project Sections (Columns)
Your project must have at least these two sections:
- `DOING...`
- `DONE!`

### 2. Custom Fields
Go to your project's **Customize** menu to add the following five custom fields.

| Field Name             | Field Type  | Configuration / Description                                                                   |
| ---------------------- | ----------- | --------------------------------------------------------------------------------------------- |
| **Approval Status**    | Drop-down   | The core status field. **Options must be created with these exact names:**<br>- `Ready to Review`<br>- `Permission Granted`<br>- `Posting...`<br>- `Posting Failed`<br>- `Posted` |
| **Social Platform**    | Drop-down   | Tells the script where to post. **Options:**<br>- `LinkedIn` <br>- *(Add others like `Twitter` as needed)* |
| **Image URL**          | Text        | A field to paste the direct, public URL of the image/video for the post.                        |
| **Scheduled Date**     | Date        | The calendar date the post should go live.                                                     |
| **Scheduled Time (UTC)**| Text        | The time the post should go live. **Crucial:** Must be entered in **24-hour UTC format (HH:MM)**, e.g., `16:30`. |

### 3. Asana Automation Rule
You must create one native Asana rule for the project:
- **Trigger:** When `Approval Status` is changed to `Posted`.
- **Action:** Move task to the `DONE!` section.

***

## 💻 Part 2: Local Setup and Testing

These steps are for running the project on your local machine for development and testing.

### 1. Prerequisites
- [Git](https://git-scm.com/downloads) installed.
- [Python 3.9+](https://www.python.org/downloads/) installed.
- Your Asana project must be configured as described in Part 1.

### 2. Initial Setup
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YourUsername/asana-social-scheduler.git
    cd asana-social-scheduler
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # Create the environment
    python -m venv venv
    
    # Activate it (macOS/Linux)
    source venv/bin/activate
    
    # Activate it (Windows)
    # venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration (.env file)
Create a file named `.env` in the root of the project. This file is for local development only and **must not be committed to GitHub** (it is ignored by `.gitignore`).

**Fill this template with your actual keys and GIDs:**
```
# --- Asana Credentials ---
# How to get: Asana > My Settings > Apps > Manage Developer Apps
ASANA_PAT="1/1234567890abcdef..."

# --- Asana GIDs ---
# How to get: Open the object in Asana and copy the number from the URL
ASANA_PROJECT_GID="120..."

# --- Custom Field GIDs (from Customize > Edit field) ---
ASANA_STATUS_FIELD_GID="120..."
ASANA_PLATFORM_FIELD_GID="120..."
ASANA_IMAGE_URL_FIELD_GID="120..."
ASANA_DATE_FIELD_GID="120..."
ASANA_TIME_FIELD_GID="120..."

# --- Status Option GIDs (from Customize > Edit field > Click on the option) ---
ASANA_PERMISSION_GRANTED_GID="120..."
ASANA_POSTING_GID="120..."
ASANA_POSTED_GID="120..."
ASANA_POSTING_FAILED_GID="120..."

# --- Social Media API Keys ---
# How to get: From your app on the social media platform's developer portal
LINKEDIN_ACCESS_TOKEN="your_linkedin_token_here"
```

### 4. Run the Local Test
Execute the main script. The `.env` file will be loaded automatically.```bash
python src/main.py
```
A successful test run will connect to your Asana project and print `"Found 0 tasks."`.

***

## 🚀 Part 3: AWS Deployment

These steps deploy the application to AWS Lambda where it will run automatically.

### 1. Prerequisites
- An AWS Account.
- The **[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)** is installed.
- The **[AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)** is installed.
- Your local machine is configured with your AWS credentials via `aws configure`.

### 2. Deployment Steps
1.  **Build the SAM Package:** This command bundles your Python code and dependencies.
    ```bash
    sam build
    ```
2.  **Deploy the Application:** The `--guided` flag will prompt you for configuration the first time.
    ```bash
    sam deploy --guided
    ```
    - **Stack Name:** `asana-social-scheduler`
    - **AWS Region:** `us-east-1` (or your preferred region)
    - **Confirm changes before deploy:** `y`
    - **Allow SAM CLI IAM role creation:** `y`
    - **Save arguments to configuration file:** `y` (This makes future deploys faster)

### 3. Configure Environment Variables in AWS
Your code is now in the cloud, but it needs its keys.
1.  Navigate to the **AWS Lambda Console**.
2.  Find and click on your new function (`asana-social-scheduler-...`).
3.  Go to **Configuration > Environment variables**.
4.  Manually re-create **every single variable** from your local `.env` file here and **Save**. This is the secure way to give your live function its credentials.

Your application is now live and will run every 5 minutes.
