"""Default field mappings for CLI commands."""

from typing import Dict


class CLIMappings:
    """Handles default field mappings for CLI commands."""

    @staticmethod
    def get_default_mappings() -> Dict[str, Dict[str, str]]:
        """Get default field mappings."""
        return {
            "DIURNAL": {
                "GH": "Golden Hour",
                "MH": "Magic Hour",
                "BH": "Blue Hour",
                "DAY": "Day",
                "NIGHT": "Night",
                "DAWN": "Dawn",
                "DUSK": "Dusk",
            },
            "LOC_TYPE": {
                "EXT": "Exterior",
                "INT": "Interior",
                "EXT/INT": "Exterior/Interior",
            },
            "MOVE_TYPE": {
                "STATIC": "Static",
                "PAN": "Pan",
                "TILT": "Tilt",
                "DOLLY": "Dolly",
                "CRANE": "Crane",
                "STEADICAM": "Steadicam",
                "HANDHELD": "Handheld",
                "AERIAL": "Aerial",
            },
            "MOVE_SPEED": {
                "SLOW": "Slow",
                "MEDIUM": "Medium",
                "FAST": "Fast",
                "VARIABLE": "Variable",
            },
            "ANGLE": {
                "WIDE": "Wide",
                "MEDIUM": "Medium",
                "CLOSE": "Close",
                "EXTREME_CLOSE": "Extreme Close",
                "EXTREME_WIDE": "Extreme Wide",
                "DUTCH": "Dutch",
                "HIGH": "High",
                "LOW": "Low",
                "BIRD_EYE": "Bird's Eye",
                "WORM_EYE": "Worm's Eye",
            },
            "PERIOD": {
                "ANCIENT": "Ancient",
                "MEDIEVAL": "Medieval",
                "RENAISSANCE": "Renaissance",
                "VICTORIAN": "Victorian",
                "EDWARDIAN": "Edwardian",
                "ART_DECO": "Art Deco",
                "MODERN": "Modern",
                "CONTEMPORARY": "Contemporary",
                "FUTURISTIC": "Futuristic",
            },
            "SEASON": {
                "SPRING": "Spring",
                "SUMMER": "Summer",
                "AUTUMN": "Autumn",
                "WINTER": "Winter",
            },
            "WEATHER": {
                "CLEAR": "Clear",
                "CLOUDY": "Cloudy",
                "RAINY": "Rainy",
                "SNOWY": "Snowy",
                "FOGGY": "Foggy",
                "STORMY": "Stormy",
                "WINDY": "Windy",
                "HUMID": "Humid",
                "DRY": "Dry",
            },
        }

    @staticmethod
    def get_mapping_categories() -> Dict[str, str]:
        """Get mapping category descriptions."""
        return {
            "DIURNAL": "Time of day mappings",
            "LOC_TYPE": "Location type mappings",
            "MOVE_TYPE": "Camera movement type mappings",
            "MOVE_SPEED": "Camera movement speed mappings",
            "ANGLE": "Camera angle mappings",
            "PERIOD": "Historical period mappings",
            "SEASON": "Seasonal mappings",
            "WEATHER": "Weather condition mappings",
        }

    @staticmethod
    def validate_mappings(mappings: Dict[str, Dict[str, str]]) -> bool:
        """Validate mappings structure."""
        if not isinstance(mappings, dict):
            return False

        for category, category_mappings in mappings.items():
            if not isinstance(category, str):
                return False

            if not isinstance(category_mappings, dict):
                return False

            for key, value in category_mappings.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    return False

        return True
