from typing import List

from .color_mixing_method import ColorMixingMethodDirect, ColorMixingMethodDarken, ColorMixingMethod


class ColorMixingMethodsRegister:

    methods = [ColorMixingMethodDirect(),
               ColorMixingMethodDarken()]

    @property
    def names(self) -> List[str]:
        return [x.name() for x in self.methods]

    def get_by_name(self, name: str) -> ColorMixingMethod:
        for method in self.methods:
            if method.name() == name:
                return method
