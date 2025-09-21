#!/usr/bin/env python3
"""
Academic Test Suite - Orchestrated Pattern Only
"""

import json
import time
import statistics
import concurrent.futures
from datetime import datetime
import requests

class SimplifiedSagaTestSuite:
    def __init__(self, base_url, pattern_name):
        self.base_url = base_url
        self.pattern_name = pattern_name
        self.results = {
            'load_tests': [],
            'stress_tests': [],
            'concurrency_tests': [],
            'resilience_tests': [],
            'latency_distribution': []
        }

    def generate_order_payload(self, product_code="SMARTPHONE", unit_value=1500.0, quantity=1):
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
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/api/order",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            return {
                'success': response.status_code in [200, 201],
                'status_code': response.status_code,
                'duration_ms': duration_ms,
                'response_size': len(response.content),
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

    def percentile(self, data, percent):
        if not data:
            return 0
        data_sorted = sorted(data)
        k = (len(data_sorted) - 1) * percent / 100
        f = int(k)
        c = f + 1
        if c >= len(data_sorted):
            return data_sorted[-1]
        d0 = data_sorted[f] * (c - k)
        d1 = data_sorted[c] * (k - f)
        return d0 + d1

    def load_test_progressive(self, max_requests=100, step=20):
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
                time.sleep(0.05)

            end_time = time.time()
            total_duration = end_time - start_time
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
                    'latency_min_ms': min(durations),
                    'latency_max_ms': max(durations),
                    'latency_p95_ms': self.percentile(durations, 95),
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

    def concurrent_test(self, num_threads=8, requests_per_thread=5):
        print(f"\n=== CONCURRENT TEST - {self.pattern_name} ===")
        payload = self.generate_order_payload()
        all_results = []

        def worker_thread(thread_id):
            thread_results = []
            for i in range(requests_per_thread):
                result = self.execute_single_request(payload)
                result['thread_id'] = thread_id
                thread_results.append(result)
                time.sleep(0.1)
            return thread_results

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_thread = {executor.submit(worker_thread, i): i for i in range(num_threads)}
            for future in concurrent.futures.as_completed(future_to_thread):
                thread_results = future.result()
                all_results.extend(thread_results)

        end_time = time.time()
        total_duration = end_time - start_time
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
            'latency_p95_ms': self.percentile(durations, 95),
            'concurrency_level': num_threads,
            'timestamp': datetime.now().isoformat()
        }

        self.results['concurrency_tests'].append(concurrent_metrics)
        print(f"Concurrent result: {concurrent_metrics['latency_avg_ms']:.1f}ms avg, {concurrent_metrics['success_rate']:.1f}% success")
        return concurrent_metrics

    def resilience_test(self):
        print(f"\n=== RESILIENCE TEST - {self.pattern_name} ===")
        test_scenarios = [
            {'name': 'Normal Operation', 'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 1)},
            {'name': 'Inventory Overflow', 'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 999)},
            {'name': 'Invalid Product', 'payload': self.generate_order_payload("INVALID_PRODUCT", 1500.0, 1)},
            {'name': 'Zero Quantity', 'payload': self.generate_order_payload("SMARTPHONE", 1500.0, 0)},
            {'name': 'High Value Transaction', 'payload': self.generate_order_payload("LUXURY_ITEM", 50000.0, 1)},
        ]

        resilience_results = []
        for scenario in test_scenarios:
            print(f"Testing: {scenario['name']}")
            scenario_results = []
            for i in range(3):
                result = self.execute_single_request(scenario['payload'], timeout=45)
                scenario_results.append(result)
                time.sleep(1)

            successful = [r for r in scenario_results if r.get('success', False)]
            durations = [r['duration_ms'] for r in scenario_results]

            scenario_summary = {
                'scenario_name': scenario['name'],
                'iterations': len(scenario_results),
                'successful_iterations': len(successful),
                'success_rate': (len(successful) / len(scenario_results)) * 100,
                'avg_duration_ms': statistics.mean(durations),
                'timestamp': datetime.now().isoformat()
            }

            resilience_results.append(scenario_summary)
            print(f"  Result: {scenario_summary['success_rate']:.0f}% success, {scenario_summary['avg_duration_ms']:.1f}ms avg")

        self.results['resilience_tests'] = resilience_results
        return resilience_results

    def latency_distribution_analysis(self, num_samples=50):
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
            distribution_stats = {
                'sample_count': len(latencies),
                'mean_ms': statistics.mean(latencies),
                'median_ms': statistics.median(latencies),
                'std_dev_ms': statistics.stdev(latencies) if len(latencies) > 1 else 0,
                'min_ms': min(latencies),
                'max_ms': max(latencies),
                'p95_ms': self.percentile(latencies, 95),
                'p99_ms': self.percentile(latencies, 99),
                'coefficient_of_variation': statistics.stdev(latencies) / statistics.mean(latencies) if len(latencies) > 1 else 0,
                'timestamp': datetime.now().isoformat()
            }

            self.results['latency_distribution'] = distribution_stats
            print(f"Latency Distribution Summary:")
            print(f"  Mean: {distribution_stats['mean_ms']:.2f}ms")
            print(f"  Std Dev: {distribution_stats['std_dev_ms']:.2f}ms")
            print(f"  P95: {distribution_stats['p95_ms']:.2f}ms")
            return distribution_stats
        return None

    def run_comprehensive_test_suite(self):
        print(f"\n{'='*60}")
        print(f"COMPREHENSIVE ACADEMIC TEST SUITE - {self.pattern_name}")
        print(f"{'='*60}")

        load_results = self.load_test_progressive(max_requests=100, step=20)
        concurrent_results = self.concurrent_test(num_threads=8, requests_per_thread=5)
        resilience_results = self.resilience_test()
        distribution_results = self.latency_distribution_analysis(num_samples=50)

        comprehensive_results = {
            'pattern_name': self.pattern_name,
            'test_suite_version': '2.0_academic',
            'execution_timestamp': datetime.now().isoformat(),
            'test_results': self.results,
            'summary': {
                'load_test_peak_throughput': max([t.get('throughput_req_s', 0) for t in load_results]),
                'concurrent_max_throughput': concurrent_results.get('effective_throughput_req_s', 0),
                'resilience_overall_success_rate': statistics.mean([t.get('success_rate', 0) for t in resilience_results]),
                'latency_p95_ms': distribution_results.get('p95_ms', 0) if distribution_results else 0,
                'latency_avg_ms': distribution_results.get('mean_ms', 0) if distribution_results else 0,
                'latency_std_dev_ms': distribution_results.get('std_dev_ms', 0) if distribution_results else 0
            }
        }

        return comprehensive_results

def main():
    print("ACADEMIC TEST SUITE - ORCHESTRATED PATTERN")
    print("==========================================")

    # Test connectivity first
    import requests
    try:
        test_payload = {
            "products": [
                {
                    "product": {
                        "code": "SMARTPHONE",
                        "unitValue": 1500.0
                    },
                    "quantity": 1
                }
            ]
        }

        response = requests.post(
            "http://localhost:3000/api/order",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        if response.status_code not in [200, 201]:
            print(f"ERROR: Service not responding correctly (status: {response.status_code})")
            return

    except Exception as e:
        print(f"ERROR: Cannot connect to service - {str(e)}")
        print("Please ensure the Orchestrated Saga services are running on http://localhost:3000")
        return

    print("[OK] Orchestrated service is online and responding")

    # Execute comprehensive tests
    orchestrated_suite = SimplifiedSagaTestSuite("http://localhost:3000", "Orchestrated")
    orchestrated_results = orchestrated_suite.run_comprehensive_test_suite()

    # Save results
    with open("academic_results_orchestrated_final.json", "w") as f:
        json.dump(orchestrated_results, f, indent=2)

    # Print summary
    summary = orchestrated_results['summary']
    print(f"\n{'='*60}")
    print("ORCHESTRATED PATTERN - FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Peak Throughput: {summary['load_test_peak_throughput']:.2f} req/s")
    print(f"Concurrent Throughput: {summary['concurrent_max_throughput']:.2f} req/s")
    print(f"Average Latency: {summary['latency_avg_ms']:.2f}ms")
    print(f"P95 Latency: {summary['latency_p95_ms']:.2f}ms")
    print(f"Std Dev: {summary['latency_std_dev_ms']:.2f}ms")
    print(f"Resilience Success Rate: {summary['resilience_overall_success_rate']:.1f}%")
    print(f"\nResults saved to: academic_results_orchestrated_final.json")

if __name__ == "__main__":
    main()