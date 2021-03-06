"""Included reviews and user external token

Revision ID: 3bd22154855f
Revises: 0f3359d9596d
Create Date: 2020-06-08 12:23:27.304211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bd22154855f'
down_revision = '0f3359d9596d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review',
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('movie', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user', 'movie')
    )
    op.add_column('users', sa.Column('external_token', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['external_token'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'external_token')
    op.drop_table('review')
    # ### end Alembic commands ###
