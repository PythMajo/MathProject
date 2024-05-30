from matematik.models import Answer, User, UserOptions, SettingsOperators, SettingsLevel, CollectableItems
from datetime import datetime
from matematik import db
import pytest


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """

    assert new_user.username == 'test_user'
    assert new_user.check_password('password')
    assert new_user.settings_level_id == 1


@pytest.mark.usefixtures("init_database", "new_user")
def test_answer_model(init_database, new_user):
    """
    GIVEN an Answer model
    WHEN a new Answer is created
    THEN check the id, author_id, created, problem, and user_answer fields are defined correctly
    """
    answer = Answer(
        author_id=new_user.id,
        created=datetime.utcnow(),
        problem='2+2?',
        user_answer=True
    )
    db.session.add(answer)
    db.session.commit()

    assert answer.id is not None
    assert answer.author_id == new_user.id
    assert isinstance(answer.created, datetime)
    assert answer.problem == '2+2?'
    assert answer.user_answer is True

    # Fetch the answer from the database and check
    fetched_answer = Answer.query.filter_by(id=answer.id).first()
    assert fetched_answer is not None
    assert fetched_answer.id == answer.id
    assert fetched_answer.author_id == answer.author_id
    assert fetched_answer.problem == answer.problem
    assert fetched_answer.user_answer == answer.user_answer


def test_user_options_model(init_database, new_user):
    """
    GIVEN a UserOptions model
    WHEN a new UserOptions is created
    THEN check the id, author_id, operator_plus_option, operator_minus_option, and operator_multiply_option fields are defined correctly
    """
    user_options = UserOptions(
        author_id=new_user.id,
        operator_plus_option=True,
        operator_minus_option=False,
        operator_multiply_option=True
    )
    db.session.add(user_options)
    db.session.commit()

    assert user_options.id is not None
    assert user_options.author_id == new_user.id
    assert user_options.operator_plus_option is True
    assert user_options.operator_minus_option is False
    assert user_options.operator_multiply_option is True

    # Fetch the user_options from the database and check
    fetched_user_options = UserOptions.query.filter_by(id=user_options.id).first()
    assert fetched_user_options is not None
    assert fetched_user_options.id == user_options.id
    assert fetched_user_options.author_id == user_options.author_id
    assert fetched_user_options.operator_plus_option == user_options.operator_plus_option
    assert fetched_user_options.operator_minus_option == user_options.operator_minus_option
    assert fetched_user_options.operator_multiply_option == user_options.operator_multiply_option


def test_settings_operators_model(init_database):
    """
    GIVEN a SettingsOperators model
    WHEN a new SettingsOperators is created
    THEN check the id, name, and operator fields are defined correctly
    """
    operator = SettingsOperators(
        name='Addition',
        operator='+'
    )
    db.session.add(operator)
    db.session.commit()

    assert operator.id is not None
    assert operator.name == 'Addition'
    assert operator.operator == '+'

    # Fetch the operator from the database and check
    fetched_operator = SettingsOperators.query.filter_by(id=operator.id).first()
    assert fetched_operator is not None
    assert fetched_operator.id == operator.id
    assert fetched_operator.name == operator.name
    assert fetched_operator.operator == operator.operator


def test_settings_level_model(init_database):
    """
    GIVEN a SettingsLevel model
    WHEN a new SettingsLevel is created
    THEN check the id and name fields are defined correctly
    """
    level = SettingsLevel(
        name='Easy'
    )
    db.session.add(level)
    db.session.commit()

    assert level.id is not None
    assert level.name == 'Easy'

    # Fetch the level from the database and check
    fetched_level = SettingsLevel.query.filter_by(id=level.id).first()
    assert fetched_level is not None
    assert fetched_level.id == level.id
    assert fetched_level.name == level.name


def test_collectable_items_model(init_database):
    """
    GIVEN a CollectableItems model
    WHEN a new CollectableItems is created
    THEN check the id, fa_code, color, and test fields are defined correctly
    """
    item = CollectableItems(
        fa_code='fa-solid fa-cow',
        color='#FFD43B',
        test=1
    )
    db.session.add(item)
    db.session.commit()

    assert item.id is not None
    assert item.fa_code == 'fa-solid fa-cow'
    assert item.color == '#FFD43B'
    assert item.test == 1

    # Fetch the item from the database and check
    fetched_item = CollectableItems.query.filter_by(id=item.id).first()
    assert fetched_item is not None
    assert fetched_item.id == item.id
    assert fetched_item.fa_code == item.fa_code
    assert fetched_item.color == item.color
    assert fetched_item.test == item.test
