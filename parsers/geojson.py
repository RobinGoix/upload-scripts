"""
This module constains custom OSC geojson parsing. This file is generated by KartaView Android app.
"""
from typing import Optional, List, Type
import time

from geojson import load

from parsers.base import BaseParser
from common.models import SensorItem, GPS

TWO_WAY_KEY = "osctagging"
TWO_WAY_VALUE = "twoway"

ONE_WAY_KEY = "osctagging"
ONE_WAY_VALUE = "oneway"

CLOSED_KEY = "osctagging"
CLOSED_VALUE = "closedRoad"

NARROW_ROAD_KEY = "osctagging"
NARROW_ROAD_VALUE = "narrowRoad"

OTHER_KEY = "osctagging"
OTHER_VALUE = "notes"


class GeoJsonParser(BaseParser):
    """this class is a BaseParser that can parse a GPX"""

    def serialize(self):
        """serialize the sensors into geojson format"""
        print("This method is not implemeted for GeoJsonParser", self)

    def next_item_with_class(self, _: Type[SensorItem]) -> Optional[SensorItem]:
        print("This method is not implemented for GeoJsonParser", self)

    def items_with_class(self, _: Type[SensorItem]) -> List[SensorItem]:
        print("This method is not implemeted for GeoJsonParser", self)
        return []

    def next_item(self) -> Optional[SensorItem]:
        print("This method is not implemeted for GeoJsonParser", self)

    def items(self) -> List[SensorItem]:
        with self._storage.open(self.file_path, 'r') as geo_json_file:
            geo_json = load(geo_json_file)
            index = 0
            sensors: List[SensorItem] = []
            for feature in geo_json["features"]:
                geometry = feature["geometry"]
                coordinates = geometry["coordinates"]

                for geometry_coordinate in coordinates:
                    if isinstance(geometry_coordinate, float) and len(coordinates) == 2:
                        # this is a point
                        gps = GPS()
                        gps.timestamp = time.time() + index
                        gps.latitude = coordinates[1]
                        gps.longitude = coordinates[0]
                        sensors.append(gps)
                        break

                    if (isinstance(geometry_coordinate[0], float)
                            and len(geometry_coordinate) == 2):
                        # this is a list of points
                        longitude = geometry_coordinate[0]
                        latitude = geometry_coordinate[1]
                        gps = GPS()
                        gps.timestamp = time.time() + index
                        gps.latitude = latitude
                        gps.longitude = longitude
                        sensors.append(gps)
                        index += 1
                    else:
                        # this is a list of list of points
                        for geometry_point_coordinate in geometry_coordinate[0]:
                            longitude = geometry_point_coordinate[0]
                            latitude = geometry_point_coordinate[1]
                            gps = GPS()
                            gps.timestamp = time.time() + index
                            gps.latitude = latitude
                            gps.longitude = longitude
                            sensors.append(gps)
                            index += 1
        return sensors

    def format_version(self) -> Optional[str]:
        print("GeoJsonParser version", self)
        return "unknown"

    @classmethod
    def compatible_sensors(cls):
        return [GPS]
