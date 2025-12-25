"""add prompt table

Revision ID: 5fc19e76aff4
Revises: 
Create Date: 2025-12-25 13:38:03.940510

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5fc19e76aff4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

"""
CREATE TABLE `prompt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `model` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `return_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `template` text COLLATE utf8mb4_bin,
  `parameters` json DEFAULT NULL,
  `mock` tinyint(1) DEFAULT '1',
  `mock_data` text COLLATE utf8mb4_bin,
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `format_type` enum('square_brackets','braces','none') COLLATE utf8mb4_bin NOT NULL DEFAULT 'braces',
  `ai_provider` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `is_latest` tinyint(1) NOT NULL DEFAULT '1',
  `version` int(11) NOT NULL DEFAULT '1',
  `status` varchar(50) COLLATE utf8mb4_bin NOT NULL DEFAULT 'published',
  `enabled` int(11) NOT NULL DEFAULT '1',
  `root_id` int(11) DEFAULT NULL,
  `created_by` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `updated_by` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=342 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
"""


def upgrade() -> None:
    op.create_table(
        'prompt',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('type', sa.String(255), nullable=True),
        sa.Column('model', sa.String(255), nullable=True),
        sa.Column('return_type', sa.String(255), nullable=True),
        sa.Column('template', sa.Text, nullable=True),
        sa.Column('parameters', sa.JSON, nullable=True),
        sa.Column('mock', sa.Boolean, nullable=False, default=True),
        sa.Column('mock_data', sa.Text, nullable=True),
        sa.Column('remark', sa.String(255), nullable=True),
        sa.Column('format_type', sa.Enum('square_brackets', 'braces', 'none'), nullable=False, default='braces'),
        sa.Column('ai_provider', sa.String(20), nullable=True),
        sa.Column('is_latest', sa.Boolean, nullable=False, default=True),
        sa.Column('version', sa.Integer, nullable=False, default=1),
        sa.Column('status', sa.String(50), nullable=False, default='published'),
        sa.Column('enabled', sa.Integer, nullable=False, default=1),
        sa.Column('root_id', sa.Integer, nullable=True),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                  nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.text('NULL ON UPDATE CURRENT_TIMESTAMP'),
                  nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_bin'
    )


def downgrade() -> None:
    pass
