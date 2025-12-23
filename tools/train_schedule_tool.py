"""
Train Schedule Tool - Access and manage train schedules
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

class TrainScheduleTool:
    """
    Tool to access train schedule data
    In production, this would connect to a real database
    """
    
    def __init__(self):
        # Mock database - in production, use SQLAlchemy with real DB
        self.schedules = self._load_mock_schedules()
    
    def _load_mock_schedules(self) -> Dict[str, Any]:
        """Load mock schedule data"""
        return {
            "12627": {
                "train_number": "12627",
                "train_name": "Karnataka Express",
                "route": [
                    {"station": "Bangalore", "arrival": None, "departure": "22:00", "platform": 1},
                    {"station": "Jolarpettai", "arrival": "01:15", "departure": "01:20", "platform": 2},
                    {"station": "Katpadi", "arrival": "02:30", "departure": "02:35", "platform": 1},
                    {"station": "Chennai", "arrival": "05:45", "departure": "06:00", "platform": 3},
                    {"station": "Vijayawada", "arrival": "13:30", "departure": "13:45", "platform": 2},
                    {"station": "New Delhi", "arrival": "06:15", "departure": None, "platform": 4}
                ],
                "frequency": "Daily",
                "type": "Express"
            },
            "12650": {
                "train_number": "12650",
                "train_name": "Karnataka Sampark Kranti",
                "route": [
                    {"station": "Yesvantpur", "arrival": None, "departure": "18:45", "platform": 2},
                    {"station": "Bangalore", "arrival": "19:15", "departure": "19:20", "platform": 3},
                    {"station": "Katpadi", "arrival": "22:30", "departure": "22:35", "platform": 2},
                    {"station": "Chennai", "arrival": "01:15", "departure": "01:30", "platform": 1},
                    {"station": "New Delhi", "arrival": "03:20", "departure": None, "platform": 6}
                ],
                "frequency": "Daily",
                "type": "Superfast"
            }
        }
    
    def get_train_schedule(self, train_number: str) -> Dict[str, Any]:
        """
        Get complete schedule for a train
        """
        schedule = self.schedules.get(train_number, {})
        
        if not schedule:
            return {
                "error": f"Train {train_number} not found",
                "train_number": train_number
            }
        
        return schedule
    
    def get_station_arrivals(self, station: str, time_window: tuple) -> List[Dict[str, Any]]:
        """
        Get all train arrivals at a station within time window
        """
        arrivals = []
        
        for train_number, schedule in self.schedules.items():
            for stop in schedule["route"]:
                if stop["station"] == station and stop["arrival"]:
                    arrivals.append({
                        "train_number": train_number,
                        "train_name": schedule["train_name"],
                        "arrival": stop["arrival"],
                        "departure": stop["departure"],
                        "platform": stop["platform"]
                    })
        
        return arrivals
    
    def get_platform_availability(self, station: str, time_window: tuple) -> Dict[str, Any]:
        """
        Check platform availability at a station
        """
        arrivals = self.get_station_arrivals(station, time_window)
        
        platform_usage = {}
        for arrival in arrivals:
            platform = arrival["platform"]
            if platform not in platform_usage:
                platform_usage[platform] = []
            platform_usage[platform].append({
                "train": arrival["train_number"],
                "arrival": arrival["arrival"],
                "departure": arrival["departure"]
            })
        
        return {
            "station": station,
            "time_window": time_window,
            "platform_usage": platform_usage,
            "available_platforms": self._get_available_platforms(station, platform_usage)
        }
    
    def _get_available_platforms(self, station: str, platform_usage: Dict) -> List[int]:
        """Determine which platforms are available"""
        # Assuming stations have platforms 1-6
        all_platforms = set(range(1, 7))
        used_platforms = set(platform_usage.keys())
        available = list(all_platforms - used_platforms)
        return sorted(available)
    
    def find_connecting_trains(self, train_number: str, station: str) -> List[Dict[str, Any]]:
        """
        Find trains that connect at a specific station
        """
        main_schedule = self.get_train_schedule(train_number)
        
        if "error" in main_schedule:
            return []
        
        # Find when main train arrives at station
        main_arrival_time = None
        for stop in main_schedule["route"]:
            if stop["station"] == station:
                main_arrival_time = stop["arrival"]
                break
        
        if not main_arrival_time:
            return []
        
        # Find connecting trains
        connections = []
        for other_train, schedule in self.schedules.items():
            if other_train == train_number:
                continue
            
            for stop in schedule["route"]:
                if stop["station"] == station and stop["departure"]:
                    connections.append({
                        "train_number": other_train,
                        "train_name": schedule["train_name"],
                        "departure": stop["departure"],
                        "platform": stop["platform"],
                        "main_train_arrival": main_arrival_time
                    })
        
        return connections
