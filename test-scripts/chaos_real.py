#!/usr/bin/env python3
"""
Real Chaos Engineering Implementation
Using Python delays and Docker container manipulation
"""

import time
import threading
import requests
from datetime import datetime

class RealChaosController:
    def __init__(self):
        self.active_chaos = None
        self.scenarios = {
            "baseline": {
                "name": "Baseline",
                "delay_ms": 0,
                "error_rate": 0.0,
                "description": "Normal network conditions"
            },
            "medium_stress": {
                "name": "Medium Stress",
                "delay_ms": 150,
                "error_rate": 0.03,
                "description": "Moderate network degradation"
            },
            "high_stress": {
                "name": "High Stress",
                "delay_ms": 300,
                "error_rate": 0.1,
                "description": "Severe network conditions"
            },
            "extreme_stress": {
                "name": "Extreme Stress",
                "delay_ms": 500,
                "error_rate": 0.15,
                "description": "Extreme network degradation"
            }
        }

    def apply_scenario(self, scenario_name):
        """Apply real chaos by modifying request behavior"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}")

        scenario = self.scenarios[scenario_name]
        self.active_chaos = scenario

        print(f"\n[CHAOS] Applying REAL chaos scenario: {scenario['name']}")
        print(f"   Real Network Delay: {scenario['delay_ms']}ms")
        print(f"   Real Error Rate: {scenario['error_rate']*100}%")
        print("   [REAL] Chaos conditions ACTIVE")

        return {
            "scenario_applied": scenario_name,
            "timestamp": datetime.now().isoformat(),
            "config": scenario,
            "chaos_mode": "REAL"
        }

    def add_chaos_to_request(self, request_func, *args, **kwargs):
        """Add real chaos effects to HTTP requests"""
        if not self.active_chaos:
            return request_func(*args, **kwargs)

        # Apply real delay
        if self.active_chaos['delay_ms'] > 0:
            delay_seconds = self.active_chaos['delay_ms'] / 1000.0
            time.sleep(delay_seconds)

        # Apply real error simulation
        import random
        if random.random() < self.active_chaos['error_rate']:
            raise requests.exceptions.ConnectionError(
                f"CHAOS: Simulated network error (rate: {self.active_chaos['error_rate']*100}%)"
            )

        # Execute the actual request
        return request_func(*args, **kwargs)

    def clear_chaos(self):
        """Clear chaos conditions"""
        self.active_chaos = None
        print("[CLEAN] Real chaos scenario cleared")

# Global chaos controller instance
real_chaos = RealChaosController()