"""make username unique

Revision ID: e0287f484c3d
Revises: bb08a155f61b
Create Date: 2026-09-24 21:24:24.497285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0287f484c3d'
down_revision: Union[str, Sequence[str], None] = 'bb08a155f61b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_users_username",
        "users",
        ["username"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_users_username",
        "users",
        type_="unique",
    )
