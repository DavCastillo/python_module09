from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    RADIO = 'radio'
    VISUAL = 'visual'
    PHYSICAL = 'physical'
    TELEPATHIC = 'telepathic'


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field()
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType = Field()
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def chk_alien_contact(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact id must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL:
            if not self.is_verified:
                raise ValueError("Physical contact reports must be verified")
        if self.contact_type == ContactType.TELEPATHIC:
            if not self.witness_count >= 3:
                raise ValueError("Telepathic contact requires at "
                                 "least 3 witnesses")
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals (> 7.0) should "
                             "include received messages")
        return self


def main() -> None:
    cntc_rp = AlienContact(
        contact_id='AC_2024_001',
        timestamp=datetime(2024, 10, 31),
        location='Area 51, Nevada',
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="'Greetings from Zeta Reticuli'"
    )
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print("ID:", cntc_rp.contact_id)
    print("Type:", cntc_rp.contact_type.value)
    print("Location:", cntc_rp.location)
    print(f"Signal: {cntc_rp.signal_strength}/10")
    print(f"Duration: {cntc_rp.duration_minutes} minutes")
    print("Witnesses:", cntc_rp.witness_count)
    print("Message:", cntc_rp.message_received)

    print("\n======================================")
    print("Expected validation error:")
    try:
        cntc_rp2 = AlienContact(
            contact_id='AC_2024_001',
            timestamp=datetime(2024, 10, 31),
            location='Area 51, Nevada',
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="'Greetings from Zeta Reticuli'"
        )
        print(cntc_rp2)
    except ValidationError as error:
        er = str(error.errors()[0].get('msg'))
        print(er.replace("Value error, ", ""))


if __name__ == "__main__":
    main()
