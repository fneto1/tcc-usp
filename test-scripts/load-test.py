#!/usr/bin/env python3
"""
Script de teste de carga para comparar Saga Orquestrado vs Coreografado
"""

import requests
import json
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import argparse

class SagaLoadTester:
    def __init__(self, base_url, pattern_name):
        self.base_url = base_url
        self.pattern_name = pattern_name
        self.results = []

    def create_order(self):
        """Executa uma única transação de pedido"""
        start_time = time.time()

        order_data = {
            "productId": "SMARTPHONE",
            "quantity": 1,
            "unitValue": 1500.0
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/orders",
                json=order_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            end_time = time.time()
            duration = (end_time - start_time) * 1000  # em ms

            return {
                "success": response.status_code == 200,
                "duration_ms": duration,
                "status_code": response.status_code,
                "timestamp": start_time
            }

        except Exception as e:
            end_time = time.time()
            duration = (end_time - start_time) * 1000

            return {
                "success": False,
                "duration_ms": duration,
                "error": str(e),
                "timestamp": start_time
            }

    def run_load_test(self, num_requests=50, num_threads=5):
        """Executa teste de carga com múltiplas threads"""
        print(f"Iniciando teste de carga - {self.pattern_name}")
        print(f"Requests: {num_requests}, Threads: {num_threads}")
        print("-" * 50)

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(self.create_order) for _ in range(num_requests)]
            results = [future.result() for future in futures]

        end_time = time.time()
        total_duration = end_time - start_time

        self.analyze_results(results, total_duration)

        return results

    def analyze_results(self, results, total_duration):
        """Analisa e exibe os resultados"""
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        if successful:
            durations = [r["duration_ms"] for r in successful]
            avg_duration = statistics.mean(durations)
            median_duration = statistics.median(durations)
            p95_duration = sorted(durations)[int(len(durations) * 0.95)]
        else:
            avg_duration = median_duration = p95_duration = 0

        throughput = len(successful) / total_duration if total_duration > 0 else 0
        success_rate = (len(successful) / len(results)) * 100

        print(f"\n=== RESULTADOS - {self.pattern_name} ===")
        print(f"Total de requests: {len(results)}")
        print(f"Sucessos: {len(successful)} ({success_rate:.1f}%)")
        print(f"Falhas: {len(failed)}")
        print(f"Duração total: {total_duration:.2f}s")
        print(f"Throughput: {throughput:.2f} req/s")
        print(f"Latência média: {avg_duration:.2f}ms")
        print(f"Latência mediana: {median_duration:.2f}ms")
        print(f"Latência P95: {p95_duration:.2f}ms")

        if failed:
            print(f"\nErros encontrados:")
            error_types = {}
            for f in failed[:5]:  # Mostra apenas os primeiros 5 erros
                error = f.get("error", f"HTTP {f.get('status_code', 'unknown')}")
                error_types[error] = error_types.get(error, 0) + 1

            for error, count in error_types.items():
                print(f"  - {error}: {count} ocorrências")

    def run_failure_test(self, service_name="payment"):
        """Testa recuperação de falhas"""
        print(f"\n=== TESTE DE FALHA - {service_name.upper()} ===")

        # Habilita simulação de falha
        try:
            requests.post(f"{self.base_url.replace(':3000', ':8091')}/api/test/simulate-failure?enable=true")
        except:
            pass

        # Executa transação que deve falhar
        start_time = time.time()
        result = self.create_order()

        print(f"Resultado: {'SUCESSO' if result['success'] else 'FALHA (esperado)'}")
        print(f"Duração: {result['duration_ms']:.2f}ms")

        # Desabilita simulação de falha
        try:
            requests.post(f"{self.base_url.replace(':3000', ':8091')}/api/test/simulate-failure?enable=false")
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description='Teste de carga para Saga patterns')
    parser.add_argument('--pattern', choices=['orchestrated', 'choreography'], required=True,
                       help='Padrão a ser testado')
    parser.add_argument('--requests', type=int, default=50,
                       help='Número de requests (default: 50)')
    parser.add_argument('--threads', type=int, default=5,
                       help='Número de threads (default: 5)')

    args = parser.parse_args()

    # URLs dos serviços
    urls = {
        'orchestrated': 'http://localhost:3000',
        'choreography': 'http://localhost:3000'
    }

    tester = SagaLoadTester(urls[args.pattern], args.pattern.title())

    # Teste de carga
    results = tester.run_load_test(args.requests, args.threads)

    # Teste de falha
    tester.run_failure_test()

    # Salva resultados em arquivo
    timestamp = int(time.time())
    filename = f"test_results_{args.pattern}_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump({
            'pattern': args.pattern,
            'timestamp': timestamp,
            'config': {
                'requests': args.requests,
                'threads': args.threads
            },
            'results': results
        }, f, indent=2)

    print(f"\nResultados salvos em: {filename}")

if __name__ == "__main__":
    main()