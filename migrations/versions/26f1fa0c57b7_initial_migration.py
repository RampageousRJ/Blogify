"""Initial Migration

Revision ID: 26f1fa0c57b7
Revises: 
Create Date: 2023-09-07 21:24:34.535746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26f1fa0c57b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('color', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('color')

    # ### end Alembic commands ###
