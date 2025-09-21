#!/usr/bin/env python3
"""
Teste simplificado para comparar performance dos padrões Saga
"""

import requests
import json
import time
import statistics
from datetime import datetime

class SimpleTestRunner:
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url

    def create_order(self):
        """Cria um pedido simples"""
        order_data = {
            "productId": "SMARTPHONE",
            "quantity": 1,
            "unitValue": 1500.0
        }

        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/api/orders",
                json=order_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            end_time = time.time()
            duration = (end_time - start_time) * 1000

            return {
                "success": response.status_code in [200, 201],
                "duration_ms": duration,
                "status_code": response.status_code,
                "response": response.text if response.status_code != 200 else "OK"
            }
        except Exception as e:
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            return {
                "success": False,
                "duration_ms": duration,
                "error": str(e)
            }

    def run_simple_load_test(self, num_requests=10):
        """Executa teste de carga simples"""
        print(f"\n=== TESTE DE CARGA - {self.name} ===")
        print(f"Executando {num_requests} requests...")

        results = []
        start_time = time.time()

        for i in range(num_requests):
            print(f"Request {i+1}/{num_requests}...", end=" ")
            result = self.create_order()
            results.append(result)
            print("OK" if result["success"] else f"ERRO ({result.get('status_code', 'timeout')})")
            time.sleep(0.5)  # Pequena pausa entre requests

        end_time = time.time()
        total_duration = end_time - start_time

        return self.analyze_results(results, total_duration)

    def analyze_results(self, results, total_duration):
        """Analisa resultados e retorna métricas"""
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        if successful:
            durations = [r["duration_ms"] for r in successful]
            avg_duration = statistics.mean(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            median_duration = statistics.median(durations)
        else:
            avg_duration = min_duration = max_duration = median_duration = 0

        throughput = len(successful) / total_duration if total_duration > 0 else 0
        success_rate = (len(successful) / len(results)) * 100 if results else 0

        metrics = {
            "pattern": self.name,
            "timestamp": datetime.now().isoformat(),
            "total_requests": len(results),
            "successful_requests": len(successful),
            "failed_requests": len(failed),
            "success_rate_percent": success_rate,
            "total_duration_seconds": total_duration,
            "throughput_req_per_sec": throughput,
            "latency_avg_ms": avg_duration,
            "latency_min_ms": min_duration,
            "latency_max_ms": max_duration,
            "latency_median_ms": median_duration
        }

        self.print_results(metrics)
        return metrics

    def print_results(self, metrics):
        """Imprime resultados formatados"""
        print(f"\n--- RESULTADOS {metrics['pattern'].upper()} ---")
        print(f"Total de requests: {metrics['total_requests']}")
        print(f"Sucessos: {metrics['successful_requests']} ({metrics['success_rate_percent']:.1f}%)")
        print(f"Falhas: {metrics['failed_requests']}")
        print(f"Duração total: {metrics['total_duration_seconds']:.2f}s")
        print(f"Throughput: {metrics['throughput_req_per_sec']:.2f} req/s")
        print(f"Latência média: {metrics['latency_avg_ms']:.0f}ms")
        print(f"Latência mediana: {metrics['latency_median_ms']:.0f}ms")
        print(f"Latência min/max: {metrics['latency_min_ms']:.0f}ms / {metrics['latency_max_ms']:.0f}ms")

def test_connectivity(url):
    """Testa conectividade com o serviço"""
    try:
        response = requests.get(f"{url}/actuator/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    # Testes para ambos os padrões
    tests = [
        ("Orquestrado", "http://localhost:3000"),
        ("Coreografado", "http://localhost:3000")  # Mesma porta, diferentes projetos
    ]

    all_results = []

    for pattern_name, url in tests:
        print(f"\n{'='*50}")
        print(f"TESTANDO PADRÃO: {pattern_name}")
        print(f"{'='*50}")

        if not test_connectivity(url):
            print(f"ERRO Servico {pattern_name} nao esta disponivel em {url}")
            print("Certifique-se de que o docker-compose está rodando")
            continue

        print(f"OK Servico {pattern_name} esta online")

        tester = SimpleTestRunner(pattern_name, url)
        results = tester.run_simple_load_test(10)
        all_results.append(results)

        input(f"\nPressione ENTER para continuar para o próximo teste...")

    # Gerar relatório comparativo
    if len(all_results) >= 2:
        generate_comparison_report(all_results)

    # Salvar resultados
    timestamp = int(time.time())
    filename = f"test_results_comparison_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\n📄 Resultados salvos em: {filename}")

def generate_comparison_report(results):
    """Gera relatório comparativo"""
    print(f"\n{'='*60}")
    print("RELATÓRIO COMPARATIVO")
    print(f"{'='*60}")

    if len(results) >= 2:
        orch = results[0] if "orquest" in results[0]["pattern"].lower() else results[1]
        chor = results[1] if "orquest" in results[0]["pattern"].lower() else results[0]

        print(f"\n📊 PERFORMANCE")
        print(f"Latência Média:")
        print(f"  • Orquestrado: {orch['latency_avg_ms']:.0f}ms")
        print(f"  • Coreografado: {chor['latency_avg_ms']:.0f}ms")
        diff_lat = ((chor['latency_avg_ms'] - orch['latency_avg_ms']) / orch['latency_avg_ms']) * 100
        print(f"  • Diferença: {diff_lat:+.1f}%")

        print(f"\nThroughput:")
        print(f"  • Orquestrado: {orch['throughput_req_per_sec']:.2f} req/s")
        print(f"  • Coreografado: {chor['throughput_req_per_sec']:.2f} req/s")
        diff_thr = ((chor['throughput_req_per_sec'] - orch['throughput_req_per_sec']) / orch['throughput_req_per_sec']) * 100
        print(f"  • Diferença: {diff_thr:+.1f}%")

        print(f"\n✅ CONFIABILIDADE")
        print(f"Taxa de Sucesso:")
        print(f"  • Orquestrado: {orch['success_rate_percent']:.1f}%")
        print(f"  • Coreografado: {chor['success_rate_percent']:.1f}%")

        print(f"\n🏆 VENCEDOR")
        if chor['latency_avg_ms'] < orch['latency_avg_ms']:
            print("  • Latência: Coreografado (mais rápido)")
        else:
            print("  • Latência: Orquestrado (mais rápido)")

        if chor['throughput_req_per_sec'] > orch['throughput_req_per_sec']:
            print("  • Throughput: Coreografado (maior)")
        else:
            print("  • Throughput: Orquestrado (maior)")

if __name__ == "__main__":
    main()