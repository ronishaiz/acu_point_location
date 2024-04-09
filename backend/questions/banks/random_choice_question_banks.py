from backend.meridians.meridian import ALL_POINTS

Indications = {
    f"Which is the point with the following indications: {point.indications} ?": point.identifier for point in ALL_POINTS
}

Functions = {
    f"Which is the point with the following functions: {point.functions} ?": point.identifier for point in ALL_POINTS
}

Characters = {
    f"What are the characters of {point.identifier}?": point.characters for point in ALL_POINTS
}

Locations = {
    f"What is the location of {point.identifier}?": point.location for point in ALL_POINTS
}

Elements = {
    f"What is the element of {point.identifier}?": point.element for point in ALL_POINTS
}
