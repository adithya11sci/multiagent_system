"""
Delay Simulator - Simulates delay propagation
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class DelaySimulator:
    """
    Simulates how delays propagate through the railway network
    """
    
    def __init__(self):
        pass
    
    def simulate_delay(self, train_number: str, delay_minutes: int, 
                      current_location: Optional[str] = None) -> Dict[str, Any]:
        """
        Simulate delay propagation
        
        Args:
            train_number: Train identifier
            delay_minutes: Initial delay in minutes
            current_location: Where the delay occurred
            
        Returns:
            Propagation analysis
        """
        # Calculate propagation factor (delays tend to compound)
        propagation_factor = self._calculate_propagation_factor(delay_minutes)
        
        # Simulate downstream impacts
        downstream_delays = []
        remaining_delay = delay_minutes
        
        # Mock: Each subsequent station gets slightly less delay due to recovery time
        recovery_per_station = 3  # minutes recovered per station
        
        for i in range(5):  # Simulate next 5 stations
            remaining_delay = max(0, remaining_delay - recovery_per_station)
            if remaining_delay > 0:
                downstream_delays.append({
                    "station_index": i + 1,
                    "estimated_delay": remaining_delay,
                    "recovery_potential": "high" if remaining_delay < 15 else "medium" if remaining_delay < 30 else "low"
                })
        
        return {
            "train_number": train_number,
            "initial_delay": delay_minutes,
            "current_location": current_location,
            "propagation_factor": propagation_factor,
            "downstream_delays": downstream_delays,
            "total_affected_stations": len(downstream_delays),
            "estimated_recovery_time": self._estimate_recovery_time(delay_minutes),
            "risk_level": self._assess_risk_level(delay_minutes)
        }
    
    def _calculate_propagation_factor(self, delay_minutes: int) -> float:
        """
        Calculate how much the delay might compound
        """
        if delay_minutes <= 15:
            return 1.0  # No compounding
        elif delay_minutes <= 30:
            return 1.1  # 10% compounding
        elif delay_minutes <= 60:
            return 1.2  # 20% compounding
        else:
            return 1.3  # 30% compounding
    
    def _estimate_recovery_time(self, delay_minutes: int) -> str:
        """
        Estimate when the train might recover to schedule
        """
        if delay_minutes <= 15:
            return "1-2 stations"
        elif delay_minutes <= 30:
            return "3-4 stations"
        elif delay_minutes <= 60:
            return "5-6 stations"
        else:
            return "7+ stations or may not fully recover"
    
    def _assess_risk_level(self, delay_minutes: int) -> str:
        """
        Assess overall risk level
        """
        if delay_minutes <= 15:
            return "low"
        elif delay_minutes <= 30:
            return "medium"
        elif delay_minutes <= 60:
            return "high"
        else:
            return "critical"
    
    def simulate_cascading_effects(self, affected_trains: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simulate cascading effects across multiple trains
        """
        total_impact = 0
        affected_connections = []
        
        for train_data in affected_trains:
            delay = train_data.get("delay_minutes", 0)
            total_impact += delay
            
            # Check for missed connections
            if delay > 20:
                affected_connections.append({
                    "train": train_data.get("train_number"),
                    "impact": "missed_connections",
                    "estimated_passengers_affected": train_data.get("passengers", 0) * 0.2
                })
        
        return {
            "total_trains_affected": len(affected_trains),
            "total_delay_minutes": total_impact,
            "average_delay": total_impact / len(affected_trains) if affected_trains else 0,
            "affected_connections": affected_connections,
            "system_stress_level": self._calculate_system_stress(total_impact, len(affected_trains))
        }
    
    def _calculate_system_stress(self, total_delay: int, num_trains: int) -> str:
        """
        Calculate overall system stress level
        """
        avg_delay = total_delay / num_trains if num_trains > 0 else 0
        
        if avg_delay <= 15:
            return "normal"
        elif avg_delay <= 30:
            return "moderate"
        elif avg_delay <= 60:
            return "high"
        else:
            return "critical"
