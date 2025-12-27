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

    def show_content(self, on_herb_click=None, on_point_click=None):
        st.write(f"# {self.object.identifier}")

        for property_name, header_name in self.object.get_property_name_to_flash_card_property_name().items():
            attribute_value = self.object.__getattribute__(property_name)

            if attribute_value is None:
                continue

            st.write(f" #### {header_name}")

            # Special handling for syndrome treatment with clickable points and herbs
            if property_name == 'treatment_str' and hasattr(self.object, '_treatment'):

                treatment = self.object._treatment
                if treatment.principle:
                    st.write(f"Principle: {treatment.principle}")

                if treatment.points:
                    st.write("Points:")
                    # Display points in a row using columns for better layout
                    cols = st.columns(min(len(treatment.points), 3))
                    for idx, point in enumerate(treatment.points):
                        with cols[idx % len(cols)]:
                            if isinstance(point, str):
                                st.text(point)
                            else:
                                if st.button(point.identifier, key=f"point_{point.identifier}_{id(self)}_{idx}"):
                                    if on_point_click:
                                        on_point_click(point)
                if treatment.nutrition:
                    st.write(f"Nutrition: {', '.join(treatment.nutrition)}")
                if treatment.herbs:
                    st.write("Herbs:")
                    # Display herbs in a row using columns for better layout
                    cols = st.columns(min(len(treatment.herbs), 3))
                    for idx, herb in enumerate(treatment.herbs):
                        with cols[idx % len(cols)]:
                            if isinstance(herb, str):
                                # Unrecognized herb - display as non-clickable text
                                st.text(herb)
                            else:
                                # Recognized herb - display as clickable button
                                if st.button(herb.name, key=f"herb_{herb.name}_{id(self)}_{idx}"):
                                    if on_herb_click:
                                        on_herb_click(herb)
                continue
            else:
                attribute_value = format_displayable_object(attribute_value)

                if isinstance(attribute_value, list):
                    for item in attribute_value:
                        st.write(item)

                elif isinstance(attribute_value, Image):
                    st.image(attribute_value)

                else:
                    st.write(attribute_value)
