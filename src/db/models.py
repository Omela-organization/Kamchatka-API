from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Text, Float, Boolean, JSON, Date
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# base model
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role = relationship(
        "Role",
        back_populates="users"
    )
    created_eco_problems = relationship(
        'EcoProblem',
        foreign_keys='EcoProblem.creator_id',
        back_populates='creator',
        cascade="all, delete-orphan"
    )
    administered_eco_problems = relationship(
        'EcoProblem',
        foreign_keys='EcoProblem.administrator_id',
        back_populates='administrator',
        cascade="all, delete-orphan"
    )
    created_applications = relationship(
        'Application',
        foreign_keys='Application.creator_id',
        back_populates='creator',
        cascade="all, delete-orphan"
    )
    administered_applications = relationship(
        'Application',
        foreign_keys='Application.administrator_id',
        back_populates='administrator',
        cascade="all, delete-orphan"
    )
    created_feedbacks = relationship(
        "Feedback",
        foreign_keys='Feedback.creator_id',
        back_populates='creator',
        cascade="all, delete-orphan"
    )


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship(
        "User",
        back_populates="role",
        cascade="all, delete-orphan"
    )


class EcoProblem(Base):
    __tablename__ = 'eco_problems'

    id = Column(Integer, primary_key=True, index=True)
    territory_id = Column(Integer, ForeignKey('territories.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    administrator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status_id = Column(Integer, ForeignKey('statuses.id'), nullable=False)
    type_incident_id = Column(Integer, ForeignKey('type_incidents.id'), nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    classified_type = Column(JSON, nullable=True)
    is_classified = Column(Boolean, default=False)
    location = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # relationships
    territory = relationship("Territory", back_populates="eco_problems")
    track = relationship("Track", back_populates="eco_problems")
    creator = relationship("User", foreign_keys=[creator_id], back_populates='created_eco_problems')
    administrator = relationship("User", foreign_keys=[administrator_id], back_populates="administered_eco_problems")
    status = relationship("Status", back_populates="eco_problems")
    type_incident = relationship("TypeIncident", back_populates="eco_problems")
    photos = relationship('Photo', back_populates='eco_problems', cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="eco_problems", cascade="all, delete-orphan")


class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    eco_problems = relationship("EcoProblem", back_populates="status", cascade="all, delete-orphan")


class TypeIncident(Base):
    __tablename__ = 'type_incidents'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    eco_problems = relationship("EcoProblem", back_populates="type_incident", cascade="all, delete-orphan")


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    eco_id = Column(Integer, ForeignKey('eco_problems.id'))
    filename = Column(String, nullable=False)
    path_to_photo = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    eco_problems = relationship("EcoProblem", back_populates="photos")


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    eco_id = Column(Integer, ForeignKey('eco_problems.id'))
    filename = Column(String, nullable=False)
    path_to_file = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    eco_problems = relationship("EcoProblem", back_populates="documents")


class Territory(Base):
    __tablename__ = 'territories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)

    eco_problems = relationship("EcoProblem", back_populates="territory", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="territory", cascade="all, delete-orphan")
    tracks = relationship("Track", back_populates="territory", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="territory", cascade="all, delete-orphan")


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    length = Column(Float, nullable=True)
    time_passing_track = Column(Float, nullable=True)
    type_track = Column(String, nullable=True)
    basic_recreational_capacity = Column(Integer, nullable=True)
    territory_id = Column(Integer, ForeignKey('territories.id'))
    data = Column(JSON, nullable=True)

    territory = relationship("Territory", back_populates="tracks")
    eco_problems = relationship("EcoProblem", back_populates="track", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="track", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="track", cascade="all, delete-orphan")


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, index=True)
    territory_id = Column(Integer, ForeignKey('territories.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rate_painting = Column(Integer, nullable=True)
    rate_facilities = Column(Integer, nullable=True)
    rate_purity = Column(Integer, nullable=True)
    rate_expectations = Column(Integer, nullable=True)

    territory = relationship("Territory", back_populates="feedbacks")
    track = relationship("Track", back_populates="feedbacks")
    creator = relationship("User", back_populates='created_feedbacks')


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    territory_id = Column(Integer, ForeignKey('territories.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    administrator_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    car_plate = Column(String, nullable=True)
    is_permitted = Column(Boolean, default=False)
    purpose_visit = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    visitors = Column(JSON, nullable=True)

    territory = relationship("Territory", back_populates="applications")
    track = relationship("Track", back_populates="applications")
    creator = relationship("User", foreign_keys=[creator_id], back_populates='created_applications')
    administrator = relationship("User", foreign_keys=[administrator_id], back_populates="administered_applications")


class EcoMonitoring(Base):
    __tablename__ = 'eco_monitorings'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    type_data = Column(String, nullable=False)
    territory_id = Column(Integer, ForeignKey('territories.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    data = Column(JSON, nullable=False)
    params = Column(JSON, nullable=True)
