# Pattern used to validate input before calling eval().
# Allowed chars: 0-9, *, /, +, -, space, (, ), and ^.
PATTERN_CALC_VALIDATION = r"^[0-9+\-*\/^\(\)\. ]+$"

# URL use to fetch jokes
URL_JOKES = "https://vysmatej.cz/nahodne-vtipy/"