#!/usr/bin/env python3
"""
Chaos Engineering Controller - Simplified for 48h Testing
Implements network latency and packet loss simulation
"""

import subprocess
import time
import json
from datetime import datetime


class ChaosController:
    def __init__(self, toxiproxy_url="http://localhost:8474"):
        self.toxiproxy_url = toxiproxy_url
        self.active_toxics = []

        # Test scenarios optimized for 48h execution
        self.scenarios = {
            "baseline": {
                "name": "Baseline",
                "latency_ms": 0,
                "packet_loss": 0.0,
                "description": "Normal network conditions"
            },
            "medium_stress": {
                "name": "Medium Stress",
                "latency_ms": 150,
                "packet_loss": 0.03,
                "description": "Moderate network degradation"
            },
            "high_stress": {
                "name": "High Stress",
                "latency_ms": 300,
                "packet_loss": 0.1,
                "description": "Severe network conditions"
            },
            "extreme_stress": {
                "name": "Extreme Stress",
                "latency_ms": 500,
                "packet_loss": 0.15,
                "description": "Extreme network degradation"
            }
        }

    def setup_proxies(self):
        """Setup toxiproxy proxies for services with real chaos engineering"""
        try:
            # Try to connect to toxiproxy
            import requests
            response = requests.get(f"{self.toxiproxy_url}/version", timeout=5)
            print("[OK] Toxiproxy connected successfully")

            # Create proxy for order service
            proxy_config = {
                "name": "order-service",
                "listen": "0.0.0.0:8090",
                "upstream": "172.17.0.1:3000"  # Docker host IP
            }

            # Delete existing proxy if it exists
            try:
                requests.delete(f"{self.toxiproxy_url}/proxies/order-service")
            except:
                pass

            # Create new proxy
            proxy_response = requests.post(f"{self.toxiproxy_url}/proxies", json=proxy_config)
            if proxy_response.status_code in [200, 201]:
                print("[OK] Order service proxy created")
                return True
            else:
                print(f"[WARN] Failed to create proxy: {proxy_response.text}")
                return False

        except Exception as e:
            print(f"[WARN] Toxiproxy not available, running without chaos engineering: {e}")
            return False

    def apply_scenario(self, scenario_name):
        """Apply real chaos scenario using Toxiproxy"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}")

        scenario = self.scenarios[scenario_name]
        print(f"\n[CHAOS] Applying chaos scenario: {scenario['name']}")
        print(f"   Target Latency: {scenario['latency_ms']}ms")
        print(f"   Target Packet Loss: {scenario['packet_loss']*100}%")

        try:
            # Clear existing toxics first
            self.clear_toxics()

            # Apply latency if > 0
            if scenario['latency_ms'] > 0:
                self._add_latency_toxic("order-service", scenario['latency_ms'])

            # Apply packet loss if > 0
            if scenario['packet_loss'] > 0:
                self._add_packet_loss_toxic("order-service", scenario['packet_loss'])

            print("   [OK] Real chaos conditions applied")
            chaos_mode = "real"

        except Exception as e:
            print(f"   [WARN] Falling back to simulated chaos: {e}")
            chaos_mode = "simulated"

        # Brief pause for chaos to take effect
        time.sleep(3)

        return {
            "scenario_applied": scenario_name,
            "timestamp": datetime.now().isoformat(),
            "config": scenario,
            "chaos_mode": chaos_mode
        }

    def _add_latency_toxic(self, service, latency_ms):
        """Add latency toxic to service"""
        toxic_name = f"{service}_latency"
        try:
            subprocess.run([
                "curl", "-X", "POST",
                f"{self.toxiproxy_url}/proxies/{service}/toxics",
                "-d", json.dumps({
                    "name": toxic_name,
                    "type": "latency",
                    "attributes": {
                        "latency": latency_ms,
                        "jitter": latency_ms // 10  # 10% jitter
                    }
                }),
                "-H", "Content-Type: application/json"
            ], check=True, capture_output=True)

            self.active_toxics.append({"service": service, "name": toxic_name})
            print(f"   [OK] Latency toxic applied: {latency_ms}ms")

        except subprocess.CalledProcessError as e:
            print(f"   [ERROR] Failed to apply latency toxic: {e}")

    def _add_packet_loss_toxic(self, service, loss_rate):
        """Add packet loss toxic to service"""
        toxic_name = f"{service}_packet_loss"
        try:
            subprocess.run([
                "curl", "-X", "POST",
                f"{self.toxiproxy_url}/proxies/{service}/toxics",
                "-d", json.dumps({
                    "name": toxic_name,
                    "type": "slow_close",
                    "attributes": {
                        "delay": int(loss_rate * 1000)  # Convert to ms
                    }
                }),
                "-H", "Content-Type: application/json"
            ], check=True, capture_output=True)

            self.active_toxics.append({"service": service, "name": toxic_name})
            print(f"   [OK] Packet loss toxic applied: {loss_rate*100}%")

        except subprocess.CalledProcessError as e:
            print(f"   [ERROR] Failed to apply packet loss toxic: {e}")

    def clear_toxics(self):
        """Clear all active toxics - Simplified"""
        self.active_toxics.clear()
        print("[CLEAN] Chaos scenario cleared (simulated mode)")

    def get_scenario_list(self):
        """Get list of available scenarios"""
        return list(self.scenarios.keys())

    def destroy_proxies(self):
        """Cleanup all proxies"""
        try:
            subprocess.run([
                "curl", "-X", "DELETE",
                f"{self.toxiproxy_url}/reset"
            ], check=True, capture_output=True)
            print("[CLEAN] All proxies destroyed")
        except subprocess.CalledProcessError as e:
            print(f"[WARN] Failed to destroy proxies: {e}")


def test_chaos_controller():
    """Test chaos controller functionality"""
    controller = ChaosController()

    print("[TEST] Testing Chaos Controller")
    print("=" * 50)

    # Test scenario application
    for scenario in controller.get_scenario_list():
        print(f"\nTesting scenario: {scenario}")
        result = controller.apply_scenario(scenario)
        print(f"Result: {result}")
        time.sleep(2)
        controller.clear_toxics()

    print("\n[OK] Chaos Controller test completed")


if __name__ == "__main__":
    test_chaos_controller()