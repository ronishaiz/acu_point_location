import glob
import os.path

PICTURES_PATH = os.path.join(os.path.dirname(__file__), 'pictures')
ALL_PICTURES = glob.glob(os.path.join(PICTURES_PATH, '*', '*.png'))

POINT_TO_PICTURE_PATH = {
    os.path.basename(picture_path).replace('.png', ''): picture_path for picture_path in ALL_PICTURES
}

QUESTION_STR = "Enter the correct point name"

AREAS = os.listdir(PICTURES_PATH)
BY_AREA = {
    area: [point for point, path in POINT_TO_PICTURE_PATH.items() if os.path.basename(os.path.dirname(path)) == area] for area in AREAS
}

EXISTING_MERIDIANS = set([''.join((c for c in point if not c.isdigit())) for point in POINT_TO_PICTURE_PATH])

BY_MERIDIAN = {
    meridian_name:
        [point
         for point in POINT_TO_PICTURE_PATH if point.startswith(meridian_name)] for meridian_name in EXISTING_MERIDIANS
}
