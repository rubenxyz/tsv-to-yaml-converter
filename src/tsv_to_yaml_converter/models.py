"""Data models for TSV to YAML converter."""

from typing import List, Optional

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
    type: Optional[str] = None
    video_prompt: Optional[str] = None


class Location(BaseModel):
    """Location information for a scene."""

    type: Optional[str] = None
    location_name: Optional[str] = None


class Shot(BaseModel):
    """Individual shot information."""

    shot_number: int
    oref: Optional[str] = None
    camera_angle: Optional[str] = None
    specific_area: Optional[str] = None
    description: Optional[str] = None
    camera_movement: CameraMovement
    shot_timecode: ShotTimecode
    image_prompt: Optional[str] = None


class Scene(BaseModel):
    """Scene information containing multiple shots."""

    scene_number: int
    comment: Optional[str] = None
    period: Optional[str] = None
    season: Optional[str] = None
    weather: Optional[str] = None
    location: Location
    diurnal: Optional[str] = None
    light_source: Optional[str] = None
    shots: List[Shot] = Field(default_factory=list)


class TimePeriod(BaseModel):
    """Time period for a phase."""

    start: Optional[int] = None
    end: Optional[int] = None


class Phase(BaseModel):
    """Phase information containing multiple scenes."""

    phase_number: int
    time_period: TimePeriod
    scenes: List[Scene] = Field(default_factory=list)


class Project(BaseModel):
    """Project information."""

    title: str
    total_shots: int
    phases: List[Phase] = Field(default_factory=list)
