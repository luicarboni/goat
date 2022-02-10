from datetime import datetime
from typing import TYPE_CHECKING, Optional

from geoalchemy2 import Geometry
from sqlmodel import (
    JSON,
    Column,
    DateTime,
    Field,
    Float,
    ForeignKey,
    Index,
    Integer,
    Relationship,
    SQLModel,
    text,
)

if TYPE_CHECKING:
    from .building import Building, BuildingModified
    from .scenario import Scenario


class PopulationBase(SQLModel):
    id: int = Field(primary_key=True)
    population: Optional[float] = Field(sa_column=Column(Float(53)))
    geom: str = Field(
        sa_column=Column(
            Geometry(geometry_type="Point", srid="4326", spatial_index=False),
            nullable=False,
        )
    )


class Population(PopulationBase, table=True):
    __tablename__ = "population"
    __table_args__ = {"schema": "basic"}

    demography: Optional[str] = Field(sa_column=Column(JSON))
    building_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("basic.building.id", ondelete="CASCADE"), index=True),
    )
    building: Optional["Building"] = Relationship(back_populates="populations")


Index("idx_population_geom", Population.__table__.c.geom, postgresql_using="gist")


class PopulationModified(PopulationBase, table=True):
    __tablename__ = "population_modified"
    __table_args__ = {"schema": "customer"}

    creation_date: datetime = Field(
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )
    building_modified_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("customer.building_modified.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        ),
    )

    scenario_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            ForeignKey("customer.scenario.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        ),
    )
    building_modified: "BuildingModified" = Relationship(back_populates="populations_modified")
    scenario: Optional["Scenario"] = Relationship(back_populates="populations_modified")


Index("idx_population_modified_geom", PopulationModified.__table__.c.geom, postgresql_using="gist")