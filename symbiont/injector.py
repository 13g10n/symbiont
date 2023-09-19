import inspect
from typing import MutableMapping, Type, Union

from .components import Module, Component, Injectable


class DependencyInjector:
    """Dependency injector."""

    _components: MutableMapping[Type["Component"], "Component"]

    def __init__(self):
        self._components = {}

    def get_component(self, component_type: Union[Type["Component"], str]) -> Component:
        if isinstance(component_type, str):
            return next(iter(self._components[x] for x in self._components if x.__name__ == component_type))
        return self._components[component_type]

    def initialize(self, module_type: Type[Module]) -> Module:
        return self.initialize_module(module_type)

    def initialize_component(self, component_type: Type["Component"]) -> "Component":
        obj = component_type.__new__(component_type)

        self._inject_dependencies(obj)
        obj.__init__()

        return obj

    def initialize_module(self, module_type: Type["Module"]) -> "Module":
        module_type.children = []

        obj = module_type.__new__(module_type)

        for submodule_type in (*module_type.meta.imports, *module_type.meta.providers):
            submodule_type.parent = obj
            if issubclass(submodule_type, Module):
                submodule = self.initialize_module(submodule_type)
            else:
                submodule = self.initialize_component(submodule_type)
            module_type.children.append(submodule)
            self._components[submodule_type] = submodule

        self._inject_dependencies(obj)

        obj.__init__()
        return obj

    def _inject_dependencies(self, instance):
        for key, annotation in instance.__class__.__annotations__.items():
            if isinstance(annotation, type) and issubclass(annotation, Component):
                if target := self._components.get(annotation):
                    setattr(instance, key, target)
                else:
                    print(
                        f'"{key}" of type "{annotation.__name__}" is not ' f'found for "{instance.__class__.__name__}"!'
                    )

    def inject(self, fn):
        deps = {
            key: param.annotation
            for key, param in inspect.signature(fn).parameters.items()
            if issubclass(param.annotation, Injectable)
        }

        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs, **{k: self.get_component(v) for k, v in deps.items()})

        return wrapper
