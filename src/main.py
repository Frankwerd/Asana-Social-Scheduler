import json
import datetime
from dateutil.parser import parse

# Import our custom modules
from . import config
from .asana_service import AsanaService
from .social_service import SocialService

def _get_custom_field_value(task, field_name):
    """A helper function to safely extract a custom field's value from a task."""
    for field in task.get('custom_fields', []):
        if field and field.get('name') == field_name:
            # This handles different field types (text, date, dropdown)
            return field.get('display_value') or field.get('text_value') or field.get('date_value')
    return None

def lambda_handler(event, context):
    """
    Main handler for the AWS Lambda function.
    This function is called by the scheduled AWS trigger.
    """
    print("Script started at:", datetime.datetime.now(datetime.UTC))

    asana = AsanaService()
    social = SocialService()
    tasks_to_post_now = []

    try:
        # Step 1: Fetch a broad list of approved tasks from Asana
        approved_tasks = asana.get_approved_tasks()

        # Step 2: Filter tasks for the precise time
        current_time_utc = datetime.datetime.now(datetime.UTC).replace(tzinfo=None) # Make timezone-naive

        for task in approved_tasks:
            date_str = _get_custom_field_value(task, 'Scheduled Date')
            time_str = _get_custom_field_value(task, 'Scheduled Time (UTC)')

            if date_str and time_str:
                try:
                    # Combine date and time and parse into a datetime object
                    scheduled_datetime = parse(f"{date_str} {time_str}").replace(tzinfo=None)

                    # If the scheduled time is now or in the past, add to our list
                    if scheduled_datetime <= current_time_utc:
                        tasks_to_post_now.append(task)
                except Exception as e:
                    print(f"Skipping task {task['gid']} due to invalid date/time: {e}")

    except Exception as e:
        # If fetching tasks fails, log the error and exit
        print(f"FATAL: Could not fetch tasks from Asana. Error: {e}")
        return {"statusCode": 500, "body": "Failed to fetch tasks from Asana."}

    print(f"Found {len(tasks_to_post_now)} tasks ready to be posted.")

    # Step 3: Loop through the final list and process each task
    for task in tasks_to_post_now:
        task_gid = task['gid']
        print(f"--- Processing task: {task_gid} ---")

        try:
            # Lock the task in Asana to prevent duplicate posts
            asana.set_task_status(task_gid, config.ASANA_POSTING_GID)

            # Extract content for posting
            post_text = task.get('notes', '') # Use the task's description as the post text
            image_url = _get_custom_field_value(task, 'Image URL')
            platform = _get_custom_field_value(task, 'Social Platform')

            if not platform:
                raise ValueError("'Social Platform' custom field is not set.")

            # Post to the social media platform
            social.post_to_platform(platform, post_text, image_url)

            # If successful, finalize the task in Asana
            asana.set_task_status(task_gid, config.ASANA_POSTED_GID)
            asana.mark_task_complete(task_gid)
            print(f"SUCCESS: Task {task_gid} has been posted and completed.")

        except Exception as e:
            # If any step fails, report the error back to the Asana task
            print(f"ERROR: Failed to process task {task_gid}. Reason: {e}")
            try:
                asana.set_task_status(task_gid, config.ASANA_POSTING_FAILED_GID)
                asana.add_error_comment(task_gid, str(e))
            except Exception as comment_e:
                print(f"FATAL: Could not update Asana task {task_gid} with error state. Error: {comment_e}")

    print("Script finished successfully.")
    return {
        "statusCode": 200,
        "body": json.dumps(f"Processed {len(tasks_to_post_now)} tasks.")
    }

# This block allows local testing of the script
if __name__ == '__main__':
    lambda_handler(None, None)
