# Symbiont

![PyPI](https://img.shields.io/pypi/v/symbiont)
![GitHub](https://img.shields.io/github/license/13g10n/symbiont)
![Project status](https://img.shields.io/pypi/status/symbiont)
![PyPI - Downloads](https://img.shields.io/pypi/dm/symbiont?label=installs)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tiny module-service and dependency injection framework

## Installation

```bash
pip install symbiont
```

## Usage

```python
from symbiont import Module, Injectable, DependencyInjector


class BarService(Injectable):
    x: int = 42


class FooService(Injectable):
    bar: BarService


class ExampleModule(
    Module,
    providers=[BarService, FooService]
):
    foo: FooService


class RootModule(
    Module,
    imports=[ExampleModule]
):
    foo: FooService


injector = DependencyInjector()
root = injector.initialize(RootModule)


@injector.inject
def example_method(a, foo: FooService):
    ...

```
