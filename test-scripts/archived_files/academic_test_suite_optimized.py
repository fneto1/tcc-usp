#!/usr/bin/env python3
"""
Academic Test Suite - Optimized for Speed with Scientific Rigor
Faster execution while maintaining statistical validity
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
from chaos_real import real_chaos


class OptimizedAcademicTestSuite:
    def __init__(self, base_url, pattern_name):
        self.base_url = base_url
        self.pattern_name = pattern_name

        # Optimized configuration for speed + scientific validity
        self.config = {
            'runs_per_scenario': 10,      # Statistically sufficient for comparison
            'load_test_requests': 100,    # Reduced but still meaningful
            'concurrent_users': 10,       # Manageable concurrency
            'test_timeout': 30,           # Faster execution
            'scenarios': ['baseline', 'medium_stress', 'high_stress', 'extreme_stress']
        }

        self.results = {
            'pattern_name': pattern_name,
            'test_suite_version': 'optimized_for_speed',
            'execution_start': datetime.now().isoformat(),
            'scenarios': {},
            'summary_stats': {},
            'execution_metadata': {}
        }

    def generate_order_payload(self, product_code="COMPLEX", unit_value=1500.0, quantity=1):
        """Generate standardized order payload with multiple products or single product"""
        if product_code == "COMPLEX":
            # Complex order with multiple products
            return {
                "products": [
                    {"product": {"code": "SMARTPHONE", "unitValue": 1500.0}, "quantity": 3},
                    {"product": {"code": "NOTEBOOK", "unitValue": 1500.0}, "quantity": 2}
                ]
            }
        else:
            # Single product order
            return {
                "products": [
                    {"product": {"code": product_code, "unitValue": unit_value}, "quantity": quantity}
                ]
            }

    def execute_single_request(self, payload, timeout=30):
        """Execute single request with comprehensive metrics"""
        start_time = time.time()
        cpu_before = psutil.cpu_percent()
        memory_before = psutil.virtual_memory().percent

        try:
            # Apply REAL chaos engineering
            response = real_chaos.add_chaos_to_request(
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
                'chaos_applied': real_chaos.active_chaos is not None
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
                'chaos_applied': real_chaos.active_chaos is not None
            }

    def run_load_test(self, scenario_name, num_requests=100):
        """Execute load test with specified parameters"""
        print(f"[START] Running Load Test...")
        print(f"  [DATA] Load Test: {num_requests} requests")

        payload = self.generate_order_payload("COMPLEX")
        results = []
        start_time = time.time()

        for i in range(num_requests):
            if i % 20 == 0:  # Progress feedback
                print(f"  [PROGRESS] {i}/{num_requests} requests completed")

            result = self.execute_single_request(payload)
            results.append(result)

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
            'detailed_results': results
        }

    def run_concurrent_test(self, scenario_name, concurrent_users=10):
        """Execute concurrent stress test"""
        print(f"[PROCESS] Running Concurrent Stress Test...")
        print(f"  [PROCESS] Concurrent Test: {concurrent_users} threads")

        payload = self.generate_order_payload("COMPLEX")
        results = []

        def worker():
            return self.execute_single_request(payload)

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(worker) for _ in range(concurrent_users * 2)]  # 2 requests per user
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
            'detailed_results': results
        }

    def run_resilience_test(self, scenario_name):
        """Execute resilience test with edge cases"""
        print(f"[SHIELD] Running Resilience Test...")
        print(f"  [SHIELD] Resilience Test: Multiple failure conditions")

        test_cases = [
            self.generate_order_payload("COMPLEX"),
            self.generate_order_payload("SMARTPHONE", 1500.0, 1),
            self.generate_order_payload("NOTEBOOK", 1500.0, 1),
        ]

        results = []
        for payload in test_cases:
            result = self.execute_single_request(payload, timeout=15)  # Shorter timeout
            results.append(result)

        successful_requests = sum(1 for r in results if r['success'])
        success_rate = successful_requests / len(results)

        return {
            'scenario': scenario_name,
            'test_cases': len(test_cases),
            'successful_cases': successful_requests,
            'success_rate': success_rate,
            'detailed_results': results
        }

    def test_scenario(self, scenario_name):
        """Test a specific chaos scenario"""
        print(f"\n[TEST] Testing Scenario: {scenario_name.upper()}")
        print("=" * 60)

        # Apply chaos scenario with REAL chaos engineering
        chaos_result = real_chaos.apply_scenario(scenario_name)

        print(f"[WAIT] Waiting for system stabilization (10s)...")
        time.sleep(10)  # Reduced stabilization time

        # Execute tests
        load_test_result = self.run_load_test(scenario_name, self.config['load_test_requests'])
        concurrent_test_result = self.run_concurrent_test(scenario_name, self.config['concurrent_users'])
        resilience_test_result = self.run_resilience_test(scenario_name)

        # Calculate aggregate metrics
        all_latencies = []
        all_latencies.extend([r['duration_ms'] for r in load_test_result['detailed_results']])
        all_latencies.extend([r['duration_ms'] for r in concurrent_test_result['detailed_results']])
        all_latencies.extend([r['duration_ms'] for r in resilience_test_result['detailed_results']])

        scenario_result = {
            'scenario_name': scenario_name,
            'chaos_config': chaos_result,
            'tests': {
                'load_test': load_test_result,
                'concurrent_test': concurrent_test_result,
                'resilience_test': resilience_test_result
            },
            'aggregate_metrics': {
                'total_requests': len(all_latencies),
                'mean_latency_ms': statistics.mean(all_latencies),
                'p95_latency_ms': np.percentile(all_latencies, 95),
                'overall_success_rate': (
                    load_test_result['success_rate'] +
                    concurrent_test_result['success_rate'] +
                    resilience_test_result['success_rate']
                ) / 3
            }
        }

        print(f"\n[STATS] Scenario Summary:")
        print(f"   Load Test Success Rate: {load_test_result['success_rate']*100:.1f}%")
        print(f"   Concurrent Test Success Rate: {concurrent_test_result['success_rate']*100:.1f}%")
        print(f"   Chaos Conditions: {chaos_result['config']['description']}")

        try:
            real_chaos.clear_chaos()
            print("[CLEAN] Clearing chaos conditions...")
        except:
            pass

        return scenario_result

    def run_complete_test_suite(self):
        """Execute the complete test suite"""
        print(f"\nStarting Optimized Academic Test Suite for {self.pattern_name}")
        print("\n" + "=" * 80)
        print(f"[TARGET] OPTIMIZED ACADEMIC TEST SUITE - {self.pattern_name.upper()} PATTERN")
        print("=" * 80)

        print("Configuration:")
        print(f"  Runs per scenario: {self.config['runs_per_scenario']}")
        print(f"  Load test requests: {self.config['load_test_requests']}")
        print(f"  Concurrent users: {self.config['concurrent_users']}")
        print(f"  Scenarios: {', '.join(self.config['scenarios'])}")

        print(f"\n[SETUP] Setting up REAL Chaos Engineering...")
        print("[OK] Real chaos controller initialized")

        total_runs = len(self.config['scenarios']) * self.config['runs_per_scenario']
        current_run = 0

        for scenario in self.config['scenarios']:
            for run_num in range(1, self.config['runs_per_scenario'] + 1):
                current_run += 1
                print(f"\n[PROCESS] RUN {current_run}/{total_runs}")
                print("-" * 60)

                # Apply chaos scenario BEFORE testing
                chaos_result = real_chaos.apply_scenario(scenario)

                run_key = f"{scenario}_run_{run_num}"
                scenario_result = self.test_scenario(scenario)
                self.results['scenarios'][run_key] = scenario_result

                print(f"[PROGRESS] Completed run {current_run}/{total_runs}")

        # Generate summary statistics
        self.generate_summary_stats()

        # Save results
        self.save_results()

        print(f"\n[COMPLETE] Test suite execution completed!")
        print(f"Total scenarios executed: {len(self.results['scenarios'])}")
        print(f"Results saved to: academic_results_{self.pattern_name}_optimized.json")

    def generate_summary_stats(self):
        """Generate comprehensive summary statistics"""
        print(f"\n[ANALYSIS] Generating summary statistics...")

        scenario_stats = {}

        for scenario in self.config['scenarios']:
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
            'total_scenarios': len(self.config['scenarios']),
            'runs_per_scenario': self.config['runs_per_scenario'],
            'total_runs_executed': len(self.results['scenarios']),
            'execution_end': datetime.now().isoformat(),
            'chaos_engineering': 'REAL',
            'config_used': self.config
        }

    def save_results(self):
        """Save results to JSON file"""
        filename = f"academic_results_{self.pattern_name}_optimized.json"

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
        print("Usage: python academic_test_suite_optimized.py <pattern> <base_url>")
        print("Example: python academic_test_suite_optimized.py orchestrated http://localhost:3000")
        sys.exit(1)

    pattern_name = sys.argv[1].lower()
    base_url = sys.argv[2]

    if pattern_name not in ['orchestrated', 'choreographed']:
        print("Error: Pattern must be 'orchestrated' or 'choreographed'")
        sys.exit(1)

    # Create and run test suite
    test_suite = OptimizedAcademicTestSuite(base_url, pattern_name)
    test_suite.run_complete_test_suite()


if __name__ == "__main__":
    main()