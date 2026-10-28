"""Колонка пароля должна вмещать хеш scrypt.

Revision ID: d4b12f8a6c21
Revises: c3a91e2b7d10
Create Date: 2026-10-28 20:25:00
"""
from alembic import op
import sqlalchemy as sa


revision = "d4b12f8a6c21"
down_revision = "c3a91e2b7d10"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user") as batch:
        batch.alter_column(
            "password",
            existing_type=sa.String(length=128),
            type_=sa.String(length=255),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table("user") as batch:
        batch.alter_column(
            "password",
            existing_type=sa.String(length=255),
            type_=sa.String(length=128),
            existing_nullable=True,
        )
