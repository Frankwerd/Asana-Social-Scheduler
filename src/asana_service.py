import requests
import datetime

# Import our configuration variables
from . import config

class AsanaService:
    """A class to handle all interactions with the Asana API."""

    def __init__(self):
        """Initializes the Asana service with authentication headers."""
        self.headers = {
            "Authorization": f"Bearer {config.ASANA_PAT}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.base_url = "https://app.asana.com/api/1.0"

    def get_approved_tasks(self):
        """
        Searches Asana for tasks that are approved and scheduled for today or earlier.
        """
        search_url = f"{self.base_url}/tasks"

        # We only want the essential fields to keep the response fast and small.
        # This is an important optimization.
        desired_fields = [
            "name", "notes", "completed", "custom_fields"
        ]

        # The search query payload
        payload = {
            "data": {
                "projects.any": [config.ASANA_PROJECT_GID],
                f"custom_fields.{config.ASANA_STATUS_FIELD_GID}.value": config.ASANA_PERMISSION_GRANTED_GID,
                "completed": False,
                "due_on.before": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
                "opt_fields": ",".join(desired_fields)
            }
        }

        print("Searching for approved tasks in Asana...")
        response = requests.post(search_url, headers=self.headers, json=payload)

        # Raise an exception if the API call failed
        response.raise_for_status()

        tasks = response.json().get("data", [])
        print(f"Found {len(tasks)} tasks.")
        return tasks

    def _update_task(self, task_gid, payload):
        """A private helper function to handle generic task updates."""
        update_url = f"{self.base_url}/tasks/{task_gid}"
        response = requests.put(update_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def set_task_status(self, task_gid, status_gid):
        """Updates the 'Approval Status' custom field of a task."""
        print(f"Updating task {task_gid} status...")
        payload = {
            "data": {
                "custom_fields": {
                    config.ASANA_STATUS_FIELD_GID: status_gid
                }
            }
        }
        return self._update_task(task_gid, payload)

    def mark_task_complete(self, task_gid):
        """Marks a task as complete."""
        print(f"Completing task {task_gid}...")
        payload = {"data": {"completed": True}}
        return self._update_task(task_gid, payload)

    def add_error_comment(self, task_gid, error_message):
        """Adds a formatted error comment to a task in Asana."""
        comment_url = f"{self.base_url}/tasks/{task_gid}/stories"

        # We add an HTML body for better formatting in the Asana UI
        formatted_comment = f"<body><strong>🤖 Automation Bot Error:</strong><br>{error_message}</body>"

        payload = {
            "data": {
                "html_text": formatted_comment
            }
        }
        print(f"Adding error comment to task {task_gid}...")
        response = requests.post(comment_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
