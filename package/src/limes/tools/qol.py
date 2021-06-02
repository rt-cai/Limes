def Switch(arg, options, default):
    if arg in options.keys():
        return options[arg]()
    else:
        return default()