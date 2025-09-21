#!/usr/bin/env python3
"""
Simplified Orchestrated Test - Working Version
"""

import requests
import json
import time
from datetime import datetime

def run_orchestrated_test():
    print("Starting Orchestrated Pattern Test")
    print("=" * 50)

    base_url = "http://localhost:3000"

    # Test payload
    payload = {
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

    results = {
        "pattern": "orchestrated",
        "start_time": datetime.now().isoformat(),
        "runs": []
    }

    # Execute 20 runs
    for run in range(1, 21):
        print(f"\nRUN {run}/20")
        print("-" * 30)

        run_results = []

        # 3 scenarios per run
        scenarios = [
            {"name": "baseline", "description": "Normal conditions"},
            {"name": "medium_stress", "description": "Medium stress"},
            {"name": "high_stress", "description": "High stress"}
        ]

        for scenario in scenarios:
            print(f"Testing {scenario['name']}...")

            scenario_start = time.time()

            # Execute 10 requests for this scenario
            successful_requests = 0
            total_duration = 0

            for req in range(10):
                try:
                    req_start = time.time()
                    response = requests.post(
                        f"{base_url}/api/order",
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                    req_end = time.time()
                    req_duration = req_end - req_start

                    if response.status_code in [200, 201]:
                        successful_requests += 1
                        total_duration += req_duration

                except Exception as e:
                    print(f"  Request {req+1} failed: {e}")

            scenario_end = time.time()
            scenario_duration = scenario_end - scenario_start

            scenario_result = {
                "scenario": scenario["name"],
                "requests": 10,
                "successful": successful_requests,
                "success_rate": successful_requests / 10,
                "avg_response_time": total_duration / max(successful_requests, 1),
                "total_duration": scenario_duration
            }

            run_results.append(scenario_result)
            print(f"  Success: {successful_requests}/10 ({successful_requests/10*100:.1f}%)")

        results["runs"].append({
            "run_number": run,
            "scenarios": run_results,
            "timestamp": datetime.now().isoformat()
        })

        # Save intermediate results
        with open("simple_orchestrated_results.json", "w") as f:
            json.dump(results, f, indent=2)

    results["end_time"] = datetime.now().isoformat()

    # Final save
    with open("simple_orchestrated_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nTest completed!")
    print(f"Results saved to: simple_orchestrated_results.json")

if __name__ == "__main__":
    run_orchestrated_test()