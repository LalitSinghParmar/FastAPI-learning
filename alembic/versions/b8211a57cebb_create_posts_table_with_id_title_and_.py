"""Create posts table with id, title and content as column

Revision ID: b8211a57cebb
Revises: 
Create Date: 2022-07-01 08:25:16.498499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8211a57cebb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id',sa.Integer, primary_key=True, nullable=False),
    sa.Column('title',sa.String, nullable=False),
    sa.Column('content',sa.String, nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass