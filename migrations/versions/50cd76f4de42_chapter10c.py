"""chapter10c

Revision ID: 50cd76f4de42
Revises: 7a9e2b9c467d
Create Date: 2017-03-27 15:15:59.111472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50cd76f4de42'
down_revision = '7a9e2b9c467d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_me', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('location', sa.Unicode(length=64), nullable=True))
    op.add_column('users', sa.Column('member_since', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('name', sa.Unicode(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'name')
    op.drop_column('users', 'member_since')
    op.drop_column('users', 'location')
    op.drop_column('users', 'last_seen')
    op.drop_column('users', 'avatar_hash')
    op.drop_column('users', 'about_me')
    # ### end Alembic commands ###
