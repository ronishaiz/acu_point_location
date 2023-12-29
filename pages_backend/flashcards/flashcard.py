from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum

import streamlit as st


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

            if isinstance(attribute_value, Enum):
                attribute_value = str(attribute_value.value)

            st.write(f" #### {header_name}")

            if isinstance(attribute_value, list):

                for item in attribute_value:

                    if isinstance(item, Enum):
                        item = str(item.value)

                    st.write(item)

            else:
                st.write(attribute_value)
