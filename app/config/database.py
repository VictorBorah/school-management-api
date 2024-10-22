import os
from dotenv import load_dotenv
from xata.client import XataClient

load_dotenv()

# Constants for table names
TABLE_STUDENTS = "tbl_students"  # Define table name as a constant

def get_db():
    """
    Create and return a Xata client instance
    Database URL format: https://{workspace-slug}.xata.sh/db/{database-name}
    """
    client = XataClient(
        api_key=os.getenv("XATA_API_KEY"),
        db_url=os.getenv("XATA_DATABASE_URL"),
        branch_name=os.getenv("XATA_BRANCH")
    )
    return client