"""Одно описание на маршрут.

Revision ID: b7e3a91c4d02
Revises: d4b12f8a6c21
Create Date: 2026-10-28 20:50:00
"""
from alembic import op
import sqlalchemy as sa


revision = "b7e3a91c4d02"
down_revision = "d4b12f8a6c21"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    rows = bind.execute(sa.text(
        "SELECT id, route_id FROM detail ORDER BY id"
    )).fetchall()
    seen = set()
    for row in rows:
        if row.route_id in seen:
            bind.execute(sa.text("DELETE FROM detail WHERE id = :id"), {"id": row.id})
        else:
            seen.add(row.route_id)
    with op.batch_alter_table("detail") as batch:
        batch.create_unique_constraint("uq_detail_route_id", ["route_id"])


def downgrade():
    with op.batch_alter_table("detail") as batch:
        batch.drop_constraint("uq_detail_route_id", type_="unique")
