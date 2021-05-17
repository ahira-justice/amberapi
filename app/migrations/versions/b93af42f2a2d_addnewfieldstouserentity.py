"""AddNewFieldsToUserEntity

Revision ID: b93af42f2a2d
Revises: 93f675923f33
Create Date: 2021-05-16 23:26:12.876497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b93af42f2a2d'
down_revision = '93f675923f33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users', 'username')
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
