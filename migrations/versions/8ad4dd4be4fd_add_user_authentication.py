"""Add user authentication

Revision ID: 8ad4dd4be4fd
Revises: fe4bcb53491e
Create Date: 2025-02-22 02:24:13.044182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ad4dd4be4fd'
down_revision = 'fe4bcb53491e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=200), nullable=False))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
