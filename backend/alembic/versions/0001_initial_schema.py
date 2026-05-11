"""Initial schema - all 6 tables

Revision ID: 0001
Revises:
Create Date: 2026-05-10
"""
# DATABASE_AGENT | 2026-05-10 | Initial migration creating all tables
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "projects",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("output_dir", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_projects_user_id", "projects", ["user_id"])

    op.create_table(
        "sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("phase", sa.String(20), nullable=False, server_default="discovery"),
        sa.Column("architecture_doc", sa.Text, nullable=True),
        sa.Column("research_brief", sa.Text, nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sessions_project_id", "sessions", ["project_id"])

    op.create_table(
        "agent_tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("session_id", sa.String(36), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("agent_type", sa.String(20), nullable=False),
        sa.Column("task_number", sa.Integer, nullable=False, server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("input_context", sa.JSON, nullable=True),
        sa.Column("output", sa.Text, nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_agent_tasks_session_id_status", "agent_tasks", ["session_id", "status"])

    op.create_table(
        "messages",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("session_id", sa.String(36), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("agent_task_id", sa.String(36), sa.ForeignKey("agent_tasks.id", ondelete="SET NULL"), nullable=True),
        sa.Column("message_type", sa.String(30), nullable=False),
        sa.Column("sender", sa.String(50), nullable=False),
        sa.Column("target", sa.String(50), nullable=True),
        sa.Column("body", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_messages_session_id_created_at", "messages", ["session_id", "created_at"])

    op.create_table(
        "generated_files",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("session_id", sa.String(36), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("agent_task_id", sa.String(36), sa.ForeignKey("agent_tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relative_path", sa.String(500), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("language", sa.String(50), nullable=True),
        sa.Column("written_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_generated_files_session_id", "generated_files", ["session_id"])


def downgrade() -> None:
    op.drop_table("generated_files")
    op.drop_table("messages")
    op.drop_table("agent_tasks")
    op.drop_table("sessions")
    op.drop_table("projects")
    op.drop_table("users")
