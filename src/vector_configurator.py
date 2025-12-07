from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class VectorConfiguration:
    """Represents a configurable numeric vector."""

    name: str
    components: List[float] = field(default_factory=list)

    @property
    def dimensions(self) -> int:
        return len(self.components)

    def update_component(self, index: int, value: float) -> None:
        if index < 0 or index >= self.dimensions:
            raise IndexError(f"Index {index} is outside the vector bounds (0-{self.dimensions - 1}).")
        self.components[index] = value

    def magnitude(self) -> float:
        return math.sqrt(sum(component ** 2 for component in self.components))

    def normalize(self) -> "VectorConfiguration":
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero-length vector.")
        normalized_components = [component / mag for component in self.components]
        return VectorConfiguration(name=f"{self.name}-normalized", components=normalized_components)

    def to_dict(self) -> dict:
        return {"name": self.name, "components": self.components}

    @classmethod
    def from_dict(cls, payload: dict) -> "VectorConfiguration":
        name = payload.get("name", "Unnamed Vector")
        components = payload.get("components", [])
        if not isinstance(components, list):
            raise ValueError("components must be a list of numbers")
        return cls(name=name, components=[float(value) for value in components])

    @classmethod
    def from_file(cls, path: Path) -> "VectorConfiguration":
        data = json.loads(path.read_text())
        return cls.from_dict(data)

    def to_file(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2))


def init_command(args: argparse.Namespace) -> None:
    components = [0.0] * args.dimensions
    config = VectorConfiguration(name=args.name, components=components)
    config.to_file(Path(args.output))
    print(f"Created vector '{config.name}' with {config.dimensions} dimensions at {args.output}")


def update_command(args: argparse.Namespace) -> None:
    config_path = Path(args.config)
    config = VectorConfiguration.from_file(config_path)
    config.update_component(args.index, args.value)
    config.to_file(config_path)
    print(f"Updated component {args.index} to {args.value} in {config_path}")


def info_command(args: argparse.Namespace) -> None:
    config = VectorConfiguration.from_file(Path(args.config))
    print(f"Name: {config.name}")
    print(f"Dimensions: {config.dimensions}")
    print(f"Components: {config.components}")
    print(f"Magnitude: {config.magnitude():.4f}")


def normalize_command(args: argparse.Namespace) -> None:
    config_path = Path(args.config)
    config = VectorConfiguration.from_file(config_path)
    normalized = config.normalize()
    output_path = Path(args.output)
    normalized.to_file(output_path)
    print(f"Wrote normalized vector to {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Configure and inspect numeric vectors.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a new vector configuration")
    init_parser.add_argument("name", help="Name of the vector")
    init_parser.add_argument("dimensions", type=int, help="Number of dimensions")
    init_parser.add_argument("output", help="Where to save the configuration")
    init_parser.set_defaults(func=init_command)

    update_parser = subparsers.add_parser("update", help="Update a specific vector component")
    update_parser.add_argument("config", help="Path to the vector configuration file")
    update_parser.add_argument("index", type=int, help="Index of the component to update")
    update_parser.add_argument("value", type=float, help="New value for the component")
    update_parser.set_defaults(func=update_command)

    info_parser = subparsers.add_parser("info", help="Display configuration details")
    info_parser.add_argument("config", help="Path to the vector configuration file")
    info_parser.set_defaults(func=info_command)

    normalize_parser = subparsers.add_parser("normalize", help="Normalize the vector and save to a new file")
    normalize_parser.add_argument("config", help="Path to the vector configuration file")
    normalize_parser.add_argument("output", help="Path to write the normalized configuration")
    normalize_parser.set_defaults(func=normalize_command)

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
