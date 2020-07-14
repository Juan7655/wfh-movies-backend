"""First data model complete

Revision ID: d72227819bcc
Revises: 
Create Date: 2020-05-07 22:23:42.833724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72227819bcc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre',
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genre_id'), 'genre', ['id'], unique=False)
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('imdb_id', sa.Integer(), nullable=True),
    sa.Column('tmdb_id', sa.Integer(), nullable=True),
    sa.Column('poster_path', sa.String(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.Column('budget', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movie_id'), 'movie', ['id'], unique=False)
    op.create_index(op.f('ix_movie_title'), 'movie', ['title'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('movie_genre',
    sa.Column('movie', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['genre'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['movie'], ['movie.id'], ),
    sa.PrimaryKeyConstraint('movie', 'genre')
    )
    op.create_table('rating',
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('movie', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user', 'movie')
    )
    op.create_table('tag',
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('movie', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user', 'movie', 'name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag')
    op.drop_table('rating')
    op.drop_table('movie_genre')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_movie_title'), table_name='movie')
    op.drop_index(op.f('ix_movie_id'), table_name='movie')
    op.drop_table('movie')
    op.drop_index(op.f('ix_genre_id'), table_name='genre')
    op.drop_table('genre')
    # ### end Alembic commands ###