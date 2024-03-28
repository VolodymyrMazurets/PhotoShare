"""empty message

Revision ID: 488e1d8d9676
Revises: 512a44dd440d, e8d7de85a1bf
Create Date: 2024-03-27 12:35:26.571136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '488e1d8d9676'
down_revision: Union[str, None] = ('512a44dd440d', 'e8d7de85a1bf')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
