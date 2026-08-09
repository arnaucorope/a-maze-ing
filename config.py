from typing import Optional
from pydantic import BaseModel, Field, field_validator


class MazeConfig(BaseModel):
    """Validate """
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    entry: tuple[int, int] = Field(..., alias="ENTRY")
    exit_: tuple[int, int] = Field(..., alias="EXIT")
    output_file: str = Field(..., min_length=1)
    perfect: bool
    seed: Optional[int] = None

    @field_validator("entry", "exit_", mode="before")
    @classmethod
    def validate_coord(cls, value: str) -> tuple[int, int]:
        coord = value.split(",")
        if len(coord) == 2:
            try:
                first = int(coord[0].strip())
                sec = int(coord[1].strip())
            except ValueError:
                raise ValueError("Coordinate must be in format: int, int.")
        else:
            raise ValueError

        return (first, sec)


def config_parser(file: str) -> dict[str, str]:
    """Read the config.txt file and convert it in data that Pydantic can take
    for the MazeConfig Model"""

    data: dict[str, str] = {}

    with open(file, "r") as file:
        for i, line in file:
            if not line or line.startswith("#")
                continue

            if "=" not in line:
                raise ValueError(f"Invalid configuration at line {i}: "
                    "expected KEY=VALUE.")

            
            line = line.strip()
            key, value = line.split("=", 1) # 1 por si hay mas de un = por ejemplo en el nombre d eun file, que solo nos lo separe una vez y en el otro no haga split
            
            data[key.lower()] = value


    return MazeConfig(**data) # los ** desempaquetan el dict y es el equivalente a darle a pydantic el modelo escrito a mano y luego el model vallidator ira str por str del dict revisando todo y luego pydantic validara los fields
}