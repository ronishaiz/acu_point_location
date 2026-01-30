import streamlit as st

from backend.enums import MeridianName, Organ
from backend.herbs.herb import ALL_HERBS, get_herb_group_options, filter_herbs_by_groups
from backend.meridians.meridian import ALL_POINTS, ALL_MERIDIANS, get_meridian_by_name
from backend.syndromes.syndrome import ALL_SYNDROMES
from pages_backend.flashcards.flashcard import FlashCard
from pages_backend.utils import Queue


def restack(sort: bool = False):
    if 'stack' in st.session_state:
        st.session_state.pop('stack')

    st.session_state['sort'] = sort


def show_flashcards(flashcard_topic):
    stack = st.session_state['stack']

    hide_content = st.checkbox('Hide Content', value=True, key='hide_flashcard_content')
    
    # Add option to show only location for Point flashcards
    show_only_location = False
    if flashcard_topic == 'Points':
        show_only_location = st.checkbox('Show Only Location', value=False, key='show_only_location')
    
    # Check if we need to jump to a point
    if 'jump_to_point' in st.session_state and st.session_state['jump_to_point']:
        point = st.session_state['jump_to_point']
        # Find the point in the current stack and navigate to it
        flashcards = st.session_state.get('all_flashcards', [])
        for i, flashcard in enumerate(flashcards):
            if hasattr(flashcard.object, 'identifier') and flashcard.object.identifier == point.identifier:
                # Navigate to this flashcard
                while stack.get_top() != flashcard:
                    stack.next()
                break
        st.session_state.pop('jump_to_point')
    
    # Check if we need to jump to a herb
    if 'jump_to_herb' in st.session_state and st.session_state['jump_to_herb']:
        herb = st.session_state['jump_to_herb']
        # Find the herb in the current stack and navigate to it
        flashcards = st.session_state.get('all_flashcards', [])
        for i, flashcard in enumerate(flashcards):
            if hasattr(flashcard.object, 'name') and flashcard.object.name == herb.name:
                # Navigate to this flashcard
                while stack.get_top() != flashcard:
                    stack.next()
                break
        st.session_state.pop('jump_to_herb')
    
    def on_point_click(point):
        """Callback when a point is clicked in a syndrome flashcard."""
        st.session_state['jump_to_point'] = point
        # Switch to Points topic
        st.session_state['flashcard_topic'] = 'Points'
        # Determine which meridian the point belongs to
        from backend.meridians.meridian import get_meridian_by_name
        from backend.enums import MeridianName
        # Extract meridian name from point identifier (e.g., "LIV3" -> "LIV")
        meridian_name = ''.join([c for c in point.identifier if not c.isdigit()])
        try:
            meridian = get_meridian_by_name(MeridianName(meridian_name))
            st.session_state['meridian_selection'] = meridian_name
        except:
            st.session_state['meridian_selection'] = 'ALL'
        restack()
        st.rerun()
    
    def on_herb_click(herb):
        """Callback when a herb is clicked in a syndrome flashcard."""
        st.session_state['jump_to_herb'] = herb
        # Switch to Herbs topic
        st.session_state['flashcard_topic'] = 'Herbs'
        restack()
        st.rerun()
    
    # Determine property filter for Point flashcards
    property_filter = None
    if flashcard_topic == 'Points' and show_only_location:
        property_filter = ['location']
    
    show_flashcard(stack.get_top(), hide_content, 
                   on_herb_click if flashcard_topic == 'Syndromes' else None,
                   on_point_click if flashcard_topic == 'Syndromes' else None,
                   property_filter)

    st.button("Previous", on_click=lambda: stack.prev(), key="previous_flashcard")
    st.button("Next", on_click=lambda: stack.next(), key="next_flashcard")


def show_flashcard(flashcard: FlashCard, hide_content: bool, on_herb_click=None, on_point_click=None, property_filter=None):
    if hide_content:
        flashcard.show_identifier()
    else:
        flashcard.show_content(on_herb_click, on_point_click, property_filter)


st.set_page_config(
    page_title="Flash Cards",
    page_icon="📒",
)

# Get topic from session state or default
flashcard_topic = st.session_state.get('flashcard_topic', 'Points')
flashcard_topic = st.selectbox('Select Flashcards Topic', ['Points', 'Meridians', 'Syndromes', 'Herbs'], 
                               index=['Points', 'Meridians', 'Syndromes', 'Herbs'].index(flashcard_topic) if flashcard_topic in ['Points', 'Meridians', 'Syndromes', 'Herbs'] else 0,
                               on_change=restack)
st.session_state['flashcard_topic'] = flashcard_topic

if flashcard_topic == 'Points':
    # Get meridian selection from session state if available (for point navigation)
    default_meridian = st.session_state.get('meridian_selection', 'ALL')
    meridians = ['ALL'] + [meridian.name.value for meridian in ALL_MERIDIANS]
    meridian_selection = st.selectbox('Choose Meridian', meridians, 
                                      index=meridians.index(default_meridian) if default_meridian in meridians else 0,
                                      on_change=restack)
    st.session_state['meridian_selection'] = meridian_selection
    flashcard_objects = ALL_POINTS if meridian_selection == 'ALL' else get_meridian_by_name(MeridianName(meridian_selection)).points

elif flashcard_topic == 'Meridians':
    flashcard_objects = ALL_MERIDIANS

elif flashcard_topic == 'Syndromes':
    organ_selection = st.selectbox('Choose Organ', ['ALL'] + [organ.value for organ in Organ], on_change=restack)
    flashcard_objects = ALL_SYNDROMES if organ_selection == 'ALL' else [syndrome for syndrome in ALL_SYNDROMES if syndrome.organ == Organ(organ_selection)]

else:  # Herbs
    # Herb group selector (single selection). Options come from get_herb_group_options().
    herb_group_opts = get_herb_group_options()  # [{'label': ..., 'value': ...}, ...]
    option_labels = ['ALL'] + [opt['label'] for opt in herb_group_opts]
    default_group = st.session_state.get('herb_group_selection', 'ALL')
    herb_group_selection = st.selectbox(
        'Choose Herb Group',
        option_labels,
        index=option_labels.index(default_group) if default_group in option_labels else 0,
        on_change=restack
    )
    st.session_state['herb_group_selection'] = herb_group_selection

    if herb_group_selection == 'ALL':
        flashcard_objects = ALL_HERBS
    else:
        # find the enum value for the selected label and filter herbs by that value
        selected_value = next((opt['value'] for opt in herb_group_opts if opt['label'] == herb_group_selection), None)
        flashcard_objects = filter_herbs_by_groups([selected_value]) if selected_value else []

flashcards = [FlashCard(flashcard_object) for flashcard_object in flashcard_objects]
st.session_state['all_flashcards'] = flashcards

st.button('Shuffle', on_click=restack)
st.button('Sort', on_click=lambda: restack(True))

if 'stack' not in st.session_state:
    st.session_state['stack'] = Queue[FlashCard](flashcards, st.session_state.get('sort', False))

show_flashcards(flashcard_topic)
