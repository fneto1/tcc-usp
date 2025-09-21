# Documentação Completa dos Testes Executados

## Visão Geral

Esta documentação detalha todos os testes executados para comparação entre os padrões Saga Orquestrado e Saga Coreografado, incluindo metodologia, configurações, execução e resultados obtidos.

## 1. Ambiente de Teste

### 1.1 Configuração do Sistema
- **Sistema Operacional**: Windows 11
- **Runtime**: Java 17, Python 3.x
- **Containers**: Docker Desktop com Docker Compose
- **Data/Hora**: 18 de setembro de 2025, 00:12-00:14

### 1.2 Arquitetura dos Serviços
- **Saga Orquestrado**: http://localhost:3000
- **Saga Coreografado**: http://localhost:3000
- **Banco de Dados**: PostgreSQL (Inventory, Payment), MongoDB (Order)
- **Message Broker**: Apache Kafka
- **Padrão Outbox**: Implementado em todos os serviços

## 2. Testes Implementados

### 2.1 Teste de Carga (Load Test)

#### 2.1.1 Descrição
Teste de performance com múltiplas requisições sequenciais para medir latência, throughput e taxa de sucesso.

#### 2.1.2 Configuração
```json
{
  "numero_requests": 20,
  "payload": {
    "products": [
      {
        "product": {
          "code": "SMARTPHONE",
          "unitValue": 1500.0
        },
        "quantity": 1
      }
    ]
  },
  "timeout": 30,
  "intervalo_entre_requests": 0.1
}
```

#### 2.1.3 Métricas Coletadas
- Latência média, mediana, mínima, máxima e P95
- Throughput (requisições por segundo)
- Taxa de sucesso (%)
- Duração total do teste

#### 2.1.4 Resultados - Saga Orquestrado
```json
{
  "timestamp": "2025-09-18T00:12:56.866361",
  "total_requests": 20,
  "successful_requests": 20,
  "failed_requests": 0,
  "success_rate_percent": 100.0,
  "total_duration_seconds": 2.338855266571045,
  "throughput_req_per_sec": 8.551191809881272,
  "latency": {
    "avg_ms": 16.25267267227173,
    "median_ms": 14.615535736083984,
    "min_ms": 8.008241653442383,
    "max_ms": 31.403064727783203,
    "p95_ms": 31.403064727783203
  }
}
```

#### 2.1.5 Resultados - Saga Coreografado
```json
{
  "timestamp": "2025-09-18T00:14:22.029817",
  "total_requests": 20,
  "successful_requests": 20,
  "failed_requests": 0,
  "success_rate_percent": 100.0,
  "total_duration_seconds": 2.4315407276153564,
  "throughput_req_per_sec": 8.225237510051604,
  "latency": {
    "avg_ms": 20.76045274734497,
    "median_ms": 21.98171615600586,
    "min_ms": 9.44662094116211,
    "max_ms": 34.55042839050293,
    "p95_ms": 34.55042839050293
  }
}
```

### 2.2 Teste de Falha (Failure Test)

#### 2.2.1 Descrição
Teste para verificar o comportamento do sistema em cenários de falha simulada, usando quantidade alta de produtos para forçar falha no serviço de inventário.

#### 2.2.2 Configuração
```json
{
  "payload_falha": {
    "products": [
      {
        "product": {
          "code": "SMARTPHONE",
          "unitValue": 1500.0
        },
        "quantity": 999
      }
    ]
  },
  "timeout": 30
}
```

#### 2.2.3 Resultados - Saga Orquestrado
```json
{
  "status_code": 200,
  "duration_ms": 24.965524673461914,
  "response_length": 263
}
```

#### 2.2.4 Resultados - Saga Coreografado
```json
{
  "status_code": 200,
  "duration_ms": 22.52340316772461,
  "response_length": 263
}
```

### 2.3 Teste de Métricas do Sistema

#### 2.3.1 Descrição
Coleta de métricas básicas de sistema para verificar disponibilidade e responsividade dos serviços.

#### 2.3.2 Resultados - Saga Orquestrado
```json
{
  "memory_used_mb": 0,
  "health_status": "UP"
}
```

#### 2.3.3 Resultados - Saga Coreografado
```json
{
  "ping_ms": 19.26898956298828,
  "service_available": true
}
```

## 3. Scripts de Automação

### 3.1 Scripts Desenvolvidos
- `test-orchestrated.py`: Automação para Saga Orquestrado
- `test-choreography.py`: Automação para Saga Coreografado
- `generate-report.py`: Geração de relatórios comparativos
- `simple-test.py`: Testes simplificados para verificação

### 3.2 Funcionalidades Implementadas
- Execução automática de testes de carga
- Simulação de cenários de falha
- Coleta e análise estatística de métricas
- Geração de relatórios em JSON e Markdown
- Logging detalhado de execução

## 4. Análise Comparativa

### 4.1 Performance (Latência)
- **Saga Orquestrado**: 16.25ms (média)
- **Saga Coreografado**: 20.76ms (média)
- **Vantagem**: Orquestrado é 27.7% mais rápido

### 4.2 Throughput
- **Saga Orquestrado**: 8.55 req/s
- **Saga Coreografado**: 8.23 req/s
- **Vantagem**: Orquestrado é 3.8% superior

### 4.3 Confiabilidade
- **Ambos os padrões**: 100% de taxa de sucesso
- **Ambos os padrões**: 0 falhas em 20 requisições

### 4.4 Consistência de Performance
- **Orquestrado**: Menor variação (8-31ms)
- **Coreografado**: Maior variação (9-34ms)

## 5. Validação dos Dados

### 5.1 Rastreabilidade
- Todos os testes executados em sequência temporal
- Timestamps precisos para cada execução
- Dados armazenados em arquivos JSON estruturados

### 5.2 Reprodutibilidade
- Scripts automatizados para repetição dos testes
- Configuração padronizada em Docker Compose
- Payloads estruturados conforme especificação da API

### 5.3 Arquivos de Evidência
- `results_orchestrated_detailed.json`: Dados brutos Orquestrado
- `results_choreography_detailed.json`: Dados brutos Coreografado
- `relatorio_comparativo_final.json`: Análise comparativa

## 6. Metodologia de Execução

### 6.1 Preparação do Ambiente
1. Limpeza de containers anteriores
2. Inicialização dos serviços via Docker Compose
3. Verificação de conectividade dos endpoints
4. Validação da estrutura de payload

### 6.2 Execução dos Testes
1. **Fase 1**: Teste do padrão Orquestrado
2. **Fase 2**: Limpeza e mudança de ambiente
3. **Fase 3**: Teste do padrão Coreografado
4. **Fase 4**: Geração de relatório comparativo

### 6.3 Coleta de Dados
- Medição precisa de timestamps com Python `time.time()`
- Captura de códigos de status HTTP
- Cálculo automático de métricas estatísticas
- Persistência em formato JSON estruturado

## 7. Conclusões Técnicas

### 7.1 Performance
O padrão Saga Orquestrado demonstrou **superioridade em performance**, com latência 27.7% menor que o padrão Coreografado.

### 7.2 Estabilidade
Ambos os padrões apresentaram **100% de disponibilidade** durante os testes, demonstrando robustez nas implementações.

### 7.3 Previsibilidade
O padrão Orquestrado mostrou **menor variação na latência**, indicando comportamento mais previsível.

## 8. Limitações e Considerações

### 8.1 Escopo dos Testes
- Testes executados em ambiente local (não distribuído)
- Volume limitado de requisições (20 por teste)
- Sem simulação de alta concorrência

### 8.2 Fatores Externos
- Performance pode variar com carga de sistema
- Latência de rede não foi fator significativo (localhost)
- Configurações de JVM podem impactar resultados

---

**Data de Geração**: 18 de setembro de 2025
**Executado por**: Sistema automatizado de testes
**Versão**: 1.0
**Formato**: Markdown com dados estruturados em JSON