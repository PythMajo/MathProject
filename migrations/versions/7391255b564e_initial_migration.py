"""Initial migration

Revision ID: 7391255b564e
Revises: 
Create Date: 2024-05-20 17:45:17.463458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7391255b564e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collectable_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fa_code', sa.String(length=100), nullable=True),
    sa.Column('color', sa.String(length=50), nullable=True),
    sa.Column('test', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_collectable_items'))
    )
    op.create_table('settings_level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_settings_level'))
    )
    op.create_table('settings_operators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('operator', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_settings_operators'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('settings_level_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['settings_level_id'], ['settings_level.id'], name=op.f('fk_user_settings_level_id_settings_level')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('problem', sa.String(length=50), nullable=False),
    sa.Column('user_answer', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_answers_author_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_answers'))
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=130), nullable=False),
    sa.Column('body', sa.String(length=1200), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_post_author_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post'))
    )
    op.create_table('user_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('operator_plus_option', sa.Boolean(), nullable=False),
    sa.Column('operator_minus_option', sa.Boolean(), nullable=True),
    sa.Column('operator_multiply_option', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_user_options_author_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_options'))
    )
    op.create_table('users_collectable_items',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('collectable_items_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['collectable_items_id'], ['collectable_items.id'], name=op.f('fk_users_collectable_items_collectable_items_id_collectable_items')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_users_collectable_items_user_id_user'))
    )
    op.create_table('users_settings_operators',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('settings_operator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['settings_operator_id'], ['settings_operators.id'], name=op.f('fk_users_settings_operators_settings_operator_id_settings_operators')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_users_settings_operators_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', 'settings_operator_id', name=op.f('pk_users_settings_operators'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_settings_operators')
    op.drop_table('users_collectable_items')
    op.drop_table('user_options')
    op.drop_table('post')
    op.drop_table('answers')
    op.drop_table('user')
    op.drop_table('settings_operators')
    op.drop_table('settings_level')
    op.drop_table('collectable_items')
    # ### end Alembic commands ###