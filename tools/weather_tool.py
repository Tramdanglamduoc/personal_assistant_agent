from typing import Any, Dict
import requests

from tools.base_tool import BaseTool


class WeatherTool(BaseTool):
    @property
    def name(self) -> str:
        return "weather"

    def execute(self, args: Dict[str, Any]) -> str:
        city = args.get("city", "").strip()

        if not city:
            return "Weather error: 'city' is required."

        try:
            # Step 1: Convert city name to latitude and longitude
            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            geocoding_params = {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }

            geo_response = requests.get(geocoding_url, params=geocoding_params, timeout=10)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            results = geo_data.get("results")
            if not results:
                return f"Weather error: could not find location '{city}'."

            location = results[0]
            latitude = location["latitude"]
            longitude = location["longitude"]
            location_name = location["name"]
            country = location.get("country", "Unknown country")

            # Step 2: Get current weather
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True
            }

            weather_response = requests.get(weather_url, params=weather_params, timeout=10)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            current_weather = weather_data.get("current_weather")
            if not current_weather:
                return f"Weather error: weather data is unavailable for '{city}'."

            temperature = current_weather.get("temperature")
            windspeed = current_weather.get("windspeed")
            weather_code = current_weather.get("weathercode")

            description = self._weather_code_to_text(weather_code)

            return (
                f"Current weather in {location_name}, {country}: "
                f"{description}, temperature {temperature}°C, wind speed {windspeed} km/h."
            )

        except requests.RequestException as e:
            return f"Weather API error: {str(e)}"
        except Exception as e:
            return f"Weather error: {str(e)}"

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": "weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "city": {
                        "type_": "STRING",
                        "description": "The city name, for example 'Riga' or 'Tokyo'"
                    }
                },
                "required": ["city"]
            }
        }

    def _weather_code_to_text(self, code: int) -> str:
        weather_codes = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "fog",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle",
            55: "dense drizzle",
            56: "light freezing drizzle",
            57: "dense freezing drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            66: "light freezing rain",
            67: "heavy freezing rain",
            71: "slight snow fall",
            73: "moderate snow fall",
            75: "heavy snow fall",
            77: "snow grains",
            80: "slight rain showers",
            81: "moderate rain showers",
            82: "violent rain showers",
            85: "slight snow showers",
            86: "heavy snow showers",
            95: "thunderstorm",
            96: "thunderstorm with slight hail",
            99: "thunderstorm with heavy hail"
        }
        return weather_codes.get(code, f"unknown weather code ({code})")