from typing import Optional, cast
from pydantic import BaseModel, Field, field_validator, model_validator


class MazeConfig(BaseModel):
    """Validate the maze configuration."""

    width: int = Field(..., gt=0, alias="WIDTH")
    height: int = Field(..., gt=0, alias="HEIGHT")
    entry: tuple[int, int] = Field(..., alias="ENTRY")
    exit_: tuple[int, int] = Field(..., alias="EXIT")
    output_file: str = Field(..., min_length=1, alias="OUTPUT_FILE")
    perfect: bool = Field(..., alias="PERFECT")
    seed: Optional[int] = Field(None, alias="SEED")

    @field_validator("entry", "exit_", mode="before")
    @classmethod
    def validate_coord(cls, value: str) -> tuple[int, int]:
        coord = value.split(",")

        if len(coord) == 2:
            try:
                first = int(coord[0].strip().strip("\"'"))
                sec = int(coord[1].strip().strip("\"'"))
            except ValueError:
                raise ValueError("Coordinate must be in format: int, int.")
        else:
            raise ValueError("Coordinate must be in format: int, int.")

        return (first, sec)

    @model_validator(mode="after")
    def validate_limits(self) -> "MazeConfig":
        en_x, en_y = self.entry
        ex_x, ex_y = self.exit_

        if en_x < 0 or en_x >= self.width or en_y < 0 or en_y >= self.height:
            raise ValueError(f"Entry coordinates are outside of the maze "
                             f"limits: coordinates must be smaller "
                             f"that {self.height} and {self.width}.")

        if ex_x < 0 or ex_x >= self.width or ex_y < 0 or ex_y >= self.height: 
            raise ValueError(f"Exit coordinates are outside of the maze "
                             f"limits: coordinates must be smaller "
                             f"that {self.height} and {self.width}.")

        if en_x == ex_x and en_y == ex_y:
            raise ValueError("Entry and Exit coordinates must be different.")
        return self


def config_parser(filename: str) -> MazeConfig:
    """Read config.txt and create a validated MazeConfig."""

    data: dict[str, str] = {}

    with open(filename, "r") as file:
        for i, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Invalid configuration at line {i}: "
                                 "expected KEY=VALUE.")

            key, value = line.split("=", 1)

            key = key.strip().upper()
            value = value.strip().strip("\"'")

            if not key:
                raise ValueError(
                    f"Invalid configuration at line {i}: "
                    "empty key."
                )

            if key in data:
                raise ValueError(f"Duplicate configuration key '{key}'.")

            data[key] = value

    try:
        return MazeConfig(**cast(dict, data)) # casteo xq mypy no entiende que pydantic puede recibir el dict de str y sabe convertirlas a los tipos de datos que espera cada atributo del modelo
    except ValueError as e:
        raise ValueError(f"Invalid configuration: {e}") from e
