"""
Booking Analyzer - Analyzes ticket booking data
"""
from typing import Dict, Any, List
from datetime import datetime
import random

class BookingAnalyzer:
    """
    Analyzes ticket booking patterns and data
    """
    
    def __init__(self):
        # Mock booking database
        self.bookings = {}
    
    def get_bookings(self, train_number: str, travel_date: str) -> Dict[str, Any]:
        """
        Get booking data for a train on a specific date
        """
        # Mock booking data - in production, query actual database
        total_capacity = 1000
        booked = random.randint(600, 1100)
        
        return {
            "train_number": train_number,
            "travel_date": travel_date,
            "total_capacity": total_capacity,
            "total_booked": booked,
            "occupancy_rate": round(booked / total_capacity, 2),
            "class_wise_bookings": {
                "sleeper": {
                    "capacity": 500,
                    "booked": min(random.randint(400, 550), 500),
                    "waitlist": max(0, booked - 500)
                },
                "ac_3tier": {
                    "capacity": 300,
                    "booked": min(random.randint(250, 350), 300),
                    "waitlist": max(0, random.randint(0, 50))
                },
                "ac_2tier": {
                    "capacity": 150,
                    "booked": min(random.randint(100, 170), 150),
                    "waitlist": max(0, random.randint(0, 20))
                },
                "ac_1tier": {
                    "capacity": 50,
                    "booked": min(random.randint(30, 60), 50),
                    "waitlist": 0
                }
            },
            "booking_trend": self._analyze_booking_trend(train_number, travel_date),
            "peak_booking_stations": [
                {"station": "Bangalore", "bookings": random.randint(150, 250)},
                {"station": "Chennai", "bookings": random.randint(100, 180)},
                {"station": "Vijayawada", "bookings": random.randint(80, 120)}
            ]
        }
    
    def _analyze_booking_trend(self, train_number: str, travel_date: str) -> str:
        """
        Analyze booking trend
        """
        trends = ["increasing", "stable", "decreasing", "rapidly_increasing"]
        return random.choice(trends)
    
    def get_passenger_demographics(self, train_number: str) -> Dict[str, Any]:
        """
        Get passenger demographics for a train
        """
        return {
            "train_number": train_number,
            "age_distribution": {
                "0-18": 0.15,
                "19-35": 0.40,
                "36-60": 0.35,
                "60+": 0.10
            },
            "gender_distribution": {
                "male": 0.60,
                "female": 0.38,
                "other": 0.02
            },
            "journey_type": {
                "business": 0.25,
                "leisure": 0.45,
                "family_visit": 0.20,
                "emergency": 0.05,
                "other": 0.05
            },
            "frequent_travelers": 0.30
        }
    
    def analyze_cancellation_patterns(self, train_number: str, 
                                     date_range: tuple) -> Dict[str, Any]:
        """
        Analyze booking cancellation patterns
        """
        return {
            "train_number": train_number,
            "date_range": date_range,
            "total_cancellations": random.randint(50, 150),
            "cancellation_rate": round(random.uniform(0.05, 0.15), 2),
            "cancellation_reasons": {
                "schedule_change": 0.30,
                "personal_reasons": 0.40,
                "found_alternative": 0.15,
                "refund": 0.15
            },
            "peak_cancellation_time": "24-48 hours before departure",
            "trend": "normal"
        }
    
    def get_real_time_booking_velocity(self, train_number: str) -> Dict[str, Any]:
        """
        Get real-time booking velocity (how fast tickets are being booked)
        """
        return {
            "train_number": train_number,
            "bookings_last_hour": random.randint(5, 50),
            "bookings_last_24_hours": random.randint(100, 300),
            "velocity": random.choice(["slow", "moderate", "fast", "very_fast"]),
            "predicted_sellout": random.choice(["unlikely", "possible", "likely", "certain"]),
            "time_to_sellout_estimate": f"{random.randint(1, 48)} hours"
        }
    
    def identify_high_value_passengers(self, train_number: str) -> List[Dict[str, Any]]:
        """
        Identify high-value passengers (frequent travelers, premium class, etc.)
        """
        return [
            {
                "passenger_id": f"P{i:04d}",
                "class": random.choice(["ac_1tier", "ac_2tier"]),
                "frequent_traveler": random.choice([True, False]),
                "loyalty_tier": random.choice(["gold", "platinum", "silver"]),
                "special_assistance": random.choice([None, "wheelchair", "elderly"])
            }
            for i in range(1, random.randint(10, 30))
        ]
