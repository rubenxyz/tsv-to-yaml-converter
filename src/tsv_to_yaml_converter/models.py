"""Data models for TSV to YAML converter."""

from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ShotTimecode(BaseModel):
    """Shot timecode information for a shot."""
    
    in_time: Optional[str] = Field(default=None, alias="in")
    out_time: Optional[str] = Field(default=None, alias="out")
    
    class Config:
        populate_by_name = True


class CameraMovement(BaseModel):
    """Camera movement information for a shot."""
    
    speed: Optional[str] = None
    movement_type: Optional[str] = Field(default=None, alias="type")
    
    class Config:
        populate_by_name = True


class Shot(BaseModel):
    """Individual shot information."""
    
    shot_number: int
    shot_timecode: ShotTimecode
    specific_area: Optional[str] = None
    camera_movement: CameraMovement
    angle: Optional[str] = None
    description: Optional[str] = None


class Scene(BaseModel):
    """Scene information containing multiple shots."""
    
    scene_number: int
    location_type: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    shots: List[Shot] = Field(default_factory=list)


class TimePeriod(BaseModel):
    """Time period for an epoch."""
    
    start: Optional[int] = None
    end: Optional[int] = None


class Epoch(BaseModel):
    """Epoch information containing multiple scenes."""
    
    epoch_number: int
    time_period: TimePeriod
    scenes: List[Scene] = Field(default_factory=list)
class Project(BaseModel):
    """Project information."""
    
    title: str
    total_shots: int
    epochs: List[Epoch] = Field(default_factory=list)


class ShotList(BaseModel):
    """Complete shot list structure."""
    
    project: Project