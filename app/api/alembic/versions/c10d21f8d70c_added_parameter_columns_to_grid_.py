"""Added parameter columns to grid_visualization

Revision ID: c10d21f8d70c
Revises: 986bbb0db4d4
Create Date: 2022-03-15 17:58:03.966569

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import sqlmodel  



# revision identifiers, used by Alembic.
revision = 'c10d21f8d70c'
down_revision = '986bbb0db4d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grid_visualization', sa.Column('area_isochrone', sa.Float(precision=53), nullable=True), schema='basic')
    op.add_column('grid_visualization', sa.Column('percentile_area_isochrone', sa.SmallInteger(), nullable=True), schema='basic')
    op.add_column('grid_visualization', sa.Column('percentile_population', sa.SmallInteger(), nullable=True), schema='basic')
    op.add_column('grid_visualization', sa.Column('population', sa.Integer(), nullable=True), schema='basic')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('grid_visualization', 'population', schema='basic')
    op.drop_column('grid_visualization', 'percentile_population', schema='basic')
    op.drop_column('grid_visualization', 'percentile_area_isochrone', schema='basic')
    op.drop_column('grid_visualization', 'area_isochrone', schema='basic')
    # ### end Alembic commands ###