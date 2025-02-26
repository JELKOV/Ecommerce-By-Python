"""add order_name column to order table

Revision ID: 4f7cd994b81e
Revises: fb9db8b5239e
Create Date: 2025-02-26 19:51:05.580698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f7cd994b81e'
down_revision = 'fb9db8b5239e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_name', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('order_name')

    # ### end Alembic commands ###
