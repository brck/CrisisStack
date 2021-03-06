"""empty message

Revision ID: d85a5a195958
Revises: None
Create Date: 2016-11-07 15:05:03.625958

"""

# revision identifiers, used by Alembic.
revision = 'd85a5a195958'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_apps')
    op.add_column('application', sa.Column('installed', sa.Boolean(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('application', 'installed')
    op.create_table('user_apps',
    sa.Column('application_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['application_id'], [u'application.id'], name=u'user_apps_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], [u'user.id'], name=u'user_apps_ibfk_2'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
