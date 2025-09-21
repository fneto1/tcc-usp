#!/usr/bin/env python3
"""
Quick Test for Orchestrated Pattern
Simplified version to verify functionality
"""

import requests
import time
import json
from datetime import datetime

def test_orchestrated_pattern():
    base_url = "http://localhost:3000"

    print("=== QUICK ORCHESTRATED PATTERN TEST ===")
    print(f"Testing: {base_url}")

    # Test health check
    try:
        health_response = requests.get(f"{base_url}/actuator/health", timeout=5)
        print(f"✓ Health check: {health_response.status_code}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return

    # Test order creation
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

    results = []

    for i in range(5):
        print(f"\nTest {i+1}/5:")
        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/order",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            duration = time.time() - start_time

            result = {
                "test": i+1,
                "status_code": response.status_code,
                "duration_ms": duration * 1000,
                "timestamp": datetime.now().isoformat()
            }

            if response.status_code in [200, 201]:
                result["success"] = True
                print(f"  ✓ Success: {response.status_code} ({duration:.3f}s)")
            else:
                result["success"] = False
                print(f"  ✗ Failed: {response.status_code} ({duration:.3f}s)")
                print(f"  Response: {response.text[:100]}...")

            results.append(result)

        except Exception as e:
            print(f"  ✗ Exception: {e}")
            results.append({
                "test": i+1,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })

        time.sleep(1)  # Brief pause between tests

    # Save results
    with open("quick_test_results.json", "w") as f:
        json.dump({
            "test_run": datetime.now().isoformat(),
            "pattern": "orchestrated",
            "base_url": base_url,
            "results": results,
            "summary": {
                "total_tests": len(results),
                "successful": len([r for r in results if r.get("success", False)]),
                "avg_duration_ms": sum([r.get("duration_ms", 0) for r in results if "duration_ms" in r]) / len([r for r in results if "duration_ms" in r]) if results else 0
            }
        }, f, indent=2)

    # Print summary
    successful = len([r for r in results if r.get("success", False)])
    print(f"\n=== SUMMARY ===")
    print(f"Total tests: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Success rate: {successful/len(results)*100:.1f}%")
    print(f"Results saved to: quick_test_results.json")

if __name__ == "__main__":
    test_orchestrated_pattern()