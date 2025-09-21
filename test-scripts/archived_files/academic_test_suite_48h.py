#!/usr/bin/env python3
"""
Academic Test Suite - Optimized for 48h Execution
Scientific rigor with time-optimized execution
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


class Academic48hTestSuite:
    def __init__(self, base_url, pattern_name):
        self.base_url = base_url
        self.pattern_name = pattern_name
        # Using real chaos engineering controller
        self.real_chaos = real_chaos

        # Optimized for realistic high-load simulation
        self.config = {
            'runs_per_scenario': 20,     # statistically valid
            'load_test_requests': 1000,  # high load testing
            'concurrent_users': 50,      # realistic high concurrency
            'test_timeout': 60,          # more time for complex processing
            'scenarios': ['baseline', 'medium_stress', 'high_stress', 'extreme_stress']
        }

        self.results = {
            'pattern_name': pattern_name,
            'test_suite_version': '48h_optimized',
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
                    {"product": {"code": "HEADPHONE", "unitValue": 1500.0}, "quantity": 3},
                    {"product": {"code": "KEYBOARD", "unitValue": 3000.0}, "quantity": 1},
                    {"product": {"code": "TABLET", "unitValue": 800.0}, "quantity": 2}
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
                f"{getattr(self, 'proxy_url', self.base_url)}/api/order",
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
                'response_size': len(response.content),
                'cpu_delta': cpu_after - cpu_before,
                'memory_delta': memory_after - memory_before,
                'timestamp': datetime.now().isoformat()
            }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'duration_ms': timeout * 1000,
                'error': 'timeout',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            return {
                'success': False,
                'duration_ms': duration_ms,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def optimized_load_test(self, scenario_name, num_requests=200):
        """Optimized load test for 48h execution"""
        print(f"  [DATA] Load Test: {num_requests} requests")

        payload = self.generate_order_payload("COMPLEX")
        results = []

        # Use thread pool for faster execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['concurrent_users']) as executor:
            start_time = time.time()

            # Submit all requests
            futures = []
            for i in range(num_requests):
                future = executor.submit(self.execute_single_request, payload)
                futures.append(future)
                time.sleep(0.01)  # Small delay to avoid overwhelming

            # Collect results
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        'success': False,
                        'error': str(e),
                        'duration_ms': 0,
                        'timestamp': datetime.now().isoformat()
                    })

            end_time = time.time()
            total_duration = end_time - start_time

        # Analyze results
        successful = [r for r in results if r.get('success', False)]
        durations = [r['duration_ms'] for r in successful]

        if durations:
            load_metrics = {
                'scenario': scenario_name,
                'total_requests': num_requests,
                'successful_requests': len(successful),
                'success_rate': len(successful) / num_requests,
                'total_duration_s': total_duration,
                'throughput_req_s': len(successful) / total_duration,
                'latency_stats': {
                    'mean_ms': statistics.mean(durations),
                    'median_ms': statistics.median(durations),
                    'std_dev_ms': statistics.stdev(durations) if len(durations) > 1 else 0,
                    'min_ms': min(durations),
                    'max_ms': max(durations),
                    'p95_ms': np.percentile(durations, 95),
                    'p99_ms': np.percentile(durations, 99)
                },
                'timestamp': datetime.now().isoformat()
            }
        else:
            load_metrics = {
                'scenario': scenario_name,
                'total_requests': num_requests,
                'successful_requests': 0,
                'success_rate': 0,
                'error': 'No successful requests',
                'timestamp': datetime.now().isoformat()
            }

        return load_metrics

    def concurrent_stress_test(self, scenario_name):
        """Concurrent execution stress test"""
        print(f"  [PROCESS] Concurrent Test: {self.config['concurrent_users']} threads")

        payload = self.generate_order_payload("COMPLEX")
        all_results = []
        requests_per_thread = 10

        def worker_thread(thread_id):
            thread_results = []
            for i in range(requests_per_thread):
                result = self.execute_single_request(payload)
                result['thread_id'] = thread_id
                result['request_id'] = i
                thread_results.append(result)
                time.sleep(0.1)
            return thread_results

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['concurrent_users']) as executor:
            future_to_thread = {
                executor.submit(worker_thread, i): i
                for i in range(self.config['concurrent_users'])
            }

            for future in concurrent.futures.as_completed(future_to_thread):
                thread_results = future.result()
                all_results.extend(thread_results)

        end_time = time.time()
        total_duration = end_time - start_time

        # Analyze concurrent results
        successful = [r for r in all_results if r.get('success', False)]
        durations = [r['duration_ms'] for r in successful]

        concurrent_metrics = {
            'scenario': scenario_name,
            'total_requests': len(all_results),
            'successful_requests': len(successful),
            'success_rate': len(successful) / len(all_results) if all_results else 0,
            'total_duration_s': total_duration,
            'effective_throughput_req_s': len(successful) / total_duration if total_duration > 0 else 0,
            'concurrency_level': self.config['concurrent_users'],
            'latency_stats': {
                'mean_ms': statistics.mean(durations) if durations else 0,
                'std_dev_ms': statistics.stdev(durations) if len(durations) > 1 else 0,
                'p95_ms': np.percentile(durations, 95) if durations else 0
            },
            'timestamp': datetime.now().isoformat()
        }

        return concurrent_metrics

    def resilience_failure_test(self, scenario_name):
        """Test system resilience with failure scenarios"""
        print(f"  [SHIELD] Resilience Test: Multiple failure conditions")

        failure_scenarios = [
            {
                'name': 'Normal Operation',
                'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 1)
            },
            {
                'name': 'Inventory Overflow',
                'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 999)
            },
            {
                'name': 'Invalid Product',
                'payload': self.generate_order_payload("INVALID_PRODUCT", 1500.0, 1)
            },
            {
                'name': 'Zero Quantity',
                'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 0)
            }
        ]

        resilience_results = {}

        for failure_scenario in failure_scenarios:
            scenario_results = []

            # 5 runs per failure scenario (vs 15 for time optimization)
            for i in range(5):
                result = self.execute_single_request(failure_scenario['payload'], timeout=45)
                result['failure_scenario'] = failure_scenario['name']
                result['iteration'] = i + 1
                scenario_results.append(result)
                time.sleep(0.5)

            # Analyze failure scenario
            successful = [r for r in scenario_results if r.get('success', False)]
            durations = [r['duration_ms'] for r in scenario_results]

            resilience_results[failure_scenario['name']] = {
                'iterations': len(scenario_results),
                'successful_iterations': len(successful),
                'success_rate': len(successful) / len(scenario_results),
                'avg_duration_ms': statistics.mean(durations) if durations else 0,
                'max_duration_ms': max(durations) if durations else 0,
                'consistent_behavior': len(set(r.get('status_code', 0) for r in scenario_results)) <= 2,
                'timestamp': datetime.now().isoformat()
            }

        return resilience_results

    def run_scenario_test_suite(self, scenario_name):
        """Run complete test suite for a specific chaos scenario"""
        print(f"\n[TEST] Testing Scenario: {scenario_name.upper()}")
        print("=" * 60)

        # Apply chaos scenario
        chaos_result = self.real_chaos.apply_scenario(scenario_name)

        # Wait for system to stabilize under chaos conditions
        print("[WAIT] Waiting for system stabilization (30s)...")
        time.sleep(30)

        scenario_results = {
            'scenario_name': scenario_name,
            'chaos_config': chaos_result,
            'tests': {},
            'execution_start': datetime.now().isoformat()
        }

        try:
            # Test 1: Load Testing
            print("[START] Running Load Test...")
            scenario_results['tests']['load_test'] = self.optimized_load_test(
                scenario_name,
                self.config['load_test_requests']
            )

            # Test 2: Concurrent Stress Testing
            print("[PROCESS] Running Concurrent Stress Test...")
            scenario_results['tests']['concurrent_test'] = self.concurrent_stress_test(scenario_name)

            # Test 3: Resilience Testing
            print("[SHIELD] Running Resilience Test...")
            scenario_results['tests']['resilience_test'] = self.resilience_failure_test(scenario_name)

            scenario_results['execution_end'] = datetime.now().isoformat()

            # Log scenario summary
            load_success = scenario_results['tests']['load_test'].get('success_rate', 0)
            concurrent_success = scenario_results['tests']['concurrent_test'].get('success_rate', 0)

            print(f"\n[STATS] Scenario Summary:")
            print(f"   Load Test Success Rate: {load_success:.1%}")
            print(f"   Concurrent Test Success Rate: {concurrent_success:.1%}")
            print(f"   Chaos Conditions: {chaos_result['config']['description']}")

        except Exception as e:
            print(f"[ERROR] Error during scenario testing: {e}")
            scenario_results['error'] = str(e)
            scenario_results['execution_end'] = datetime.now().isoformat()

        finally:
            # Clear chaos conditions
            print("[CLEAN] Clearing chaos conditions...")
            self.real_chaos.clear_chaos()
            time.sleep(10)  # Recovery time

        return scenario_results

    def run_complete_pattern_test(self):
        """Run complete test suite for this pattern"""
        print(f"\n{'='*80}")
        print(f"[TARGET] ACADEMIC 48H TEST SUITE - {self.pattern_name.upper()} PATTERN")
        print(f"{'='*80}")
        print(f"Configuration:")
        print(f"  Runs per scenario: {self.config['runs_per_scenario']}")
        print(f"  Load test requests: {self.config['load_test_requests']}")
        print(f"  Concurrent users: {self.config['concurrent_users']}")
        print(f"  Scenarios: {', '.join(self.config['scenarios'])}")

        # Setup REAL chaos engineering
        print("\n[SETUP] Setting up REAL Chaos Engineering...")
        print("[OK] Real chaos controller initialized")

        # Run tests for each scenario
        for run_number in range(self.config['runs_per_scenario']):
            print(f"\n[PROCESS] RUN {run_number + 1}/{self.config['runs_per_scenario']}")
            print("-" * 60)

            for scenario in self.config['scenarios']:
                scenario_key = f"{scenario}_run_{run_number + 1}"

                try:
                    # Apply REAL chaos for this scenario
                    real_chaos.apply_scenario(scenario)

                    scenario_result = self.run_scenario_test_suite(scenario)
                    self.results['scenarios'][scenario_key] = scenario_result

                    # Save intermediate results
                    self._save_intermediate_results()

                except Exception as e:
                    print(f"[ERROR] Failed scenario {scenario} run {run_number + 1}: {e}")
                    self.results['scenarios'][scenario_key] = {
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }

        # Calculate final statistics
        self._calculate_summary_statistics()

        # Cleanup
        self.real_chaos.clear_chaos()

        # Mark completion
        self.results['execution_end'] = datetime.now().isoformat()
        self.results['total_duration_minutes'] = self._calculate_total_duration()

        print(f"\n[OK] {self.pattern_name} Pattern Testing Complete!")
        print(f"   Total Duration: {self.results['total_duration_minutes']:.1f} minutes")
        print(f"   Total Scenarios Tested: {len(self.results['scenarios'])}")

        return self.results

    def _save_intermediate_results(self):
        """Save intermediate results during execution"""
        filename = f"intermediate_results_{self.pattern_name.lower()}.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(self.results, f, indent=2)
        except Exception as e:
            print(f"[WARN] Failed to save intermediate results: {e}")

    def _calculate_summary_statistics(self):
        """Calculate comprehensive summary statistics"""
        print("\n[DATA] Calculating Summary Statistics...")

        # Collect all successful tests by scenario type
        load_tests = []
        concurrent_tests = []

        for scenario_key, scenario_data in self.results['scenarios'].items():
            if 'tests' in scenario_data:
                if 'load_test' in scenario_data['tests']:
                    load_tests.append(scenario_data['tests']['load_test'])
                if 'concurrent_test' in scenario_data['tests']:
                    concurrent_tests.append(scenario_data['tests']['concurrent_test'])

        # Calculate load test statistics
        if load_tests:
            success_rates = [t.get('success_rate', 0) for t in load_tests]
            throughputs = [t.get('throughput_req_s', 0) for t in load_tests]
            latencies = [t.get('latency_stats', {}).get('mean_ms', 0) for t in load_tests]

            self.results['summary_stats']['load_tests'] = {
                'total_tests': len(load_tests),
                'avg_success_rate': statistics.mean(success_rates),
                'avg_throughput_req_s': statistics.mean(throughputs),
                'avg_latency_ms': statistics.mean(latencies),
                'max_throughput_req_s': max(throughputs),
                'min_latency_ms': min(latencies),
                'latency_std_dev': statistics.stdev(latencies) if len(latencies) > 1 else 0
            }

        # Calculate concurrent test statistics
        if concurrent_tests:
            success_rates = [t.get('success_rate', 0) for t in concurrent_tests]
            throughputs = [t.get('effective_throughput_req_s', 0) for t in concurrent_tests]

            self.results['summary_stats']['concurrent_tests'] = {
                'total_tests': len(concurrent_tests),
                'avg_success_rate': statistics.mean(success_rates),
                'avg_throughput_req_s': statistics.mean(throughputs),
                'max_throughput_req_s': max(throughputs)
            }

        # Overall pattern performance
        if load_tests:
            all_latencies = []
            for test in load_tests:
                if 'latency_stats' in test:
                    all_latencies.append(test['latency_stats'].get('mean_ms', 0))

            if all_latencies:
                self.results['summary_stats']['overall_performance'] = {
                    'pattern_name': self.pattern_name,
                    'avg_latency_ms': statistics.mean(all_latencies),
                    'median_latency_ms': statistics.median(all_latencies),
                    'latency_std_dev_ms': statistics.stdev(all_latencies) if len(all_latencies) > 1 else 0,
                    'coefficient_of_variation': (statistics.stdev(all_latencies) / statistics.mean(all_latencies)) if statistics.mean(all_latencies) > 0 else 0
                }

    def _calculate_total_duration(self):
        """Calculate total test duration in minutes"""
        try:
            start_time = datetime.fromisoformat(self.results['execution_start'])
            end_time = datetime.fromisoformat(self.results['execution_end'])
            duration = (end_time - start_time).total_seconds() / 60
            return duration
        except:
            return 0


def main():
    """Main execution function for testing individual patterns"""
    import sys

    if len(sys.argv) != 3:
        print("Usage: python academic_test_suite_48h.py <pattern_name> <base_url>")
        print("Example: python academic_test_suite_48h.py orchestrated http://localhost:3000")
        sys.exit(1)

    pattern_name = sys.argv[1]
    base_url = sys.argv[2]

    print(f"Starting Academic 48h Test Suite for {pattern_name}")

    # Create test suite
    test_suite = Academic48hTestSuite(base_url, pattern_name)

    # Run complete test
    results = test_suite.run_complete_pattern_test()

    # Save final results
    output_filename = f"academic_results_{pattern_name.lower()}_48h.json"
    with open(output_filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[TARGET] Results saved to: {output_filename}")
    print("=" * 80)


if __name__ == "__main__":
    main()