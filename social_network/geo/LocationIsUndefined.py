class LocationIsUndefined(Exception):
    def __init__(self):
        super().__init__('Location is undefined.')
