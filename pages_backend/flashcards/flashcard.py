from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

import streamlit as st
from PIL.Image import Image

from pages_backend.utils import format_displayable_object


@dataclass
class FlashCardObject(metaclass=ABCMeta):

    @property
    @abstractmethod
    def identifier(self):
        return NotImplementedError()

    @classmethod
    @abstractmethod
    def get_property_name_to_flash_card_property_name(cls) -> dict:
        pass


class FlashCard:

    def __init__(self, flash_card_object: FlashCardObject):
        self.object = flash_card_object

    def show_identifier(self):
        st.write(f"# {self.object.identifier}")

    def show_content(self):
        st.write(f"# {self.object.identifier}")

        for property_name, header_name in self.object.get_property_name_to_flash_card_property_name().items():
            attribute_value = self.object.__getattribute__(property_name)

            if attribute_value is None:
                continue

            st.write(f" #### {header_name}")

            attribute_value = format_displayable_object(attribute_value)

            if isinstance(attribute_value, list):
                for item in attribute_value:
                    st.write(item)

            elif isinstance(attribute_value, Image):
                st.image(attribute_value)

            else:
                st.write(attribute_value)
