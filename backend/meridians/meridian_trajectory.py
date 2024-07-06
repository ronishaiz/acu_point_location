import os.path
from dataclasses import dataclass
from typing import List

import toml

from backend.enums import MeridianName
from PIL import Image


trajectories_folder = os.path.join(os.path.dirname(__file__), 'data', 'trajectories')


@dataclass
class MeridianPath:
    inner: bool
    index: int

    sections: List[str]

    @classmethod
    def from_dict(cls, index: int, d: dict) -> 'MeridianPath':
        return cls(inner=d['inner'], index=index, sections=d['sections'])

    @property
    def str_rep(self) -> str:
        inner_outer = "Inner" if self.inner else "Outer"
        sections = " -> ".join(self.sections)

        return f"{inner_outer} Path {self.index}:\n{sections}"


@dataclass
class MeridianTrajectory:

    meridian_name: MeridianName
    paths: List[MeridianPath]
    _image: Image = None

    @property
    def image(self) -> Image:
        if not self._image:
            self._image = Image.open(os.path.join(trajectories_folder, 'images', self.meridian_name.value + '.png'))

        return self._image

    @property
    def str_rep(self) -> str:
        return "\n\n".join([path.str_rep for path in self.paths])

    @classmethod
    def from_dict(cls, d: dict, meridian_name: MeridianName) -> 'MeridianTrajectory':
        return cls(paths=[MeridianPath.from_dict(int(index), path) for index, path in d.items()], meridian_name=meridian_name)

    @classmethod
    def from_toml(cls, meridian_name: MeridianName) -> 'MeridianTrajectory':
        toml_file_path = os.path.join(trajectories_folder, 'descriptions', meridian_name.value + '.toml')

        with open(toml_file_path, 'r') as f:
            trajectory_dict = toml.load(f)

        return cls.from_dict(trajectory_dict, meridian_name)
