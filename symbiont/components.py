import dataclasses
from typing import Type, List


@dataclasses.dataclass
class _ModuleMeta:
    imports: List[Type["Module"]] = dataclasses.field(default_factory=list)
    providers: List[Type["Injectable"]] = dataclasses.field(default_factory=list)


class Component:
    parent: "Component"


class Injectable(Component):
    """Injectable interface."""


class Module(Component):
    meta: _ModuleMeta
    children: List[Component]

    def __init_subclass__(
        cls,
        imports: List[Type["Module"]] = None,
        providers: List[Type["Injectable"]] = None,
    ) -> None:
        super().__init_subclass__()
        cls.meta = _ModuleMeta(imports=imports or [], providers=providers or [])
