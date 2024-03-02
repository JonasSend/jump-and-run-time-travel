def fade_colour(rgb):
    """
    Fade an RGB color 25% closer to black.

    Parameters:
    - rgb: A tuple of (R, G, B) where each component is an integer in [0, 255].

    Returns:
    - A tuple of (R, G, B) representing the faded color.
    """
    faded_rgb = tuple(int(current_value - (current_value * 0.25)) for current_value in rgb)
    return faded_rgb
