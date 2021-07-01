"""empty message

Revision ID: 17f1ecafec96
Revises: 
Create Date: 2021-07-01 17:40:34.738415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17f1ecafec96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('height', sa.String(), nullable=False),
    sa.Column('mass', sa.String(), nullable=False),
    sa.Column('hair_color', sa.String(), nullable=False),
    sa.Column('skin_color', sa.String(), nullable=False),
    sa.Column('eye_color', sa.String(), nullable=False),
    sa.Column('birth_year', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('homeworld', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('diameter', sa.String(), nullable=False),
    sa.Column('climate', sa.String(), nullable=False),
    sa.Column('gravity', sa.String(), nullable=False),
    sa.Column('terrain', sa.String(), nullable=False),
    sa.Column('population', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('favoritecharacters',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_character', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_character'], ['character.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_user', 'id_character')
    )
    op.create_table('favoriteplanet',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_planet', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_planet'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_user', 'id_planet')
    )
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    op.drop_table('favoriteplanet')
    op.drop_table('favoritecharacters')
    op.drop_table('user')
    op.drop_table('planet')
    op.drop_table('character')
    # ### end Alembic commands ###