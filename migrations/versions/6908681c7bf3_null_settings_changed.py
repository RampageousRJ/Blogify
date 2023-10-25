"""Null settings changed

Revision ID: 6908681c7bf3
Revises: f4383bc12490
Create Date: 2023-10-25 11:22:00.161922

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6908681c7bf3'
down_revision = 'f4383bc12490'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriber', schema=None) as batch_op:
        batch_op.alter_column('follower',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('following',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriber', schema=None) as batch_op:
        batch_op.alter_column('following',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('follower',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###