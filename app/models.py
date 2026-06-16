from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Float, Integer, JSON, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String(512), nullable=True, default=None
    )
    gpx_oss_url: Mapped[str] = mapped_column(
        String(1024), nullable=False
    )
    distance: Mapped[float] = mapped_column(nullable=False, default=0.0)
    elevation_gain: Mapped[float] = mapped_column(nullable=False, default=0.0)
    track_points: Mapped[int] = mapped_column(nullable=False, default=0)
    source: Mapped[str] = mapped_column(
        String(32), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(512), nullable=True, default=None
    )
    nickname: Mapped[str] = mapped_column(
        String(64), nullable=False, default=""
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class ActivityRecord(Base):
    """骑行活动记录 (FIT 文件上传)。"""

    __tablename__ = "activity_records"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False
    )
    fit_oss_url: Mapped[str] = mapped_column(
        String(1024), nullable=False
    )
    distance: Mapped[float] = mapped_column(nullable=False, default=0.0)
    duration: Mapped[float] = mapped_column(nullable=False, default=0.0)
    elevation_gain: Mapped[float] = mapped_column(nullable=False, default=0.0)
    avg_speed: Mapped[float] = mapped_column(nullable=True, default=None)
    avg_hr: Mapped[float] = mapped_column(nullable=True, default=None)
    avg_power: Mapped[float | None] = mapped_column(nullable=True, default=None)
    avg_cadence: Mapped[float | None] = mapped_column(nullable=True, default=None)
    max_hr: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    max_power: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    np: Mapped[float | None] = mapped_column(nullable=True, default=None)
    tss: Mapped[float | None] = mapped_column(nullable=True, default=None)
    if_score: Mapped[float | None] = mapped_column(nullable=True, default=None)
    power_curve: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=None)
    hr_zones: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=None)
    track_data_oss_url: Mapped[str | None] = mapped_column(String(1024), nullable=True, default=None)
    device_info: Mapped[str | None] = mapped_column(String(128), nullable=True, default=None)
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None)
    track_points: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )


class FitnessProfile(Base):
    """用户骑行体能档案。"""

    __tablename__ = "fitness_profiles"

    user_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )
    ftp: Mapped[float | None] = mapped_column(nullable=True, default=None)
    ftp_wkg: Mapped[float | None] = mapped_column(nullable=True, default=None)
    ftp_confidence: Mapped[float] = mapped_column(default=0.0)
    fitness_level: Mapped[str] = mapped_column(
        String(16), nullable=False, default="beginner"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
