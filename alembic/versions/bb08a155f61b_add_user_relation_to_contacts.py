"""add user relation to contacts

Revision ID: bb08a155f61b
Revises: aeb10a566492
Create Date: 2026-09-24 19:55:53.769948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb08a155f61b'
down_revision: Union[str, Sequence[str], None] = 'aeb10a566492'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "contacts",
        sa.Column("user_id", sa.Integer(), nullable=False),
    )

    op.create_foreign_key(
        "fk_contacts_user_id_users",
        "contacts",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_contacts_user_id_users",
        "contacts",
        type_="foreignkey",
    )

    op.drop_column("contacts", "user_id")