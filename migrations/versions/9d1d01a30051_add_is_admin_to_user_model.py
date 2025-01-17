"""Add is_admin to User model

Revision ID: 9d1d01a30051
Revises: 2c51554a0472
Create Date: 2024-12-14 15:42:42.775510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9d1d01a30051'
down_revision = '2c51554a0472'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('file_path')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_path', mysql.VARCHAR(length=200), nullable=True))

    # ### end Alembic commands ###
