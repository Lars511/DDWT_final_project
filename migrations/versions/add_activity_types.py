"""Add ActivityType model and update Activity

Revision ID: add_activity_types
Revises: 80d4586e8f91
Create Date: 2026-01-12

"""
from alembic import op
import sqlalchemy as sa


#revision identifiers
revision = 'add_activity_types'
down_revision = '80d4586e8f91'
branch_labels = None
depends_on = None


def upgrade():
    #Create activity_types table
    op.create_table('activity_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name='fk_activity_types_category'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'category_id', name='unique_type_per_category')
    )

    #Add activity_type_id column to activities table
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.add_column(sa.Column('activity_type_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_activities_activity_type', 'activity_types', ['activity_type_id'], ['id'])


def downgrade():
    #Remove activity_type_id from activities
    with op.batch_alter_table('activities', schema=None) as batch_op:
        batch_op.drop_constraint('fk_activities_activity_type', type_='foreignkey')
        batch_op.drop_column('activity_type_id')

    #Drop activity_types table
    op.drop_table('activity_types')