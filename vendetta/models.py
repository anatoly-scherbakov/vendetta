from typing import Callable, Dict, List, Optional, Union

from pydantic import BaseModel, Field

Row = Dict[str, str]

# Naively generate a random value
NaiveFake = Callable[[], str]

# Generate a random value cached based on original value
ResponsibleFake = Callable[[str], str]


class FakerConfig(BaseModel):
    """Faker configuration."""

    locale: Optional[Union[str, List[str]]] = None
    providers: Optional[List[str]] = None


class Config(BaseModel):
    """Configuration file."""

    faker: FakerConfig = Field(default_factory=FakerConfig)
    columns: Dict[str, str] = Field(default_factory=dict)
