"""add performance indexes

Revision ID: add_performance_indexes
Revises: 5fc19e76aff4
Create Date: 2025-12-25 08:19:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'add_performance_indexes'
down_revision: Union[str, None] = '5fc19e76aff4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add indexes for frequently queried fields to improve query performance
    # Index on is_latest for filtering latest prompts
    op.create_index('idx_prompt_is_latest', 'prompt', ['is_latest'])
    
    # Index on status for filtering by status (draft/published/archived)
    op.create_index('idx_prompt_status', 'prompt', ['status'])
    
    # Index on enabled for filtering enabled/disabled prompts
    op.create_index('idx_prompt_enabled', 'prompt', ['enabled'])
    
    # Index on root_id for version history queries
    op.create_index('idx_prompt_root_id', 'prompt', ['root_id'])
    
    # Index on ai_provider for filtering by provider
    op.create_index('idx_prompt_ai_provider', 'prompt', ['ai_provider'])
    
    # Index on name for filtering by name
    op.create_index('idx_prompt_name', 'prompt', ['name'])
    
    # Composite index for most common query pattern: is_latest=true with filters
    op.create_index('idx_prompt_latest_status_enabled', 'prompt', ['is_latest', 'status', 'enabled'])
    
    # Index on updated_at for ordering
    op.create_index('idx_prompt_updated_at', 'prompt', ['updated_at'])
    
    # Index on version for ordering version history
    op.create_index('idx_prompt_root_id_version', 'prompt', ['root_id', 'version'])


def downgrade() -> None:
    # Remove all indexes in reverse order
    op.drop_index('idx_prompt_root_id_version', 'prompt')
    op.drop_index('idx_prompt_updated_at', 'prompt')
    op.drop_index('idx_prompt_latest_status_enabled', 'prompt')
    op.drop_index('idx_prompt_name', 'prompt')
    op.drop_index('idx_prompt_ai_provider', 'prompt')
    op.drop_index('idx_prompt_root_id', 'prompt')
    op.drop_index('idx_prompt_enabled', 'prompt')
    op.drop_index('idx_prompt_status', 'prompt')
    op.drop_index('idx_prompt_is_latest', 'prompt')
