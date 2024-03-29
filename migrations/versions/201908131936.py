"""empty message

Revision ID: 188eb4eb1b66
Revises: 
Create Date: 2019-08-13 19:36:25.307579+07:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '188eb4eb1b66'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_tokens',
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('deleted_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=128), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('logged_datetime', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('deleted_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', mssql.TINYINT(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('facebook', sa.String(length=255), nullable=True),
    sa.Column('email_confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('active_code', sa.String(length=128), nullable=True),
    sa.Column('active_code_expired_at', sa.Integer(), nullable=True),
    sa.Column('roles', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index('idx_email', 'users', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_email', table_name='users')
    op.drop_table('users')
    op.drop_table('user_tokens')
    # ### end Alembic commands ###
