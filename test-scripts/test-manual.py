#!/usr/bin/env python3
import requests
import json
import time
import statistics

def test_order_creation(base_url, num_requests=5):
    """Testa criacao de pedidos"""
    print(f"Testando {base_url} com {num_requests} requests...")

    order_data = {
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

    for i in range(num_requests):
        start_time = time.time()
        try:
            response = requests.post(
                f"{base_url}/api/order",
                json=order_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            end_time = time.time()
            duration = (end_time - start_time) * 1000

            success = response.status_code in [200, 201]
            print(f"Request {i+1}: {duration:.0f}ms - {'OK' if success else 'ERRO'}")

            results.append({
                "success": success,
                "duration_ms": duration,
                "status_code": response.status_code
            })

        except Exception as e:
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            print(f"Request {i+1}: {duration:.0f}ms - ERRO: {str(e)}")
            results.append({
                "success": False,
                "duration_ms": duration,
                "error": str(e)
            })

        time.sleep(1)  # Pausa entre requests

    return analyze_results(results)

def analyze_results(results):
    """Analisa resultados"""
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    if successful:
        durations = [r["duration_ms"] for r in successful]
        avg_duration = statistics.mean(durations)
        min_duration = min(durations)
        max_duration = max(durations)
    else:
        avg_duration = min_duration = max_duration = 0

    success_rate = (len(successful) / len(results)) * 100 if results else 0

    print(f"\n--- RESULTADOS ---")
    print(f"Total: {len(results)}")
    print(f"Sucessos: {len(successful)} ({success_rate:.1f}%)")
    print(f"Falhas: {len(failed)}")
    print(f"Latencia media: {avg_duration:.0f}ms")
    print(f"Latencia min/max: {min_duration:.0f}ms / {max_duration:.0f}ms")

    return {
        "total": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "success_rate": success_rate,
        "avg_latency": avg_duration,
        "min_latency": min_duration,
        "max_latency": max_duration
    }

def main():
    print("=== TESTE SAGA ORQUESTRADO ===")
    orch_results = test_order_creation("http://localhost:3000", 5)

    # Salvar resultados
    with open("test_results_orchestrated.json", "w") as f:
        json.dump(orch_results, f, indent=2)

    print(f"\nResultados salvos em test_results_orchestrated.json")

if __name__ == "__main__":
    main()