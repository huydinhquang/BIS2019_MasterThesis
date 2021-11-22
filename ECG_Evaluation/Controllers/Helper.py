def switch_format_desc(value):
    value = value.lower()
    switcher = {
        1: "WFDB",
        2: "SciPy",
    }
    return switcher.get(value, "Invalid format descriptor")