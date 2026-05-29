from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
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
