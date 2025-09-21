#!/usr/bin/env python3
"""
Network Simulator for Real Server Conditions
Simulates real network conditions: latency, jitter, packet loss, bandwidth
"""

import time
import random
import requests
from datetime import datetime
import threading
import queue
import socket


class NetworkSimulator:
    def __init__(self):
        self.active_profile = None
        self.profiles = {
            "localhost": {
                "name": "Localhost",
                "base_latency_ms": 1,
                "jitter_ms": 0.5,
                "packet_loss_rate": 0.001,
                "bandwidth_limit_mbps": 1000,
                "description": "Local network"
            },
            "lan": {
                "name": "Local Area Network",
                "base_latency_ms": 5,
                "jitter_ms": 2,
                "packet_loss_rate": 0.01,
                "bandwidth_limit_mbps": 100,
                "description": "Corporate LAN"
            },
            "wan_good": {
                "name": "Good WAN Connection",
                "base_latency_ms": 50,
                "jitter_ms": 10,
                "packet_loss_rate": 0.02,
                "bandwidth_limit_mbps": 50,
                "description": "Good internet connection"
            },
            "wan_average": {
                "name": "Average WAN Connection",
                "base_latency_ms": 100,
                "jitter_ms": 25,
                "packet_loss_rate": 0.05,
                "bandwidth_limit_mbps": 20,
                "description": "Average internet connection"
            },
            "wan_poor": {
                "name": "Poor WAN Connection",
                "base_latency_ms": 200,
                "jitter_ms": 50,
                "packet_loss_rate": 0.1,
                "bandwidth_limit_mbps": 5,
                "description": "Poor internet connection"
            },
            "mobile_4g": {
                "name": "Mobile 4G Network",
                "base_latency_ms": 80,
                "jitter_ms": 30,
                "packet_loss_rate": 0.03,
                "bandwidth_limit_mbps": 25,
                "description": "Mobile 4G connection"
            },
            "mobile_3g": {
                "name": "Mobile 3G Network",
                "base_latency_ms": 150,
                "jitter_ms": 60,
                "packet_loss_rate": 0.08,
                "bandwidth_limit_mbps": 3,
                "description": "Mobile 3G connection"
            },
            "satellite": {
                "name": "Satellite Connection",
                "base_latency_ms": 600,
                "jitter_ms": 100,
                "packet_loss_rate": 0.15,
                "bandwidth_limit_mbps": 10,
                "description": "Satellite internet"
            }
        }

    def apply_network_profile(self, profile_name):
        """Apply network simulation profile"""
        if profile_name not in self.profiles:
            raise ValueError(f"Unknown profile: {profile_name}")

        self.active_profile = self.profiles[profile_name]
        print(f"\n[NETWORK] Applying network profile: {self.active_profile['name']}")
        print(f"   Base Latency: {self.active_profile['base_latency_ms']}ms")
        print(f"   Jitter: ±{self.active_profile['jitter_ms']}ms")
        print(f"   Packet Loss: {self.active_profile['packet_loss_rate']*100:.1f}%")
        print(f"   Bandwidth: {self.active_profile['bandwidth_limit_mbps']} Mbps")
        print(f"   [REAL] Network simulation ACTIVE")

        return {
            "profile_applied": profile_name,
            "timestamp": datetime.now().isoformat(),
            "config": self.active_profile,
            "simulation_mode": "REAL_NETWORK"
        }

    def simulate_network_delay(self):
        """Calculate realistic network delay with jitter"""
        if not self.active_profile:
            return 0

        base_latency = self.active_profile['base_latency_ms']
        jitter = self.active_profile['jitter_ms']

        # Apply jitter (normal distribution)
        actual_latency = base_latency + random.normalvariate(0, jitter/3)
        return max(0, actual_latency) / 1000.0  # Convert to seconds

    def simulate_packet_loss(self):
        """Simulate packet loss based on profile"""
        if not self.active_profile:
            return False

        loss_rate = self.active_profile['packet_loss_rate']
        return random.random() < loss_rate

    def simulate_bandwidth_limit(self, data_size_bytes):
        """Simulate bandwidth limitations"""
        if not self.active_profile:
            return 0

        bandwidth_bps = self.active_profile['bandwidth_limit_mbps'] * 1_000_000
        bandwidth_delay = data_size_bytes * 8 / bandwidth_bps  # Convert to seconds

        # Add some variability to bandwidth
        variability = random.normalvariate(1.0, 0.1)
        return max(0, bandwidth_delay * variability)

    def simulate_real_request(self, request_func, *args, **kwargs):
        """Apply real network simulation to HTTP requests"""
        if not self.active_profile:
            return request_func(*args, **kwargs)

        # Simulate packet loss
        if self.simulate_packet_loss():
            raise requests.exceptions.ConnectionError(
                f"NETWORK_SIM: Packet loss (rate: {self.active_profile['packet_loss_rate']*100:.1f}%)"
            )

        # Simulate network latency with jitter
        network_delay = self.simulate_network_delay()
        if network_delay > 0:
            time.sleep(network_delay)

        # Execute the actual request
        start_time = time.time()
        response = request_func(*args, **kwargs)
        end_time = time.time()

        # Simulate bandwidth limitation based on response size
        if hasattr(response, 'content'):
            response_size = len(response.content)
            bandwidth_delay = self.simulate_bandwidth_limit(response_size)
            if bandwidth_delay > 0:
                time.sleep(bandwidth_delay)

        return response

    def get_network_stats(self):
        """Get current network simulation statistics"""
        if not self.active_profile:
            return {"status": "no_simulation"}

        return {
            "active_profile": self.active_profile['name'],
            "simulated_conditions": {
                "base_latency_ms": self.active_profile['base_latency_ms'],
                "jitter_ms": self.active_profile['jitter_ms'],
                "packet_loss_rate": self.active_profile['packet_loss_rate'],
                "bandwidth_mbps": self.active_profile['bandwidth_limit_mbps']
            },
            "realistic_simulation": True
        }

    def clear_simulation(self):
        """Clear network simulation"""
        self.active_profile = None
        print("[CLEAN] Network simulation cleared")


class ServerLoadSimulator:
    """Simulate server load conditions"""

    def __init__(self):
        self.active_load = None
        self.load_profiles = {
            "light": {
                "name": "Light Load",
                "cpu_delay_ms": 5,
                "memory_pressure": 0.1,
                "io_delay_ms": 10,
                "description": "Low server load"
            },
            "moderate": {
                "name": "Moderate Load",
                "cpu_delay_ms": 20,
                "memory_pressure": 0.3,
                "io_delay_ms": 50,
                "description": "Moderate server load"
            },
            "heavy": {
                "name": "Heavy Load",
                "cpu_delay_ms": 100,
                "memory_pressure": 0.7,
                "io_delay_ms": 200,
                "description": "Heavy server load"
            },
            "overloaded": {
                "name": "Overloaded",
                "cpu_delay_ms": 500,
                "memory_pressure": 0.9,
                "io_delay_ms": 1000,
                "description": "Server overloaded"
            }
        }

    def apply_load_profile(self, profile_name):
        """Apply server load simulation"""
        if profile_name not in self.load_profiles:
            raise ValueError(f"Unknown load profile: {profile_name}")

        self.active_load = self.load_profiles[profile_name]
        print(f"\n[SERVER] Applying server load: {self.active_load['name']}")
        print(f"   CPU Processing Delay: {self.active_load['cpu_delay_ms']}ms")
        print(f"   Memory Pressure: {self.active_load['memory_pressure']*100:.0f}%")
        print(f"   I/O Delay: {self.active_load['io_delay_ms']}ms")

        return {
            "load_applied": profile_name,
            "timestamp": datetime.now().isoformat(),
            "config": self.active_load
        }

    def simulate_server_processing(self):
        """Simulate server processing delays"""
        if not self.active_load:
            return

        # Simulate CPU processing delay
        cpu_delay = self.active_load['cpu_delay_ms'] / 1000.0
        cpu_variation = random.normalvariate(1.0, 0.2)
        actual_cpu_delay = max(0, cpu_delay * cpu_variation)

        if actual_cpu_delay > 0:
            time.sleep(actual_cpu_delay)

        # Simulate I/O delay with higher variability
        io_delay = self.active_load['io_delay_ms'] / 1000.0
        io_variation = random.normalvariate(1.0, 0.5)
        actual_io_delay = max(0, io_delay * io_variation)

        if actual_io_delay > 0:
            time.sleep(actual_io_delay)


class RealWorldSimulator:
    """Combined real-world network and server simulation"""

    def __init__(self):
        self.network_sim = NetworkSimulator()
        self.server_sim = ServerLoadSimulator()
        self.active_scenario = None

        # Predefined realistic scenarios
        self.scenarios = {
            "enterprise_lan": {
                "name": "Enterprise LAN",
                "network_profile": "lan",
                "server_load": "light",
                "description": "Corporate network with good infrastructure"
            },
            "cloud_datacenter": {
                "name": "Cloud Datacenter",
                "network_profile": "wan_good",
                "server_load": "moderate",
                "description": "Cloud deployment with good connectivity"
            },
            "remote_office": {
                "name": "Remote Office",
                "network_profile": "wan_average",
                "server_load": "moderate",
                "description": "Remote office with average internet"
            },
            "mobile_users": {
                "name": "Mobile Users",
                "network_profile": "mobile_4g",
                "server_load": "heavy",
                "description": "Mobile users on 4G network"
            },
            "poor_connectivity": {
                "name": "Poor Connectivity",
                "network_profile": "wan_poor",
                "server_load": "heavy",
                "description": "Poor network with overloaded server"
            },
            "disaster_recovery": {
                "name": "Disaster Recovery",
                "network_profile": "satellite",
                "server_load": "overloaded",
                "description": "Emergency satellite connection"
            }
        }

    def apply_real_world_scenario(self, scenario_name):
        """Apply complete real-world scenario"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}")

        scenario = self.scenarios[scenario_name]

        print(f"\n[REAL_WORLD] Applying scenario: {scenario['name']}")
        print(f"   Description: {scenario['description']}")

        # Apply network conditions
        network_result = self.network_sim.apply_network_profile(scenario['network_profile'])

        # Apply server load
        server_result = self.server_sim.apply_load_profile(scenario['server_load'])

        self.active_scenario = scenario_name

        return {
            "scenario_applied": scenario_name,
            "timestamp": datetime.now().isoformat(),
            "config": scenario,
            "network_simulation": network_result,
            "server_simulation": server_result,
            "simulation_mode": "REAL_WORLD"
        }

    def simulate_real_world_request(self, request_func, *args, **kwargs):
        """Execute request with full real-world simulation"""
        # Apply server processing delay first
        self.server_sim.simulate_server_processing()

        # Then apply network simulation
        return self.network_sim.simulate_real_request(request_func, *args, **kwargs)

    def get_scenario_list(self):
        """Get list of available real-world scenarios"""
        return list(self.scenarios.keys())

    def clear_simulation(self):
        """Clear all simulations"""
        self.network_sim.clear_simulation()
        self.active_scenario = None
        print("[CLEAN] Real-world simulation cleared")


# Global simulator instance for easy access
real_world_sim = RealWorldSimulator()


def test_real_world_simulation():
    """Test the real-world simulation"""
    print("Testing Real-World Network Simulation")
    print("=" * 50)

    # Test different scenarios
    for scenario in real_world_sim.get_scenario_list()[:3]:  # Test first 3
        print(f"\nTesting scenario: {scenario}")
        result = real_world_sim.apply_real_world_scenario(scenario)

        # Simulate a request
        start_time = time.time()
        try:
            response = real_world_sim.simulate_real_world_request(
                requests.get,
                'http://httpbin.org/delay/1'  # Simple test endpoint
            )
            duration = time.time() - start_time
            print(f"Request completed in: {duration:.2f}s (Status: {response.status_code})")
        except Exception as e:
            duration = time.time() - start_time
            print(f"Request failed after {duration:.2f}s: {e}")

        real_world_sim.clear_simulation()
        time.sleep(1)


if __name__ == "__main__":
    test_real_world_simulation()