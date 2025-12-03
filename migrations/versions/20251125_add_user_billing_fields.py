"""Add billing-related fields to user

Revision ID: 5b7d98c7f2b0
Revises: 080eaac6e013
Create Date: 2025-11-25 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "5b7d98c7f2b0"
down_revision = "080eaac6e013"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "started",
                sa.DateTime(),
                nullable=False,
                server_default=sa.func.now(),
            )
        )
        batch_op.add_column(sa.Column("lastPaymentDate", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("lastPaymentAmount", sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column(
                "recurringPayment",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )
        batch_op.add_column(
            sa.Column(
                "isTrial",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )

    # Drop server defaults to avoid locking DB-level defaults if not desired
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column("started", server_default=None)
        batch_op.alter_column("recurringPayment", server_default=None)
        batch_op.alter_column("isTrial", server_default=None)


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("isTrial")
        batch_op.drop_column("recurringPayment")
        batch_op.drop_column("lastPaymentAmount")
        batch_op.drop_column("lastPaymentDate")
        batch_op.drop_column("started")
