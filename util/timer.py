

def format_time(seconds):
    """Convert seconds to MM:SS format."""
    mins = seconds // 60
    secs = seconds % 60
    return "{:02d}:{:02d}".format(mins, secs)
