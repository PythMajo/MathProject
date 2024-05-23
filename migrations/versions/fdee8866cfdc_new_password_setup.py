"""new password setup

Revision ID: fdee8866cfdc
Revises: 8002b547ec91
Create Date: 2024-05-23 22:23:20.010085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdee8866cfdc'
down_revision = '8002b547ec91'
branch_labels = None
depends_on = None


def upgrade():
    # Rename the 'password' column to '_password'
    op.alter_column('user', 'password',
                    new_column_name='_password',
                    existing_type=sa.String(length=400),
                    existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # Rename the '_password' column back to 'password'
    op.alter_column('user', '_password',
                    new_column_name='password',
                    existing_type=sa.String(length=400),
                    existing_nullable=False)