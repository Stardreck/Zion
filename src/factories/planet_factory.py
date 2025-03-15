from typing import Dict, Any

from src.models.planet import Planet


class PlanetFactory:
    @staticmethod
    def create_planet(planet_data: Dict[str, Any]) -> Planet:
        return Planet(
            name=planet_data["name"],
            description=planet_data["description"],
            row=planet_data["row"],
            col=planet_data["col"],
            visited=planet_data.get("visited", False),
            is_fuel_planet=planet_data.get("isFuelPlanet", False),
            is_start_planet=planet_data.get("isStartPlanet", False),
            is_end_planet=planet_data.get("isEndPlanet", False),
            is_spacestation=planet_data.get("IsSpacestation", False),
            depend_on=planet_data.get("depend_on", None),
            background_image=planet_data.get("background_image"),
            planet_image=planet_data.get("planet_image"),
            cutscene_media=planet_data.get("cutscene", None),
            wormhole_cutscene_media=planet_data.get("wormhole_cutscene", None),
        )
