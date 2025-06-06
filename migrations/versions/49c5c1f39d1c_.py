"""empty message

Revision ID: 49c5c1f39d1c
Revises: 
Create Date: 2025-05-10 02:53:46.865878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49c5c1f39d1c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('gender', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('username')
    )
    op.create_table('pokemons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pokemon_name', sa.String(length=128), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemons')
    op.drop_table('users')
    # ### end Alembic commands ###
