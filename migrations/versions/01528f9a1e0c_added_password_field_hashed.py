"""Added password field hashed

Revision ID: 01528f9a1e0c
Revises: 0d21f846b2c7
Create Date: 2023-09-08 01:40:57.637622

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '01528f9a1e0c'
down_revision = '0d21f846b2c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash2', sa.String(length=128), nullable=True))
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
        batch_op.drop_column('password_hash2')

    # ### end Alembic commands ###