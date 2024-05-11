from typing import Dict, Any, Optional


def get_user_options(author_id: int, db) -> Optional[Dict[str, Any]]:
    """
    Retrieve user options from the user_options table for a given author_id.

    Args:
        author_id (int): The ID of the user whose options are to be retrieved.

    Returns:
        Dict[str, Any]: A dictionary containing user options if found, None otherwise.
    """
    cursor = db.cursor()

    # Fetch user options from the database
    cursor.execute("SELECT * FROM user_options WHERE author_id = ?", (author_id,))
    user_options = cursor.fetchone()

    # Close the database connection
    db.close()

    # If user options are found, return them as a dictionary
    if user_options:
        # Assuming the database columns are in the same order as in the query
        column_names = [description[0] for description in cursor.description]
        user_options_dict = dict(zip(column_names, user_options))
        return user_options_dict
    else:
        return None
