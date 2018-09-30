"""empty message

Revision ID: c893592431f0
Revises: 
Create Date: 2018-09-27 09:21:04.320028

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c893592431f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('catalog',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('fullname', sa.String(length=250), nullable=True),
                    sa.Column('email', sa.String(length=50), nullable=True),
                    sa.Column('password', sa.String(length=250), nullable=True),
                    sa.Column('password_salt', sa.String(length=50), nullable=True),
                    sa.Column('google_id', sa.String(length=20), nullable=True),
                    sa.Column('image_url', sa.String(length=1000), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('google_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('catalog')
    # ### end Alembic commands ###