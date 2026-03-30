
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Clients(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )
    name: str
    phone: str
    background_color: str    
    foreground_color: str    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

class Hotspots(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )
    name: str
    client_id: UUID = Field(
        foreign_key="clients.id", 
        index=True        
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

class Media(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )
    type: str
    source: str
    client_id: UUID = Field(
        foreign_key="clients.id", 
        index=True        
    )
    hotspot_id: UUID = Field(
        foreign_key="hotspots.id", 
        index=True        
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

class Subscribers(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )
    phone: str = Field(
        index=True
    )
    session_hour: datetime  
    user_id: int = Field(
        index=True,
        nullable=False
    )
    #CREATE SEQUENCE IF NOT EXISTS subscribers_user_id_seq;
    client_id: UUID = Field(
        foreign_key="clients.id", 
        index=True        
    )
    hotspot_id: UUID = Field(
        foreign_key="hotspots.id", 
        index=True        
    )   
    device: str 
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
           
class System_Users(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )
    name: str
    phone: str = Field(
        unique=True, 
        index=True
    )
    password: str    
    client_id: UUID = Field(
        foreign_key="clients.id", 
        index=True        
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )