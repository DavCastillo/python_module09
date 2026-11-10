from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field()
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    iss001 = SpaceStation(station_id='ISS001',
                          name='International Space Station',
                          crew_size=6, power_level=85.5,
                          oxygen_level=92.3,
                          last_maintenance=datetime.now(),
                          is_operational=True)
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    print("ID:", iss001.station_id)
    print("Name:", iss001.name)
    print("Crew:", iss001.crew_size, "people")
    print(f"Power: {iss001.power_level}%")
    print(f"Oxygen: {iss001.oxygen_level}%")
    print("Status: ", end='')
    if iss001.is_operational:
        print("Operational")
    else:
        print("Non operational")
    if iss001.notes:
        print("Notes:", iss001.notes)

    print("\n========================================")
    print("Expected validation error:")
    try:
        iss002 = SpaceStation(station_id='ISS002',
                              name=': International Space Station',
                              crew_size=36, power_level=85.5,
                              oxygen_level=92.3,
                              last_maintenance=datetime.now(),
                              is_operational=True)
        print(iss002)
    except ValidationError as error:
        print(error.errors()[0].get('msg'))


if __name__ == "__main__":
    main()
