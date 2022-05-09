"""Another Migration

Revision ID: 377543003483
Revises: 367a7389740d
Create Date: 2022-05-08 18:52:37.923223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '377543003483'
down_revision = '367a7389740d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=60), nullable=False))
    op.add_column('users', sa.Column('image_file', sa.String(length=20), nullable=False))
    op.drop_column('users', 'profile_pic_path')
    op.drop_column('users', 'pass_secure')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pass_secure', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('profile_pic_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'image_file')
    op.drop_column('users', 'password')
    # ### end Alembic commands ###