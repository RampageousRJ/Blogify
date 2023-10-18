"""Slug Removed

Revision ID: e5cbc278ac0c
Revises: c27071781ef4
Create Date: 2023-10-18 11:31:55.530260

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e5cbc278ac0c'
down_revision = 'c27071781ef4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('slug')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', mysql.VARCHAR(length=255), nullable=True))

    # ### end Alembic commands ###
