from jproperties import Properties as pr


def get(side, attribute):
    configs = pr()
    with open(f'../{side}/configs.properties', 'rb') as file:
        configs.load(file)

    return configs.get(attribute).data

