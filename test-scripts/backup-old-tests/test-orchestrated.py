#!/usr/bin/env python3
import requests
import json
import time
import statistics
from datetime import datetime

def test_load(base_url, num_requests=20):
    """Teste de carga mais extenso"""
    print(f"\n=== TESTE DE CARGA SAGA ORQUESTRADO ===")
    print(f"Executando {num_requests} requests...")

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
    start_time = time.time()

    for i in range(num_requests):
        req_start = time.time()
        try:
            response = requests.post(
                f"{base_url}/api/order",
                json=order_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            req_end = time.time()
            duration = (req_end - req_start) * 1000

            success = response.status_code in [200, 201]
            if i % 5 == 0:
                print(f"Request {i+1}: {duration:.0f}ms - {'OK' if success else 'ERRO'}")

            results.append({
                "success": success,
                "duration_ms": duration,
                "status_code": response.status_code,
                "request_id": i+1
            })

        except Exception as e:
            req_end = time.time()
            duration = (req_end - req_start) * 1000
            results.append({
                "success": False,
                "duration_ms": duration,
                "error": str(e),
                "request_id": i+1
            })

        time.sleep(0.1)  # Pequena pausa

    end_time = time.time()
    total_duration = end_time - start_time

    return analyze_performance(results, total_duration)

def test_failure_scenario(base_url):
    """Teste de cenario de falha"""
    print(f"\n=== TESTE DE FALHA ===")

    # Tentar forcar falha com quantidade muito alta
    order_data = {
        "products": [
            {
                "product": {
                    "code": "SMARTPHONE",
                    "unitValue": 1500.0
                },
                "quantity": 999  # Quantidade alta para forcar falha
            }
        ]
    }

    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/api/order",
            json=order_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        end_time = time.time()
        duration = (end_time - start_time) * 1000

        print(f"Resultado: {response.status_code} em {duration:.0f}ms")
        print(f"Response: {response.text[:200]}...")

        return {
            "status_code": response.status_code,
            "duration_ms": duration,
            "response_length": len(response.text)
        }
    except Exception as e:
        print(f"Erro: {str(e)}")
        return {"error": str(e)}

def analyze_performance(results, total_duration):
    """Analisa performance detalhada"""
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    if successful:
        durations = [r["duration_ms"] for r in successful]
        avg_duration = statistics.mean(durations)
        median_duration = statistics.median(durations)
        min_duration = min(durations)
        max_duration = max(durations)
        # P95 - 95% das requests abaixo deste valor
        p95_duration = sorted(durations)[int(len(durations) * 0.95)] if durations else 0
    else:
        avg_duration = median_duration = min_duration = max_duration = p95_duration = 0

    success_rate = (len(successful) / len(results)) * 100 if results else 0
    throughput = len(successful) / total_duration if total_duration > 0 else 0

    metrics = {
        "timestamp": datetime.now().isoformat(),
        "pattern": "Orquestrado",
        "total_requests": len(results),
        "successful_requests": len(successful),
        "failed_requests": len(failed),
        "success_rate_percent": success_rate,
        "total_duration_seconds": total_duration,
        "throughput_req_per_sec": throughput,
        "latency": {
            "avg_ms": avg_duration,
            "median_ms": median_duration,
            "min_ms": min_duration,
            "max_ms": max_duration,
            "p95_ms": p95_duration
        }
    }

    print(f"\n--- METRICAS ORQUESTRADO ---")
    print(f"Total de requests: {metrics['total_requests']}")
    print(f"Sucessos: {metrics['successful_requests']} ({metrics['success_rate_percent']:.1f}%)")
    print(f"Falhas: {metrics['failed_requests']}")
    print(f"Duracao total: {metrics['total_duration_seconds']:.2f}s")
    print(f"Throughput: {metrics['throughput_req_per_sec']:.2f} req/s")
    print(f"Latencia media: {metrics['latency']['avg_ms']:.0f}ms")
    print(f"Latencia mediana: {metrics['latency']['median_ms']:.0f}ms")
    print(f"Latencia P95: {metrics['latency']['p95_ms']:.0f}ms")
    print(f"Latencia min/max: {metrics['latency']['min_ms']:.0f}ms / {metrics['latency']['max_ms']:.0f}ms")

    return metrics

def get_system_metrics(base_url):
    """Coleta metricas do sistema"""
    try:
        # Memoria do JVM
        response = requests.get(f"{base_url}/actuator/metrics/jvm.memory.used", timeout=5)
        if response.status_code == 200:
            memory_data = response.json()
            memory_mb = memory_data.get("measurements", [{}])[0].get("value", 0) / 1024 / 1024
        else:
            memory_mb = 0

        # Health check
        health_response = requests.get(f"{base_url}/actuator/health", timeout=5)
        health_status = health_response.json().get("status", "UNKNOWN") if health_response.status_code == 200 else "DOWN"

        return {
            "memory_used_mb": memory_mb,
            "health_status": health_status
        }
    except:
        return {"memory_used_mb": 0, "health_status": "UNKNOWN"}

def main():
    base_url = "http://localhost:3000"

    # Verificar conectividade
    try:
        health = requests.get(f"{base_url}/actuator/health", timeout=5)
        if health.status_code != 200:
            print("ERRO: Servico nao esta disponivel")
            return
    except:
        print("ERRO: Nao foi possivel conectar ao servico")
        return

    print("OK Servico esta online")

    # Teste de carga
    load_results = test_load(base_url, 20)

    # Teste de falha
    failure_results = test_failure_scenario(base_url)

    # Metricas do sistema
    system_metrics = get_system_metrics(base_url)

    # Compilar resultados
    final_results = {
        "pattern": "Orquestrado",
        "timestamp": datetime.now().isoformat(),
        "load_test": load_results,
        "failure_test": failure_results,
        "system_metrics": system_metrics
    }

    # Salvar em arquivo
    with open("results_orchestrated_detailed.json", "w") as f:
        json.dump(final_results, f, indent=2)

    print(f"\n=== SISTEMA ===")
    print(f"Memoria JVM: {system_metrics['memory_used_mb']:.1f}MB")
    print(f"Status: {system_metrics['health_status']}")

    print(f"\nResultados detalhados salvos em: results_orchestrated_detailed.json")

if __name__ == "__main__":
    main()