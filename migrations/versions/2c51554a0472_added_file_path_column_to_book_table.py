"""Added file_path column to book table

Revision ID: 2c51554a0472
Revises: 
Create Date: 2024-12-14 09:10:30.556773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2c51554a0472'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('file_path',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=200),
               existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=80),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=120),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=120),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.drop_index('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('username', ['username'], unique=True)
        batch_op.alter_column('password',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=80),
               existing_nullable=False)

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('file_path',
               existing_type=sa.String(length=200),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###
