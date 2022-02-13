"""added default settings to study area

Revision ID: 1410c9e58044
Revises: ef6d9681f09d
Create Date: 2022-02-13 19:17:49.082189

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import sqlmodel  

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1410c9e58044'
down_revision = 'ef6d9681f09d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('study_area', sa.Column('default_setting', postgresql.JSONB(astext_type=sa.Text())), schema='basic')
    op.alter_column('user', 'storage',
               existing_type=sa.INTEGER(),
               nullable=False,
               schema='customer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'storage',
               existing_type=sa.INTEGER(),
               nullable=True,
               schema='customer')
    op.drop_column('study_area', 'default_setting', schema='basic')
    # ### end Alembic commands ###
