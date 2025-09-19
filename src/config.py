import os

# --- Asana Configuration ---
# Your master key for the Asana API
ASANA_PAT = os.getenv("ASANA_PAT")

# The unique ID of the Asana project we are targeting
ASANA_PROJECT_GID = os.getenv("ASANA_PROJECT_GID")

# --- Custom Field GIDs ---
# The unique IDs for each custom field on the Asana board
ASANA_STATUS_FIELD_GID = os.getenv("ASANA_STATUS_FIELD_GID")
ASANA_PLATFORM_FIELD_GID = os.getenv("ASANA_PLATFORM_FIELD_GID")
ASANA_IMAGE_URL_FIELD_GID = os.getenv("ASANA_IMAGE_URL_FIELD_GID")
ASANA_DATE_FIELD_GID = os.getenv("ASANA_DATE_FIELD_GID")
ASANA_TIME_FIELD_GID = os.getenv("ASANA_TIME_FIELD_GID")

# --- Custom Field Option GIDs ---
# The unique IDs for each choice in the "Approval Status" drop-down
ASANA_PERMISSION_GRANTED_GID = os.getenv("ASANA_PERMISSION_GRANTED_GID")
ASANA_POSTING_GID = os.getenv("ASANA_POSTING_GID")
ASANA_POSTED_GID = os.getenv("ASANA_POSTED_GID")
ASANA_POSTING_FAILED_GID = os.getenv("ASANA_POSTING_FAILED_GID")


# --- Social Media Configuration ---
# The credentials for the platforms we will be posting to
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
# We will add other social media keys here as needed...
