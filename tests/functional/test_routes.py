from matematik import create_app, db
import pytest
from flask import url_for


def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid and redirects to the expected page
     """

    response = test_client.get('/')
    assert response.status_code == 302  # Check for redirection
    assert response.headers["Location"] == "/math/"  # Check for the specific redirection location
