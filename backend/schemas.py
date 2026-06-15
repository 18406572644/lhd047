from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    avatar: str = ""
    bio: str = ""
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class BuildingTagBase(BaseModel):
    tag: str


class BuildingTagResponse(BuildingTagBase):
    id: int

    class Config:
        from_attributes = True


class PhotoBase(BaseModel):
    url: str
    caption: str = ""


class PhotoResponse(PhotoBase):
    id: int
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class VideoBase(BaseModel):
    url: str
    title: str = ""
    description: str = ""


class VideoResponse(VideoBase):
    id: int
    uploaded_by: int
    duration: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class SafetyHazardBase(BaseModel):
    hazard_type: str
    description: str = ""
    severity: int = 2
    location: str = ""


class SafetyHazardResponse(SafetyHazardBase):
    id: int

    class Config:
        from_attributes = True


class BuildingBase(BaseModel):
    title: str
    description: str = ""
    history: str = ""
    construction_year: Optional[int] = None
    abandonment_year: Optional[int] = None
    building_type: str = "工厂"
    address: str = ""
    latitude: float
    longitude: float
    danger_level: int = 1


class BuildingCreate(BuildingBase):
    tags: List[str] = []


class BuildingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    history: Optional[str] = None
    construction_year: Optional[int] = None
    abandonment_year: Optional[int] = None
    building_type: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    danger_level: Optional[int] = None


class BuildingResponse(BuildingBase):
    id: int
    explore_count: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    owner: Optional[UserResponse] = None
    tags: List[BuildingTagResponse] = []
    photos: List[PhotoResponse] = []
    videos: List[VideoResponse] = []
    hazards: List[SafetyHazardResponse] = []

    class Config:
        from_attributes = True


class BuildingListResponse(BaseModel):
    id: int
    title: str
    description: str
    building_type: str
    address: str
    latitude: float
    longitude: float
    danger_level: int
    explore_count: int
    status: str
    created_at: datetime
    tags: List[BuildingTagResponse] = []
    photos: List[PhotoResponse] = []

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    content: str
    rating: int = 0
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    building_id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    likes: int
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


class RoutePointBase(BaseModel):
    building_id: Optional[int] = None
    order_index: int = 0
    latitude: float
    longitude: float
    description: str = ""


class RoutePointResponse(RoutePointBase):
    id: int

    class Config:
        from_attributes = True


class ExplorationRouteBase(BaseModel):
    title: str
    description: str = ""
    duration_minutes: int = 0
    difficulty: int = 2
    is_public: bool = True


class ExplorationRouteCreate(ExplorationRouteBase):
    points: List[RoutePointBase] = []


class ExplorationRouteResponse(ExplorationRouteBase):
    id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    points: List[RoutePointResponse] = []

    class Config:
        from_attributes = True


class BuildingListWithPagination(BaseModel):
    items: List[BuildingListResponse]
    total: int
    page: int
    page_size: int


class StatisticsResponse(BaseModel):
    total_buildings: int
    total_users: int
    total_comments: int
    total_photos: int
    buildings_by_type: dict
    buildings_by_danger_level: dict
    top_explored: List[BuildingListResponse]


class TimelineEventBase(BaseModel):
    year: int
    title: str
    description: str = ""
    image_url: str = ""
    source: str = ""


class TimelineEventCreate(TimelineEventBase):
    pass


class TimelineEventUpdate(BaseModel):
    year: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    source: Optional[str] = None


class TimelineEventResponse(TimelineEventBase):
    id: int
    building_id: int
    status: str
    submitted_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
