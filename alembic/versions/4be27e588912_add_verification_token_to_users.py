"""add verification token to users

Revision ID: 4be27e588912
Revises: e0287f484c3d
Create Date: 2026-09-25 07:43:16.241066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4be27e588912'
down_revision: Union[str, Sequence[str], None] = 'e0287f484c3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "verification_token",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.create_unique_constraint(
        "uq_users_verification_token",
        "users",
        ["verification_token"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_users_verification_token",
        "users",
        type_="unique",
    )

    op.drop_column(
        "users",
        "verification_token",
    )
