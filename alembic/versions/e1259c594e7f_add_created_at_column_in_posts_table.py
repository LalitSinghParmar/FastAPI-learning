"""Add created_at column in posts table

Revision ID: e1259c594e7f
Revises: b8211a57cebb
Create Date: 2022-07-01 13:36:40.825277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1259c594e7f'
down_revision = 'b8211a57cebb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text(
        'now()'),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','created_at')
    pass
