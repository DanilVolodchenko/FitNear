"""
empty message

Revision ID: 1f82e7513b4a
Revises: f8adac21e4de
Create Date: 2026-09-17 15:11:19.132946
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1f82e7513b4a'
down_revision: str | Sequence[str] | None = 'f8adac21e4de'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'auth_tokens',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('type', sa.Enum('email_confirmation', 'password_reset', name='auth_token_type_enum'), nullable=False),
        sa.Column('token_hash', sa.String(), nullable=False),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_auth_tokens_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_auth_tokens')),
    )
    op.create_index(op.f('ix_auth_tokens_token_hash'), 'auth_tokens', ['token_hash'], unique=False)
    op.create_index(op.f('ix_auth_tokens_user_id'), 'auth_tokens', ['user_id'], unique=False)
    op.create_table(
        'registration_tokens',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('token_hash', sa.String(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column(
            'type', sa.Enum('email_confirmation', 'password_reset', name='registration_token_type_enum'), nullable=False
        ),
        sa.Column('attempts', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk_registration_tokens_user_id_users'), ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_registration_tokens')),
    )
    op.create_index(op.f('ix_registration_tokens_token_hash'), 'registration_tokens', ['token_hash'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f('ix_registration_tokens_token_hash'), table_name='registration_tokens')
    op.drop_table('registration_tokens')
    op.drop_index(op.f('ix_auth_tokens_user_id'), table_name='auth_tokens')
    op.drop_index(op.f('ix_auth_tokens_token_hash'), table_name='auth_tokens')
    op.drop_table('auth_tokens')
    sa.Enum('email_confirmation', 'password_reset', name='auth_token_type_enum').drop(op.get_bind())
    sa.Enum('email_confirmation', 'password_reset', name='registration_token_type_enum').drop(op.get_bind())
