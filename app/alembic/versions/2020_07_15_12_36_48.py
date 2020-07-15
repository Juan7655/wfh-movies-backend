"""Changed constraints for Reviews-Ratings

Revision ID: 4ffdcb6ee36c
Revises: 5d8f377f0cbf
Create Date: 2020-07-15 12:36:48.517706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ffdcb6ee36c'
down_revision = '5d8f377f0cbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('review_movie_fkey', 'review', type_='foreignkey')
    op.drop_constraint('review_user_fkey', 'review', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('review_user_fkey', 'review', 'users', ['user'], ['id'])
    op.create_foreign_key('review_movie_fkey', 'review', 'movie', ['movie'], ['id'])
    # ### end Alembic commands ###
