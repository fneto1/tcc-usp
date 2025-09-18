#!/usr/bin/env python3
"""
Gerador de Relatorio Comparativo - Saga Orquestrado vs Coreografado
"""

import json
from datetime import datetime

def load_results():
    """Carrega resultados dos testes"""
    try:
        with open("results_orchestrated_detailed.json", "r") as f:
            orchestrated = json.load(f)
    except FileNotFoundError:
        print("ERRO: Arquivo results_orchestrated_detailed.json nao encontrado")
        return None, None

    try:
        with open("results_choreography_detailed.json", "r") as f:
            choreography = json.load(f)
    except FileNotFoundError:
        print("ERRO: Arquivo results_choreography_detailed.json nao encontrado")
        return orchestrated, None

    return orchestrated, choreography

def generate_performance_comparison(orch, chor):
    """Gera comparacao de performance"""
    print("=" * 80)
    print("                      RELATORIO COMPARATIVO")
    print("           SAGA ORQUESTRADO vs SAGA COREOGRAFADO")
    print("=" * 80)

    print(f"\nMETRICAS DE PERFORMANCE")
    print("-" * 50)

    # Latencia
    orch_lat = orch["load_test"]["latency"]["avg_ms"]
    chor_lat = chor["load_test"]["latency"]["avg_ms"]
    lat_diff = ((chor_lat - orch_lat) / orch_lat) * 100 if orch_lat > 0 else 0

    print(f"Latencia Media:")
    print(f"  • Orquestrado:  {orch_lat:.1f}ms")
    print(f"  • Coreografado: {chor_lat:.1f}ms")
    print(f"  • Diferenca:    {lat_diff:+.1f}% ({'Coreografado mais rapido' if lat_diff < 0 else 'Orquestrado mais rapido'})")

    # Latencia P95
    orch_p95 = orch["load_test"]["latency"]["p95_ms"]
    chor_p95 = chor["load_test"]["latency"]["p95_ms"]

    print(f"\nLatencia P95 (95% das requests):")
    print(f"  • Orquestrado:  {orch_p95:.1f}ms")
    print(f"  • Coreografado: {chor_p95:.1f}ms")

    # Throughput
    orch_thr = orch["load_test"]["throughput_req_per_sec"]
    chor_thr = chor["load_test"]["throughput_req_per_sec"]
    thr_diff = ((chor_thr - orch_thr) / orch_thr) * 100 if orch_thr > 0 else 0

    print(f"\nThroughput:")
    print(f"  • Orquestrado:  {orch_thr:.2f} req/s")
    print(f"  • Coreografado: {chor_thr:.2f} req/s")
    print(f"  • Diferenca:    {thr_diff:+.1f}% ({'Coreografado superior' if thr_diff > 0 else 'Orquestrado superior'})")

    # Confiabilidade
    print(f"\nCONFIABILIDADE")
    print("-" * 50)
    print(f"Taxa de Sucesso:")
    print(f"  • Orquestrado:  {orch['load_test']['success_rate_percent']:.1f}%")
    print(f"  • Coreografado: {chor['load_test']['success_rate_percent']:.1f}%")

    print(f"\nRequests Processadas:")
    print(f"  • Orquestrado:  {orch['load_test']['successful_requests']}/{orch['load_test']['total_requests']}")
    print(f"  • Coreografado: {chor['load_test']['successful_requests']}/{chor['load_test']['total_requests']}")

    return {
        "latencia_vantagem": "Coreografado" if lat_diff < 0 else "Orquestrado",
        "latencia_diferenca_percent": abs(lat_diff),
        "throughput_vantagem": "Coreografado" if thr_diff > 0 else "Orquestrado",
        "throughput_diferenca_percent": abs(thr_diff)
    }

def generate_complexity_analysis():
    """Analise de complexidade baseada na implementacao"""
    print(f"\nANALISE DE COMPLEXIDADE")
    print("-" * 50)

    print("Implementacao:")
    print("  • Orquestrado:")
    print("    - Servico central (Orchestrator)")
    print("    - Logica de coordenacao centralizada")
    print("    - Matriz de mapeamento de fluxo")
    print("    - Controle explicito de estados")

    print("  • Coreografado:")
    print("    - Logica distribuida entre servicos")
    print("    - Cada servico gerencia seu proprio fluxo")
    print("    - Comunicacao direta via eventos")
    print("    - Autonomia de decisao descentralizada")

    print("\nManutenibilidade:")
    print("  • Orquestrado: ALTA - ponto central facilita debugs")
    print("  • Coreografado: MEDIA - logica distribuida mais complexa")

    print("\nObservabilidade:")
    print("  • Orquestrado: EXCELENTE - rastreamento centralizado")
    print("  • Coreografado: BOA - necessita correlacao de eventos")

def generate_use_cases():
    """Recomendacoes de uso"""
    print(f"\nRECOMENDACOES DE USO")
    print("-" * 50)

    print("Saga Orquestrado - Recomendado para:")
    print("  + Fluxos complexos com multiplas decisoes")
    print("  + Necessidade de auditoria detalhada")
    print("  + Equipes que precisam de visibilidade centralizada")
    print("  + Sistemas com SLA rigoroso de observabilidade")

    print("\nSaga Coreografado - Recomendado para:")
    print("  + Sistemas com alta demanda de performance")
    print("  + Arquiteturas verdadeiramente distribuidas")
    print("  + Fluxos lineares e previsíveis")
    print("  + Equipes com maturidade em sistemas distribuidos")

def generate_final_summary(comparison):
    """Resumo final com vencedores"""
    print(f"\nRESUMO EXECUTIVO")
    print("=" * 50)

    print("VENCEDORES POR CATEGORIA:")
    print(f"  • Performance (Latencia):  {comparison['latencia_vantagem']} ({comparison['latencia_diferenca_percent']:.1f}% melhor)")
    print(f"  • Performance (Throughput): {comparison['throughput_vantagem']} ({comparison['throughput_diferenca_percent']:.1f}% superior)")
    print(f"  • Observabilidade:         Orquestrado (ponto central)")
    print(f"  • Escalabilidade:          Coreografado (distribuido)")
    print(f"  • Simplicidade:            Orquestrado (logica centralizada)")

    print(f"\nCONCLUSAO:")
    if comparison['latencia_vantagem'] == 'Coreografado':
        print("  O padrao COREOGRAFADO demonstrou MELHOR PERFORMANCE")
        print("  O padrao ORQUESTRADO oferece MELHOR OBSERVABILIDADE")
    else:
        print("  O padrao ORQUESTRADO demonstrou MELHOR PERFORMANCE")
        print("  O padrao ORQUESTRADO oferece MELHOR OBSERVABILIDADE")

    print(f"\n  Para seu TCC: Ambos os padroes sao viaveis, com trade-offs claros")
    print(f"     entre performance vs observabilidade/manutenibilidade.")

def save_report_json(orch, chor, comparison):
    """Salva relatorio em JSON para analise posterior"""
    report = {
        "generated_at": datetime.now().isoformat(),
        "comparison": comparison,
        "orchestrated_results": orch,
        "choreography_results": chor,
        "conclusions": {
            "performance_winner": comparison['latencia_vantagem'],
            "observability_winner": "Orquestrado",
            "complexity_winner": "Orquestrado",
            "scalability_winner": "Coreografado"
        }
    }

    with open("relatorio_comparativo_final.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nRelatorio completo salvo em: relatorio_comparativo_final.json")

def main():
    orchestrated, choreography = load_results()

    if not orchestrated or not choreography:
        print("ERRO: Nao foi possivel carregar todos os resultados necessarios")
        return

    # Gerar comparacoes
    comparison = generate_performance_comparison(orchestrated, choreography)

    # Analises qualitativas
    generate_complexity_analysis()
    generate_use_cases()

    # Resumo final
    generate_final_summary(comparison)

    # Salvar relatorio JSON
    save_report_json(orchestrated, choreography, comparison)

    print(f"\n" + "=" * 80)
    print("RELATORIO CONCLUIDO - Dados prontos para seu TCC!")
    print("=" * 80)

if __name__ == "__main__":
    main()