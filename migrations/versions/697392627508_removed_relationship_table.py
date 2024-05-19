"""removed relationship table

Revision ID: 697392627508
Revises: fceb6960a9eb
Create Date: 2024-05-16 23:38:40.298339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '697392627508'
down_revision = 'fceb6960a9eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_settings_level')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_settings_level',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('settings_level_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['settings_level_id'], ['settings_level.id'], name='fk_users_settings_level_settings_level_id_settings_level'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_users_settings_level_user_id_user'),
    sa.PrimaryKeyConstraint('user_id', 'settings_level_id', name='pk_users_settings_level')
    )
    # ### end Alembic commands ###
