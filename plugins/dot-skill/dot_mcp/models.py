"""Explicit MCP input models for the Dot. API tools."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class DotInputModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SettingsIntervalInput(DotInputModel):
    powerMs: int | None = Field(
        default=None,
        ge=60_000,
        le=43_200_000,
        multiple_of=60_000,
        description="Power refresh interval in milliseconds.",
    )
    batteryMs: int | None = Field(
        default=None,
        ge=60_000,
        le=43_200_000,
        multiple_of=60_000,
        description="Battery wake and refresh interval in milliseconds.",
    )

    @model_validator(mode="after")
    def require_interval_value(self) -> "SettingsIntervalInput":
        if self.powerMs is None and self.batteryMs is None:
            raise ValueError("interval must include powerMs or batteryMs")
        return self


class SettingsSleepInput(DotInputModel):
    enabled: bool
    start: str = Field(pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")
    end: str = Field(pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")


class DeviceSettingsInput(DotInputModel):
    alias: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=100)
    timezone: str | None = None
    interval: SettingsIntervalInput | None = None
    sleep: SettingsSleepInput | None = None

    @model_validator(mode="after")
    def require_setting_value(self) -> "DeviceSettingsInput":
        if not self.model_fields_set:
            raise ValueError("At least one device setting must be provided")
        return self


class TextStyleInput(DotInputModel):
    fontFamily: str | None = None
    fontSize: float | None = Field(default=None, ge=8, le=48)
    fontWeight: Literal[100, 200, 300, 400, 500, 600, 700, 800, 900] | None = None


class MessageTextStyleInput(TextStyleInput):
    lineHeight: float | None = Field(default=None, ge=0.8, le=3)


class TextStylesInput(DotInputModel):
    title: TextStyleInput | None = None
    message: MessageTextStyleInput | None = None
    signature: TextStyleInput | None = None


class TaskAliasInput(DotInputModel):
    taskAlias: str | int | None = None

    @field_validator("taskAlias")
    @classmethod
    def validate_task_alias(cls, value: str | int | None) -> str | int | None:
        if isinstance(value, str) and len(value) > 100:
            raise ValueError("taskAlias must be at most 100 characters")
        return value


class TextContentInput(TaskAliasInput):
    refreshNow: bool = True
    taskKey: str | None = None
    title: str | None = None
    message: str | None = None
    signature: str | None = None
    icon: str | None = None
    link: str | None = None
    styles: TextStylesInput | None = None


DitherType = Literal["DIFFUSION", "ORDERED", "NONE"]
DitherKernel = Literal[
    "THRESHOLD",
    "ATKINSON",
    "BURKES",
    "FLOYD_STEINBERG",
    "SIERRA2",
    "STUCKI",
    "JARVIS_JUDICE_NINKE",
    "DIFFUSION_ROW",
    "DIFFUSION_COLUMN",
    "DIFFUSION_2D",
]


class ImageContentInput(TaskAliasInput):
    image: str
    refreshNow: bool = True
    taskKey: str | None = None
    link: str | None = None
    border: Literal[0, 1] = 0
    ditherType: DitherType = "DIFFUSION"
    ditherKernel: DitherKernel = "FLOYD_STEINBERG"


class CanvasContentInput(TaskAliasInput):
    refreshNow: bool = True
    taskKey: str | None = None
    data: dict[str, Any] | None = None
    windowData: dict[str, Any]
    layoutFull: dict[str, Any] | None = None
    link: str | None = None
    border: Literal[0, 1] | None = None
