"""add password_hash to ngo and volunteer

Revision ID: add_password_hash
Revises: cd7d3dadff13
Create Date: 2025-11-03 11:09:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_password_hash'
down_revision = 'cd7d3dadff13'
branch_labels = None
depends_on = None


def upgrade():
    # Add password_hash column to ngos table
    op.add_column('ngos', sa.Column('password_hash', sa.String(length=255), nullable=True))
    
    # Add password_hash column to volunteers table
    op.add_column('volunteers', sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade():
    # Remove password_hash column from volunteers table
    op.drop_column('volunteers', 'password_hash')
    
    # Remove password_hash column from ngos table
    op.drop_column('ngos', 'password_hash')
