"""empty message

Revision ID: 34e1b086e2eb
Revises: 
Create Date: 2020-02-09 19:32:02.338708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34e1b086e2eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('configs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(length=128), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('key', sa.String(length=192), nullable=True),
    sa.Column('_type', sa.Enum('Int', 'Bool', 'Float', 'Text', 'Tuple', 'List', 'Set', 'Dict', name='valuetype'), nullable=True),
    sa.Column('_value', sa.String(length=192), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_index(op.f('ix_configs_uuid'), 'configs', ['uuid'], unique=False)
    op.create_table('genres',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(length=128), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_genres_uuid'), 'genres', ['uuid'], unique=False)
    op.create_table('movies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(length=128), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('language', sa.String(length=8), nullable=True),
    sa.Column('imdb_id', sa.String(length=10), nullable=True),
    sa.Column('release_year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movies_uuid'), 'movies', ['uuid'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(length=128), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('_password_hash', sa.String(length=256), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_uuid'), 'users', ['uuid'], unique=False)
    op.create_table('movie_genre_xref',
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.PrimaryKeyConstraint('movie_id', 'genre_id')
    )
    op.create_table('rentals',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(length=128), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('date_rented', sa.DateTime(), nullable=True),
    sa.Column('date_returned', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rentals_uuid'), 'rentals', ['uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rentals_uuid'), table_name='rentals')
    op.drop_table('rentals')
    op.drop_table('movie_genre_xref')
    op.drop_index(op.f('ix_users_uuid'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_movies_uuid'), table_name='movies')
    op.drop_table('movies')
    op.drop_index(op.f('ix_genres_uuid'), table_name='genres')
    op.drop_table('genres')
    op.drop_index(op.f('ix_configs_uuid'), table_name='configs')
    op.drop_table('configs')
    # ### end Alembic commands ###