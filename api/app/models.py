from datetime import datetime, timezone

from .extensions import db


class ComponentType(db.Model):
    __tablename__ = "component_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)

    components = db.relationship(
        "HardwareComponent",
        back_populates="component_type"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class HardwareComponent(db.Model):
    __tablename__ = "hardware_components"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    manufacturer = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), unique=True, nullable=False)
    power_consumption_w = db.Column(db.Integer)
    release_year = db.Column(db.Integer)

    component_type_id = db.Column(
        db.Integer,
        db.ForeignKey("component_types.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    component_type = db.relationship(
        "ComponentType",
        back_populates="components"
    )

    specifications = db.relationship(
        "Specification",
        back_populates="component",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "power_consumption_w": self.power_consumption_w,
            "release_year": self.release_year,
            "component_type": self.component_type.to_dict(),
            "specifications": [
                specification.to_dict()
                for specification in self.specifications
            ],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Specification(db.Model):
    __tablename__ = "specifications"

    id = db.Column(db.Integer, primary_key=True)
    attribute_name = db.Column(db.String(100), nullable=False)
    attribute_value = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(40))

    component_id = db.Column(
        db.Integer,
        db.ForeignKey("hardware_components.id"),
        nullable=False
    )

    component = db.relationship(
        "HardwareComponent",
        back_populates="specifications"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "attribute_name": self.attribute_name,
            "attribute_value": self.attribute_value,
            "unit": self.unit
        }
