"""removed list tables

Revision ID: d09e89eb774c
Revises: 0b696781410c
Create Date: 2019-12-12 12:53:12.347797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd09e89eb774c'
down_revision = '0b696781410c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('list_item')
    op.drop_table('list')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('list',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('list_name', sa.VARCHAR(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('list_item',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('list_id', sa.INTEGER(), nullable=True),
    sa.Column('list_value', sa.VARCHAR(length=20), nullable=True),
    sa.ForeignKeyConstraint(['list_id'], ['list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###