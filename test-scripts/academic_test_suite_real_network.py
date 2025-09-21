#!/usr/bin/env python3
"""
Academic Test Suite with Real Network Simulation
Simulates real server conditions: WAN, latency, jitter, packet loss
"""

import requests
import json
import time
import statistics
import threading
import concurrent.futures
import random
from datetime import datetime
import numpy as np
from scipy import stats
import psutil
import os
from network_simulator import real_world_sim


class RealNetworkTestSuite:
    def __init__(self, base_url, pattern_name):
        self.base_url = base_url
        self.pattern_name = pattern_name

        # Real-world test configuration
        self.config = {
            'runs_per_scenario': 8,       # Fewer runs due to realistic delays
            'load_test_requests': 50,     # Smaller load for realistic simulation
            'concurrent_users': 5,        # Lower concurrency for real conditions
            'test_timeout': 60,           # Longer timeout for real network delays
            'real_world_scenarios': [
                'enterprise_lan',
                'cloud_datacenter',
                'remote_office',
                'mobile_users',
                'poor_connectivity'
            ]
        }

        self.results = {
            'pattern_name': pattern_name,
            'test_suite_version': 'real_network_simulation',
            'execution_start': datetime.now().isoformat(),
            'scenarios': {},
            'summary_stats': {},
            'execution_metadata': {}
        }

    def generate_order_payload(self, product_code="COMPLEX", unit_value=1500.0, quantity=1):
        """Generate standardized order payload"""
        if product_code == "COMPLEX":
            return {
                "products": [
                    {"product": {"code": "SMARTPHONE", "unitValue": 1500.0}, "quantity": 3},
                    {"product": {"code": "NOTEBOOK", "unitValue": 1500.0}, "quantity": 2}
                ]
            }
        else:
            return {
                "products": [
                    {"product": {"code": product_code, "unitValue": unit_value}, "quantity": quantity}
                ]
            }

    def execute_real_network_request(self, payload, timeout=60):
        """Execute request with real network simulation"""
        start_time = time.time()
        cpu_before = psutil.cpu_percent()
        memory_before = psutil.virtual_memory().percent

        try:
            # Apply REAL network simulation (WAN conditions)
            response = real_world_sim.simulate_real_world_request(
                requests.post,
                f"{self.base_url}/api/order",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )

            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000

            cpu_after = psutil.cpu_percent()
            memory_after = psutil.virtual_memory().percent

            return {
                'success': response.status_code in [200, 201],
                'status_code': response.status_code,
                'duration_ms': duration_ms,
                'cpu_usage_delta': cpu_after - cpu_before,
                'memory_usage_delta': memory_after - memory_before,
                'timestamp': datetime.now().isoformat(),
                'real_network_applied': real_world_sim.active_scenario is not None,
                'network_scenario': real_world_sim.active_scenario
            }

        except Exception as e:
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000

            return {
                'success': False,
                'status_code': 0,
                'duration_ms': duration_ms,
                'error': str(e),
                'cpu_usage_delta': 0,
                'memory_usage_delta': 0,
                'timestamp': datetime.now().isoformat(),
                'real_network_applied': real_world_sim.active_scenario is not None,
                'network_scenario': real_world_sim.active_scenario
            }

    def run_real_network_load_test(self, scenario_name, num_requests=50):
        """Execute load test with real network conditions"""
        print(f"[START] Running Real Network Load Test...")
        print(f"  [DATA] Load Test: {num_requests} requests")
        print(f"  [NETWORK] Scenario: {scenario_name}")

        payload = self.generate_order_payload("COMPLEX")
        results = []
        start_time = time.time()

        for i in range(num_requests):
            if i % 10 == 0:  # Progress feedback
                print(f"  [PROGRESS] {i}/{num_requests} requests completed")

            result = self.execute_real_network_request(payload)
            results.append(result)

            # Small delay between requests to simulate realistic usage
            time.sleep(0.1)

        end_time = time.time()
        total_duration = end_time - start_time

        # Calculate metrics
        successful_requests = sum(1 for r in results if r['success'])
        success_rate = successful_requests / len(results)
        latencies = [r['duration_ms'] for r in results]
        throughput = len(results) / total_duration

        return {
            'scenario': scenario_name,
            'total_requests': len(results),
            'successful_requests': successful_requests,
            'success_rate': success_rate,
            'total_duration_s': total_duration,
            'throughput_req_s': throughput,
            'latency_stats': {
                'mean_ms': statistics.mean(latencies),
                'median_ms': statistics.median(latencies),
                'std_dev_ms': statistics.stdev(latencies) if len(latencies) > 1 else 0,
                'min_ms': min(latencies),
                'max_ms': max(latencies),
                'p95_ms': np.percentile(latencies, 95),
                'p99_ms': np.percentile(latencies, 99)
            },
            'network_conditions': real_world_sim.network_sim.get_network_stats(),
            'detailed_results': results
        }

    def run_real_network_concurrent_test(self, scenario_name, concurrent_users=5):
        """Execute concurrent test with real network simulation"""
        print(f"[PROCESS] Running Real Network Concurrent Test...")
        print(f"  [PROCESS] Concurrent Test: {concurrent_users} users")

        payload = self.generate_order_payload("COMPLEX")
        results = []

        def worker():
            return self.execute_real_network_request(payload)

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(worker) for _ in range(concurrent_users * 3)]  # 3 requests per user
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        end_time = time.time()
        total_duration = end_time - start_time

        successful_requests = sum(1 for r in results if r['success'])
        success_rate = successful_requests / len(results)
        latencies = [r['duration_ms'] for r in results]

        return {
            'scenario': scenario_name,
            'concurrent_users': concurrent_users,
            'total_requests': len(results),
            'successful_requests': successful_requests,
            'success_rate': success_rate,
            'total_duration_s': total_duration,
            'avg_latency_ms': statistics.mean(latencies),
            'network_conditions': real_world_sim.network_sim.get_network_stats(),
            'detailed_results': results
        }

    def test_real_world_scenario(self, scenario_name):
        """Test a specific real-world network scenario"""
        print(f"\n[TEST] Testing Real-World Scenario: {scenario_name.upper()}")
        print("=" * 70)

        # Apply real-world network simulation
        sim_result = real_world_sim.apply_real_world_scenario(scenario_name)

        print(f"[WAIT] Waiting for network stabilization (15s)...")
        time.sleep(15)  # Allow network simulation to stabilize

        # Execute tests
        load_test_result = self.run_real_network_load_test(scenario_name, self.config['load_test_requests'])
        concurrent_test_result = self.run_real_network_concurrent_test(scenario_name, self.config['concurrent_users'])

        # Calculate aggregate metrics
        all_latencies = []
        all_latencies.extend([r['duration_ms'] for r in load_test_result['detailed_results']])
        all_latencies.extend([r['duration_ms'] for r in concurrent_test_result['detailed_results']])

        scenario_result = {
            'scenario_name': scenario_name,
            'network_simulation_config': sim_result,
            'tests': {
                'load_test': load_test_result,
                'concurrent_test': concurrent_test_result
            },
            'aggregate_metrics': {
                'total_requests': len(all_latencies),
                'mean_latency_ms': statistics.mean(all_latencies),
                'p95_latency_ms': np.percentile(all_latencies, 95),
                'overall_success_rate': (
                    load_test_result['success_rate'] +
                    concurrent_test_result['success_rate']
                ) / 2
            }
        }

        print(f"\n[STATS] Real-World Scenario Summary:")
        print(f"   Load Test Success Rate: {load_test_result['success_rate']*100:.1f}%")
        print(f"   Concurrent Test Success Rate: {concurrent_test_result['success_rate']*100:.1f}%")
        print(f"   Network Conditions: {sim_result['config']['description']}")
        print(f"   Mean Latency: {scenario_result['aggregate_metrics']['mean_latency_ms']:.1f}ms")

        try:
            real_world_sim.clear_simulation()
            print("[CLEAN] Clearing network simulation...")
        except:
            pass

        return scenario_result

    def run_complete_real_network_suite(self):
        """Execute the complete real-network test suite"""
        print(f"\nStarting Real-Network Academic Test Suite for {self.pattern_name}")
        print("\n" + "=" * 80)
        print(f"[TARGET] REAL-NETWORK TEST SUITE - {self.pattern_name.upper()} PATTERN")
        print("=" * 80)

        print("Configuration:")
        print(f"  Runs per scenario: {self.config['runs_per_scenario']}")
        print(f"  Load test requests: {self.config['load_test_requests']}")
        print(f"  Concurrent users: {self.config['concurrent_users']}")
        print(f"  Real-world scenarios: {', '.join(self.config['real_world_scenarios'])}")

        print(f"\n[SETUP] Setting up REAL Network Simulation...")
        print("[OK] Real-world network simulator initialized")

        total_runs = len(self.config['real_world_scenarios']) * self.config['runs_per_scenario']
        current_run = 0

        for scenario in self.config['real_world_scenarios']:
            for run_num in range(1, self.config['runs_per_scenario'] + 1):
                current_run += 1
                print(f"\n[PROCESS] RUN {current_run}/{total_runs}")
                print("-" * 60)

                run_key = f"{scenario}_run_{run_num}"
                scenario_result = self.test_real_world_scenario(scenario)
                self.results['scenarios'][run_key] = scenario_result

                print(f"[PROGRESS] Completed run {current_run}/{total_runs}")

                # Brief pause between runs
                time.sleep(2)

        # Generate summary statistics
        self.generate_summary_stats()

        # Save results
        self.save_results()

        print(f"\n[COMPLETE] Real-network test suite execution completed!")
        print(f"Total scenarios executed: {len(self.results['scenarios'])}")
        print(f"Results saved to: academic_results_{self.pattern_name}_real_network.json")

    def generate_summary_stats(self):
        """Generate comprehensive summary statistics"""
        print(f"\n[ANALYSIS] Generating summary statistics...")

        scenario_stats = {}

        for scenario in self.config['real_world_scenarios']:
            scenario_runs = [
                result for key, result in self.results['scenarios'].items()
                if result['scenario_name'] == scenario
            ]

            if scenario_runs:
                latencies = [run['aggregate_metrics']['mean_latency_ms'] for run in scenario_runs]
                success_rates = [run['aggregate_metrics']['overall_success_rate'] for run in scenario_runs]
                p95_latencies = [run['aggregate_metrics']['p95_latency_ms'] for run in scenario_runs]

                scenario_stats[scenario] = {
                    'runs_count': len(scenario_runs),
                    'latency_stats': {
                        'mean': statistics.mean(latencies),
                        'std_dev': statistics.stdev(latencies) if len(latencies) > 1 else 0,
                        'min': min(latencies),
                        'max': max(latencies)
                    },
                    'success_rate_stats': {
                        'mean': statistics.mean(success_rates),
                        'std_dev': statistics.stdev(success_rates) if len(success_rates) > 1 else 0
                    },
                    'p95_latency_stats': {
                        'mean': statistics.mean(p95_latencies),
                        'std_dev': statistics.stdev(p95_latencies) if len(p95_latencies) > 1 else 0
                    }
                }

        self.results['summary_stats'] = scenario_stats
        self.results['execution_metadata'] = {
            'total_scenarios': len(self.config['real_world_scenarios']),
            'runs_per_scenario': self.config['runs_per_scenario'],
            'total_runs_executed': len(self.results['scenarios']),
            'execution_end': datetime.now().isoformat(),
            'network_simulation': 'REAL_WORLD_CONDITIONS',
            'config_used': self.config
        }

    def save_results(self):
        """Save results to JSON file"""
        filename = f"academic_results_{self.pattern_name}_real_network.json"

        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"[OK] Results saved to: {filename}")
            return filename
        except Exception as e:
            print(f"[ERROR] Failed to save results: {e}")
            return None


def main():
    """Main execution function"""
    import sys

    if len(sys.argv) != 3:
        print("Usage: python academic_test_suite_real_network.py <pattern> <base_url>")
        print("Example: python academic_test_suite_real_network.py orchestrated http://localhost:3000")
        sys.exit(1)

    pattern_name = sys.argv[1].lower()
    base_url = sys.argv[2]

    if pattern_name not in ['orchestrated', 'choreographed']:
        print("Error: Pattern must be 'orchestrated' or 'choreographed'")
        sys.exit(1)

    # Create and run test suite
    test_suite = RealNetworkTestSuite(base_url, pattern_name)
    test_suite.run_complete_real_network_suite()


if __name__ == "__main__":
    main()