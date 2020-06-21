"""including user genres column

Revision ID: bb51d18656d3
Revises: e5bf6695a336
Create Date: 2020-06-20 19:26:23.204260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb51d18656d3'
down_revision = 'e5bf6695a336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('genres', sa.String(), server_default='', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'genres')
    # ### end Alembic commands ###
