"""add name attributes

Revision ID: 7e6e9388c93b
Revises: ebba1e70ece9
Create Date: 2021-05-23 23:03:56.811754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7e6e9388c93b"
down_revision = "ebba1e70ece9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("Client", sa.Column("name", sa.String))
    op.add_column("Employee", sa.Column("matricule", sa.String))


def downgrade():
    op.drop_column("Client", "name")
    op.drop_column("Employee", "matricule")
