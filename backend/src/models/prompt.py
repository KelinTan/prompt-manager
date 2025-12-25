from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional

from sqlalchemy import JSON, Column, Index
from sqlmodel import Field, SQLModel

from src.aigc.aigc import AiProvider, CompletionReturnType


class PromptType(StrEnum):
    text = "text"
    image = "image"
    audio = "audio"
    video = "video"


class FormatType(StrEnum):
    square_brackets = "square_brackets"
    braces = "braces"
    none = "none"


class PromptName(StrEnum):
    ai_talk = "ai_talk"
    ai_talk_evaluation = "ai_talk_evaluation"
    read_aloud_evaluation = "read_aloud_evaluation"
    semi_open_qa_evaluation = "semi_open_qa_evaluation"
    stage_assessment_dsr_evaluation = "stage_assessment_dsr_evaluation"
    stage_assessment_overall_report = "stage_assessment_overall_report"
    stage_assessment_sing_along_report = "stage_assessment_sing_along_report"
    stage_assessment_dancing_report = "stage_assessment_dancing_report"
    dancing_video_extract_details = "dancing_video_extract_details"
    generate_ai_reading = "generate_ai_reading"
    extract_words_from_reading = "extract_words_from_reading"
    translate_words = "translate_words"


class PromptStatus(StrEnum):
    draft = "draft"
    published = "published"
    archived = "archived"


class Prompt(SQLModel, table=True):
    __tablename__ = "prompt"
    
    # Performance indexes defined at model level
    __table_args__ = (
        Index('idx_prompt_is_latest', 'is_latest'),
        Index('idx_prompt_status', 'status'),
        Index('idx_prompt_enabled', 'enabled'),
        Index('idx_prompt_root_id', 'root_id'),
        Index('idx_prompt_ai_provider', 'ai_provider'),
        Index('idx_prompt_name', 'name'),
        Index('idx_prompt_latest_status_enabled', 'is_latest', 'status', 'enabled'),
        Index('idx_prompt_updated_at', 'updated_at'),
        Index('idx_prompt_root_id_version', 'root_id', 'version'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str | None = Field(nullable=True)
    name: str
    template: str
    type: PromptType = PromptType.text
    model: str = Field(nullable=True)
    mock: bool = Field(default=True)
    mock_data: str | None = Field(nullable=True)
    return_type: CompletionReturnType = CompletionReturnType.text
    parameters: dict = Field(sa_column=Column(JSON), default={})
    format_type: FormatType = FormatType.braces
    remark: str = Field(nullable=True)
    ai_provider: AiProvider | None = Field(nullable=True)
    is_latest: bool = Field(default=True)
    version: int = Field(default=1)
    status: PromptStatus = Field(default=PromptStatus.draft)
    enabled: bool = Field(default=True)
    root_id: int | None = Field(default=None, nullable=True)
    created_by: str | None = Field(default=None, nullable=True)
    updated_by: str | None = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
