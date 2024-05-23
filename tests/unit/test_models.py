from matematik.models import User


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """

    assert new_user.username == 'test_user'
    assert new_user.check_password('password')
    assert new_user.settings_level_id == 1