from enum import Enum

class VisibilityEnum(Enum):
    private = "private"
    public = "public"

class RoleEnum(Enum):
    admin = "admin"
    buyer = "buyer"
    provider = "provider"

class StatusEnum(Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"