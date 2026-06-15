from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    year = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    image_url = Column(String(500), default="")
    source = Column(String(300), default="")
    status = Column(String(20), default="approved")
    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    building = relationship("Building", back_populates="timeline_events")
    submitter = relationship("User", foreign_keys=[submitted_by])


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(255), default="")
    bio = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    buildings = relationship("Building", back_populates="owner")
    comments = relationship("Comment", back_populates="user")
    routes = relationship("ExplorationRoute", back_populates="user")


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    history = Column(Text, default="")
    construction_year = Column(Integer)
    abandonment_year = Column(Integer)
    building_type = Column(String(50), default="工厂")
    address = Column(String(300), default="")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    danger_level = Column(Integer, default=1)
    explore_count = Column(Integer, default=0)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="buildings")
    photos = relationship("Photo", back_populates="building", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="building", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="building", cascade="all, delete-orphan")
    hazards = relationship("SafetyHazard", back_populates="building", cascade="all, delete-orphan")
    tags = relationship("BuildingTag", back_populates="building", cascade="all, delete-orphan")
    timeline_events = relationship("TimelineEvent", back_populates="building", cascade="all, delete-orphan", order_by="TimelineEvent.year")


class BuildingTag(Base):
    __tablename__ = "building_tags"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    tag = Column(String(50), nullable=False)

    building = relationship("Building", back_populates="tags")


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    url = Column(String(500), nullable=False)
    caption = Column(String(300), default="")
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    building = relationship("Building", back_populates="photos")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    url = Column(String(500), nullable=False)
    title = Column(String(200), default="")
    description = Column(Text, default="")
    duration = Column(Integer, default=0)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    building = relationship("Building", back_populates="videos")


class SafetyHazard(Base):
    __tablename__ = "safety_hazards"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    hazard_type = Column(String(50), nullable=False)
    description = Column(Text, default="")
    severity = Column(Integer, default=2)
    location = Column(String(200), default="")

    building = relationship("Building", back_populates="hazards")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    rating = Column(Integer, default=0)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    likes = Column(Integer, default=0)

    building = relationship("Building", back_populates="comments")
    user = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent")


class ExplorationRoute(Base):
    __tablename__ = "exploration_routes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    duration_minutes = Column(Integer, default=0)
    difficulty = Column(Integer, default=2)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="routes")
    points = relationship("RoutePoint", back_populates="route", cascade="all, delete-orphan", order_by="RoutePoint.order_index")


class RoutePoint(Base):
    __tablename__ = "route_points"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("exploration_routes.id"))
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=True)
    order_index = Column(Integer, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(String(300), default="")

    route = relationship("ExplorationRoute", back_populates="points")
