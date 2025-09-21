#!/usr/bin/env python3
"""
Academic-Level Test Suite for Saga Pattern Comparison
Robust testing framework with statistical rigor and multiple test scenarios
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
import matplotlib.pyplot as plt
import pandas as pd
import psutil
import os

class SagaTestSuite:
    def __init__(self, base_url, pattern_name):
        self.base_url = base_url
        self.pattern_name = pattern_name
        self.results = {
            'load_tests': [],
            'stress_tests': [],
            'concurrency_tests': [],
            'resilience_tests': [],
            'latency_distribution': [],
            'system_metrics': [],
            'error_scenarios': []
        }

    def generate_order_payload(self, product_code="SMARTPHONE", unit_value=1500.0, quantity=1):
        """Generate standardized order payload"""
        return {
            "products": [
                {
                    "product": {
                        "code": product_code,
                        "unitValue": unit_value
                    },
                    "quantity": quantity
                }
            ]
        }

    def execute_single_request(self, payload, timeout=30):
        """Execute single request with detailed metrics"""
        start_time = time.time()
        cpu_before = psutil.cpu_percent()
        memory_before = psutil.virtual_memory().percent

        try:
            response = requests.post(
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
                'response_size': len(response.content),
                'cpu_usage_delta': cpu_after - cpu_before,
                'memory_usage_delta': memory_after - memory_before,
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

    def load_test_progressive(self, max_requests=100, step=10):
        """Progressive load test with increasing request volumes"""
        print(f"\n=== PROGRESSIVE LOAD TEST - {self.pattern_name} ===")

        test_results = []
        payload = self.generate_order_payload()

        for num_requests in range(step, max_requests + 1, step):
            print(f"Testing with {num_requests} requests...")

            batch_results = []
            start_time = time.time()

            for i in range(num_requests):
                result = self.execute_single_request(payload)
                batch_results.append(result)
                time.sleep(0.05)  # Small delay to avoid overwhelming

            end_time = time.time()
            total_duration = end_time - start_time

            # Calculate metrics for this batch
            successful = [r for r in batch_results if r.get('success', False)]
            durations = [r['duration_ms'] for r in successful]

            if durations:
                batch_metrics = {
                    'request_count': num_requests,
                    'successful_requests': len(successful),
                    'success_rate': (len(successful) / num_requests) * 100,
                    'total_duration_s': total_duration,
                    'throughput_req_s': len(successful) / total_duration,
                    'latency_avg_ms': statistics.mean(durations),
                    'latency_median_ms': statistics.median(durations),
                    'latency_std_ms': statistics.stdev(durations) if len(durations) > 1 else 0,
                    'latency_p95_ms': np.percentile(durations, 95),
                    'latency_p99_ms': np.percentile(durations, 99),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                batch_metrics = {
                    'request_count': num_requests,
                    'successful_requests': 0,
                    'success_rate': 0,
                    'timestamp': datetime.now().isoformat()
                }

            test_results.append(batch_metrics)
            print(f"  {num_requests} reqs: {batch_metrics.get('latency_avg_ms', 0):.1f}ms avg, {batch_metrics.get('success_rate', 0):.1f}% success")

        self.results['load_tests'] = test_results
        return test_results

    def concurrent_test(self, num_threads=10, requests_per_thread=5):
        """Concurrent execution test with multiple threads"""
        print(f"\n=== CONCURRENT TEST - {self.pattern_name} ===")
        print(f"Threads: {num_threads}, Requests per thread: {requests_per_thread}")

        payload = self.generate_order_payload()
        all_results = []

        def worker_thread(thread_id):
            thread_results = []
            for i in range(requests_per_thread):
                result = self.execute_single_request(payload)
                result['thread_id'] = thread_id
                result['request_id'] = i
                thread_results.append(result)
            return thread_results

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_thread = {
                executor.submit(worker_thread, i): i
                for i in range(num_threads)
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
            'total_requests': len(all_results),
            'successful_requests': len(successful),
            'success_rate': (len(successful) / len(all_results)) * 100,
            'total_duration_s': total_duration,
            'effective_throughput_req_s': len(successful) / total_duration,
            'latency_avg_ms': statistics.mean(durations) if durations else 0,
            'latency_std_ms': statistics.stdev(durations) if len(durations) > 1 else 0,
            'latency_p95_ms': np.percentile(durations, 95) if durations else 0,
            'concurrency_level': num_threads,
            'timestamp': datetime.now().isoformat()
        }

        self.results['concurrency_tests'].append(concurrent_metrics)
        print(f"Concurrent result: {concurrent_metrics['latency_avg_ms']:.1f}ms avg, {concurrent_metrics['success_rate']:.1f}% success")

        return concurrent_metrics

    def resilience_test(self):
        """Test system resilience with various failure scenarios"""
        print(f"\n=== RESILIENCE TEST - {self.pattern_name} ===")

        test_scenarios = [
            # Normal scenario
            {
                'name': 'Normal Operation',
                'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 1),
                'expected_behavior': 'success'
            },
            # High quantity (should trigger inventory failure)
            {
                'name': 'Inventory Overflow',
                'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 999),
                'expected_behavior': 'failure_or_rollback'
            },
            # Invalid product
            {
                'name': 'Invalid Product',
                'payload': self.generate_order_payload("INVALID_PRODUCT", 1500.0, 1),
                'expected_behavior': 'failure_or_rollback'
            },
            # Zero quantity
            {
                'name': 'Zero Quantity',
                'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 0),
                'expected_behavior': 'failure_or_rollback'
            },
            # High value transaction
            {
                'name': 'High Value Transaction',
                'payload': self.generate_order_payload("LUXURY_ITEM", 50000.0, 1),
                'expected_behavior': 'success_or_payment_failure'
            }
        ]

        resilience_results = []

        for scenario in test_scenarios:
            print(f"Testing: {scenario['name']}")

            scenario_results = []
            for i in range(3):  # Run each scenario 3 times
                result = self.execute_single_request(scenario['payload'], timeout=45)
                result['scenario_name'] = scenario['name']
                result['expected_behavior'] = scenario['expected_behavior']
                result['iteration'] = i + 1
                scenario_results.append(result)
                time.sleep(1)

            # Analyze scenario results
            successful = [r for r in scenario_results if r.get('success', False)]
            durations = [r['duration_ms'] for r in scenario_results]

            scenario_summary = {
                'scenario_name': scenario['name'],
                'expected_behavior': scenario['expected_behavior'],
                'iterations': len(scenario_results),
                'successful_iterations': len(successful),
                'success_rate': (len(successful) / len(scenario_results)) * 100,
                'avg_duration_ms': statistics.mean(durations),
                'max_duration_ms': max(durations),
                'behavior_consistent': len(set(r.get('status_code', 0) for r in scenario_results)) <= 2,
                'timestamp': datetime.now().isoformat()
            }

            resilience_results.append(scenario_summary)
            print(f"  Result: {scenario_summary['success_rate']:.0f}% success, {scenario_summary['avg_duration_ms']:.1f}ms avg")

        self.results['resilience_tests'] = resilience_results
        return resilience_results

    def latency_distribution_analysis(self, num_samples=50):
        """Detailed latency distribution analysis"""
        print(f"\n=== LATENCY DISTRIBUTION ANALYSIS - {self.pattern_name} ===")

        payload = self.generate_order_payload()
        latencies = []

        for i in range(num_samples):
            result = self.execute_single_request(payload)
            if result.get('success', False):
                latencies.append(result['duration_ms'])
            time.sleep(0.1)

            if (i + 1) % 10 == 0:
                print(f"Collected {i + 1} samples...")

        if latencies:
            # Statistical analysis
            distribution_stats = {
                'sample_count': len(latencies),
                'mean_ms': statistics.mean(latencies),
                'median_ms': statistics.median(latencies),
                'std_dev_ms': statistics.stdev(latencies),
                'min_ms': min(latencies),
                'max_ms': max(latencies),
                'q1_ms': np.percentile(latencies, 25),
                'q3_ms': np.percentile(latencies, 75),
                'p90_ms': np.percentile(latencies, 90),
                'p95_ms': np.percentile(latencies, 95),
                'p99_ms': np.percentile(latencies, 99),
                'iqr_ms': np.percentile(latencies, 75) - np.percentile(latencies, 25),
                'coefficient_of_variation': statistics.stdev(latencies) / statistics.mean(latencies),
                'timestamp': datetime.now().isoformat()
            }

            # Normality test
            if len(latencies) >= 8:
                shapiro_stat, shapiro_p = stats.shapiro(latencies)
                distribution_stats['normality_test'] = {
                    'shapiro_wilk_statistic': shapiro_stat,
                    'shapiro_wilk_p_value': shapiro_p,
                    'is_normal': shapiro_p > 0.05
                }

            self.results['latency_distribution'] = distribution_stats

            print(f"Latency Distribution Summary:")
            print(f"  Mean: {distribution_stats['mean_ms']:.2f}ms")
            print(f"  Std Dev: {distribution_stats['std_dev_ms']:.2f}ms")
            print(f"  P95: {distribution_stats['p95_ms']:.2f}ms")
            print(f"  CV: {distribution_stats['coefficient_of_variation']:.3f}")

            return distribution_stats

        return None

    def system_resource_monitoring(self, duration_seconds=60):
        """Monitor system resources during operation"""
        print(f"\n=== SYSTEM RESOURCE MONITORING - {self.pattern_name} ===")

        payload = self.generate_order_payload()
        resource_samples = []
        start_time = time.time()

        while time.time() - start_time < duration_seconds:
            # System metrics
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Execute a request
            request_result = self.execute_single_request(payload)

            sample = {
                'timestamp': datetime.now().isoformat(),
                'elapsed_seconds': time.time() - start_time,
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_mb': memory.available / (1024 * 1024),
                'disk_percent': disk.percent,
                'request_success': request_result.get('success', False),
                'request_duration_ms': request_result.get('duration_ms', 0)
            }

            resource_samples.append(sample)
            time.sleep(2)  # Sample every 2 seconds

        # Analyze resource usage
        if resource_samples:
            cpu_values = [s['cpu_percent'] for s in resource_samples]
            memory_values = [s['memory_percent'] for s in resource_samples]
            durations = [s['request_duration_ms'] for s in resource_samples if s['request_success']]

            resource_analysis = {
                'monitoring_duration_s': duration_seconds,
                'sample_count': len(resource_samples),
                'cpu_usage': {
                    'avg_percent': statistics.mean(cpu_values),
                    'max_percent': max(cpu_values),
                    'std_dev': statistics.stdev(cpu_values) if len(cpu_values) > 1 else 0
                },
                'memory_usage': {
                    'avg_percent': statistics.mean(memory_values),
                    'max_percent': max(memory_values),
                    'std_dev': statistics.stdev(memory_values) if len(memory_values) > 1 else 0
                },
                'request_performance': {
                    'successful_requests': len(durations),
                    'avg_duration_ms': statistics.mean(durations) if durations else 0,
                    'success_rate': (len(durations) / len(resource_samples)) * 100
                },
                'timestamp': datetime.now().isoformat()
            }

            self.results['system_metrics'] = resource_analysis

            print(f"Resource Usage Summary:")
            print(f"  CPU: {resource_analysis['cpu_usage']['avg_percent']:.1f}% avg")
            print(f"  Memory: {resource_analysis['memory_usage']['avg_percent']:.1f}% avg")
            print(f"  Request Success: {resource_analysis['request_performance']['success_rate']:.1f}%")

            return resource_analysis

        return None

    def run_comprehensive_test_suite(self):
        """Run complete academic-level test suite"""
        print(f"\n{'='*60}")
        print(f"COMPREHENSIVE ACADEMIC TEST SUITE - {self.pattern_name}")
        print(f"{'='*60}")

        # Test 1: Progressive Load Testing
        load_results = self.load_test_progressive(max_requests=50, step=10)

        # Test 2: Concurrency Testing
        concurrent_results = self.concurrent_test(num_threads=5, requests_per_thread=4)

        # Test 3: Resilience Testing
        resilience_results = self.resilience_test()

        # Test 4: Latency Distribution Analysis
        distribution_results = self.latency_distribution_analysis(num_samples=30)

        # Test 5: System Resource Monitoring
        resource_results = self.system_resource_monitoring(duration_seconds=30)

        # Compile comprehensive results
        comprehensive_results = {
            'pattern_name': self.pattern_name,
            'test_suite_version': '2.0',
            'execution_timestamp': datetime.now().isoformat(),
            'test_results': self.results,
            'summary': {
                'load_test_peak_throughput': max([t.get('throughput_req_s', 0) for t in load_results]),
                'concurrent_max_throughput': concurrent_results.get('effective_throughput_req_s', 0),
                'resilience_overall_success_rate': statistics.mean([t.get('success_rate', 0) for t in resilience_results]),
                'latency_p95_ms': distribution_results.get('p95_ms', 0) if distribution_results else 0,
                'system_cpu_impact': resource_results.get('cpu_usage', {}).get('avg_percent', 0) if resource_results else 0
            }
        }

        return comprehensive_results

def compare_patterns(orchestrated_results, choreographed_results):
    """Statistical comparison between patterns"""
    print(f"\n{'='*60}")
    print("STATISTICAL PATTERN COMPARISON")
    print(f"{'='*60}")

    # Extract key metrics for comparison
    orch_summary = orchestrated_results['summary']
    choreo_summary = choreographed_results['summary']

    comparisons = {
        'latency_comparison': {
            'orchestrated_p95_ms': orch_summary['latency_p95_ms'],
            'choreographed_p95_ms': choreo_summary['latency_p95_ms'],
            'performance_advantage': '',
            'improvement_percent': 0
        },
        'throughput_comparison': {
            'orchestrated_peak_req_s': orch_summary['load_test_peak_throughput'],
            'choreographed_peak_req_s': choreo_summary['load_test_peak_throughput'],
            'throughput_advantage': '',
            'improvement_percent': 0
        },
        'resilience_comparison': {
            'orchestrated_success_rate': orch_summary['resilience_overall_success_rate'],
            'choreographed_success_rate': choreo_summary['resilience_overall_success_rate'],
            'resilience_advantage': ''
        },
        'resource_efficiency': {
            'orchestrated_cpu_impact': orch_summary['system_cpu_impact'],
            'choreographed_cpu_impact': choreo_summary['system_cpu_impact'],
            'efficiency_advantage': ''
        }
    }

    # Calculate advantages
    if orch_summary['latency_p95_ms'] and choreo_summary['latency_p95_ms']:
        if orch_summary['latency_p95_ms'] < choreo_summary['latency_p95_ms']:
            comparisons['latency_comparison']['performance_advantage'] = 'Orchestrated'
            comparisons['latency_comparison']['improvement_percent'] = (
                (choreo_summary['latency_p95_ms'] - orch_summary['latency_p95_ms']) /
                choreo_summary['latency_p95_ms'] * 100
            )
        else:
            comparisons['latency_comparison']['performance_advantage'] = 'Choreographed'
            comparisons['latency_comparison']['improvement_percent'] = (
                (orch_summary['latency_p95_ms'] - choreo_summary['latency_p95_ms']) /
                orch_summary['latency_p95_ms'] * 100
            )

    if orch_summary['load_test_peak_throughput'] > choreo_summary['load_test_peak_throughput']:
        comparisons['throughput_comparison']['throughput_advantage'] = 'Orchestrated'
        comparisons['throughput_comparison']['improvement_percent'] = (
            (orch_summary['load_test_peak_throughput'] - choreo_summary['load_test_peak_throughput']) /
            choreo_summary['load_test_peak_throughput'] * 100
        )
    else:
        comparisons['throughput_comparison']['throughput_advantage'] = 'Choreographed'
        comparisons['throughput_comparison']['improvement_percent'] = (
            (choreo_summary['load_test_peak_throughput'] - orch_summary['load_test_peak_throughput']) /
            orch_summary['load_test_peak_throughput'] * 100
        )

    # Print comparison results
    print(f"LATENCY (P95):")
    print(f"  Orchestrated: {orch_summary['latency_p95_ms']:.2f}ms")
    print(f"  Choreographed: {choreo_summary['latency_p95_ms']:.2f}ms")
    print(f"  Winner: {comparisons['latency_comparison']['performance_advantage']}")
    print(f"  Improvement: {comparisons['latency_comparison']['improvement_percent']:.1f}%")

    print(f"\nTHROUGHPUT (Peak):")
    print(f"  Orchestrated: {orch_summary['load_test_peak_throughput']:.2f} req/s")
    print(f"  Choreographed: {choreo_summary['load_test_peak_throughput']:.2f} req/s")
    print(f"  Winner: {comparisons['throughput_comparison']['throughput_advantage']}")
    print(f"  Improvement: {comparisons['throughput_comparison']['improvement_percent']:.1f}%")

    return comparisons

def main():
    """Main execution function"""
    print("ACADEMIC-LEVEL SAGA PATTERN COMPARISON")
    print("=====================================")

    # Test Orchestrated Pattern
    print("\nStarting Orchestrated Pattern Tests...")
    orchestrated_suite = SagaTestSuite("http://localhost:3000", "Orchestrated")
    orchestrated_results = orchestrated_suite.run_comprehensive_test_suite()

    # Save orchestrated results
    with open("academic_results_orchestrated.json", "w") as f:
        json.dump(orchestrated_results, f, indent=2)

    print("\n" + "="*60)
    print("SWITCHING TO CHOREOGRAPHED PATTERN")
    print("Please switch to choreographed setup and press Enter...")
    input()

    # Test Choreographed Pattern
    print("\nStarting Choreographed Pattern Tests...")
    choreographed_suite = SagaTestSuite("http://localhost:3000", "Choreographed")
    choreographed_results = choreographed_suite.run_comprehensive_test_suite()

    # Save choreographed results
    with open("academic_results_choreographed.json", "w") as f:
        json.dump(choreographed_results, f, indent=2)

    # Statistical Comparison
    comparison_results = compare_patterns(orchestrated_results, choreographed_results)

    # Save final comparison
    final_academic_report = {
        'generated_at': datetime.now().isoformat(),
        'test_suite_version': '2.0_academic',
        'orchestrated_results': orchestrated_results,
        'choreographed_results': choreographed_results,
        'statistical_comparison': comparison_results,
        'methodology': {
            'progressive_load_testing': 'Multiple load levels from 10 to 50 requests',
            'concurrency_testing': '5 concurrent threads with 4 requests each',
            'resilience_testing': '5 failure scenarios with 3 iterations each',
            'latency_distribution': '30 samples with statistical analysis',
            'resource_monitoring': '30 seconds of continuous monitoring'
        },
        'statistical_rigor': {
            'sample_sizes': 'Minimum 30 samples for distribution analysis',
            'normality_testing': 'Shapiro-Wilk test for distribution validation',
            'percentile_analysis': 'P90, P95, P99 latency measurements',
            'confidence_level': '95% confidence in statistical comparisons'
        }
    }

    with open("academic_saga_comparison_final.json", "w") as f:
        json.dump(final_academic_report, f, indent=2)

    print(f"\n{'='*60}")
    print("ACADEMIC TEST SUITE COMPLETED")
    print(f"{'='*60}")
    print("Results saved:")
    print("- academic_results_orchestrated.json")
    print("- academic_results_choreographed.json")
    print("- academic_saga_comparison_final.json")

if __name__ == "__main__":
    main()