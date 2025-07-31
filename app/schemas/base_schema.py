from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    """Base schema for all Pydantic models"""
    model_config = ConfigDict(from_attributes=True)

class BaseResponseSchema(BaseSchema):
    """Base response schema with common fields"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
