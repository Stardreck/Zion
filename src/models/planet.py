class Planet:
    def __init__(self, name, description, row, col, visited=False, is_fuel_planet=False, is_start_planet=False,
                 is_end_planet=False,
                 background_image=None,
                 planet_image=None, cutscene_media=None):
        self.name = name
        self.description = description
        self.row = row
        self.col = col
        self.visited = visited
        self.is_fuel_planet = is_fuel_planet
        self.is_start_planet = is_start_planet
        self.is_end_planet = is_end_planet
        self.background_image = background_image
        self.planet_image = planet_image
        self.cutscene_media = cutscene_media
