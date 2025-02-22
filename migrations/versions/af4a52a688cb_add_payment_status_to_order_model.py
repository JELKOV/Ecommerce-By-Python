"""Add payment status to Order model

Revision ID: af4a52a688cb
Revises: 8ad4dd4be4fd
Create Date: 2025-02-22 14:06:06.426517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af4a52a688cb'
down_revision = '8ad4dd4be4fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_status', sa.String(length=50), nullable=True))
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('payment_status')

    # ### end Alembic commands ###
