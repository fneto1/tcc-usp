# Scripts de Teste - Validação Experimental Saga

## Arquivos Criados

### 1. Controllers de Teste
- **TestController.java** (ambos projetos): Endpoints para testes automatizados
- **TestMetrics.java** (ambos projetos): Logs estruturados para análise

### 2. Scripts de Automação
- **load-test.py**: Script Python para testes de carga detalhados
- **run-tests.bat**: Script Windows para execução completa dos testes

## Como Usar

### Pré-requisitos
```bash
# Instalar Python requests (se não tiver)
pip install requests

# Subir os serviços
cd saga-orquestrado  # ou saga-coreografado
docker-compose up -d
```

### Execução Rápida
```bash
cd test-scripts
run-tests.bat
```

### Execução Manual
```bash
# Teste de carga - Orquestrado
python load-test.py --pattern orchestrated --requests 50 --threads 5

# Teste de carga - Coreografado
python load-test.py --pattern choreography --requests 50 --threads 5
```

## Endpoints de Teste Disponíveis

### Order Service (porta 3000)
- `POST /api/test/load-test?requests=N` - Teste de carga
- `POST /api/test/failure-test/{service}` - Teste de falha
- `GET /api/test/metrics` - Métricas do sistema

### Payment Service (porta 8091)
- `POST /api/test/simulate-failure?enable=true/false` - Controla simulação de falha
- `GET /api/test/failure-status` - Status da simulação

## Métricas Coletadas

### Performance
- Latência média, mediana, P95
- Throughput (requests/segundo)
- Taxa de sucesso/erro
- Consumo de memória

### Observabilidade
- Logs estruturados com correlation ID
- Timestamps de início/fim de saga
- Rastreamento de rollbacks
- Duração de cada etapa

## Cenários de Teste

1. **Teste de Carga**: N transações simultâneas de sucesso
2. **Teste de Falha**: Simula falha no payment-service
3. **Teste de Inventário**: Produto com estoque insuficiente
4. **Métricas Sistema**: Consumo de recursos

## Resultados

Os resultados são salvos em arquivos JSON:
- `test_results_orchestrated_[timestamp].json`
- `test_results_choreography_[timestamp].json`

## Análise dos Logs

Os logs estruturados permitem análise via grep:
```bash
# Buscar todas as sagas iniciadas
docker logs order-service | grep "SAGA_START"

# Buscar rollbacks
docker logs order-service | grep "ROLLBACK"

# Medir duração média
docker logs order-service | grep "SAGA_END" | grep "SUCCESS"
```