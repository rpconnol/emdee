def Bounds(p=None):

    bounds_dict = {
    "core_mass": [1.4,2.0],
    "core_radius": [8.0,13.0],
    "Qimp": [0.0,40.0],
    "core_temperature": [1e6,1e7],
    "Mdot": [1e16,1e18],
    "Q_shallow_heating": [0.0,5.0]
    }

    # if no argument is provided, just prints a list of the default bounds
    if p == None:
        print(bounds_dict)
        return

    if p in bounds_dict:
        return bounds_dict.get(p)
    else:
        print("No default bounds for "+p+", SET MANUALLY BEFORE RUNNING!")
        return [0,0]


def Format(p):

    format_dict = {
    "core_mass": "{:.2f}",
    "core_radius": "{:.2f}",
    "Qimp": "{:.1f}",
    "core_temperature": "{:.2e}",
    "Mdot": "{:.1e}",
    "Q_shallow_heating": "{:.2f}"
    }

    # if param is not in format_dict, returns {} as a default format
    return format_dict.get(p,"{}")