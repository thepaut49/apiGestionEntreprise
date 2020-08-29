"""empty message

Revision ID: 4835d44e468e
Revises: 
Create Date: 2020-08-29 17:09:30.524476

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4835d44e468e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='product')
    op.drop_table('product')
    op.add_column('user', sa.Column('mail', sa.String(length=50), nullable=True))
    op.create_unique_constraint(None, 'user', ['mail'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'mail')
    op.create_table('product',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('description', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('price', mysql.FLOAT(), nullable=True),
    sa.Column('qty', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'product', ['name'], unique=True)
    # ### end Alembic commands ###