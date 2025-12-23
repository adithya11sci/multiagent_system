"""
Crowd Predictor - Predicts crowd levels and overcrowding
"""
from typing import Dict, Any, List, Tuple
from datetime import datetime
import random

class CrowdPredictor:
    """
    Predicts crowd levels based on bookings and historical data
    """
    
    def __init__(self):
        # Mock historical data - in production, use ML models
        self.historical_patterns = {}
    
    def predict(self, train_number: str, travel_date: str) -> Dict[str, Any]:
        """
        Predict crowd levels for a train on a specific date
        """
        # Mock prediction - in production, use ML model
        base_capacity = 1000
        
        # Day of week factor
        date_obj = datetime.strptime(travel_date, "%Y-%m-%d")
        day_of_week = date_obj.weekday()
        
        # Weekends typically have higher demand
        demand_factor = 1.3 if day_of_week in [4, 5, 6] else 1.0
        
        # Holiday factor (simplified)
        is_holiday_season = date_obj.month in [4, 5, 10, 12]
        if is_holiday_season:
            demand_factor *= 1.2
        
        predicted_passengers = int(base_capacity * demand_factor)
        occupancy_rate = min(predicted_passengers / base_capacity, 1.2)
        
        return {
            "train_number": train_number,
            "travel_date": travel_date,
            "predicted_passengers": predicted_passengers,
            "capacity": base_capacity,
            "occupancy_rate": round(occupancy_rate, 2),
            "status": self._get_status(occupancy_rate),
            "confidence": 0.85,
            "factors": {
                "day_of_week": day_of_week,
                "demand_factor": round(demand_factor, 2),
                "is_holiday_season": is_holiday_season
            }
        }
    
    def _get_status(self, occupancy_rate: float) -> str:
        """Determine status based on occupancy"""
        if occupancy_rate <= 0.7:
            return "comfortable"
        elif occupancy_rate <= 0.9:
            return "moderate"
        elif occupancy_rate <= 1.0:
            return "near_capacity"
        else:
            return "overcrowded"
    
    def get_historical_patterns(self, train_number: str) -> Dict[str, Any]:
        """
        Get historical crowd patterns for a train
        """
        # Mock historical data
        return {
            "train_number": train_number,
            "average_occupancy": 0.85,
            "peak_days": ["Friday", "Saturday", "Sunday"],
            "peak_months": ["April", "May", "October", "December"],
            "typical_high_demand_stations": [
                {"station": "Bangalore", "avg_boarding": 250},
                {"station": "Chennai", "avg_boarding": 180},
                {"station": "Vijayawada", "avg_boarding": 120}
            ],
            "historical_overcrowding_incidents": 5,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_station_crowd(self, station: str, time_window: Tuple[str, str]) -> Dict[str, Any]:
        """
        Get crowd predictions for a station
        """
        # Mock station crowd data
        base_crowd = random.randint(200, 800)
        
        return {
            "station": station,
            "time_window": time_window,
            "predicted_crowd": base_crowd,
            "platform_distribution": {
                "platform_1": int(base_crowd * 0.3),
                "platform_2": int(base_crowd * 0.25),
                "platform_3": int(base_crowd * 0.25),
                "platform_4": int(base_crowd * 0.2)
            },
            "peak_times": ["08:00-10:00", "18:00-20:00"],
            "safety_status": "normal" if base_crowd < 500 else "caution" if base_crowd < 700 else "alert"
        }
    
    def predict_segment_occupancy(self, train_number: str, 
                                  from_station: str, to_station: str) -> Dict[str, Any]:
        """
        Predict occupancy for a specific segment of the journey
        """
        # Mock segment prediction
        occupancy = random.uniform(0.6, 1.1)
        
        return {
            "train_number": train_number,
            "from_station": from_station,
            "to_station": to_station,
            "predicted_occupancy": round(occupancy, 2),
            "status": self._get_status(occupancy),
            "recommendation": self._get_recommendation(occupancy)
        }
    
    def _get_recommendation(self, occupancy: float) -> str:
        """Get recommendation based on occupancy"""
        if occupancy <= 0.7:
            return "Normal operations"
        elif occupancy <= 0.9:
            return "Monitor closely"
        elif occupancy <= 1.0:
            return "Consider adding extra coaches"
        else:
            return "Add extra coaches or run special service"
