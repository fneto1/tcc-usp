# Metodologia de Testes Acadêmicos para Comparação de Padrões Saga

## 1. Visão Geral

Esta metodologia estabelece um framework robusto e academicamente rigoroso para comparação empírica entre padrões Saga Orquestrado e Coreografado, seguindo princípios de experimentação científica e análise estatística.

## 2. Objetivos da Pesquisa

### 2.1 Objetivo Principal
Quantificar e comparar estatisticamente a performance, resiliência e eficiência de recursos dos padrões Saga Orquestrado e Coreografado em um ambiente controlado.

### 2.2 Objetivos Específicos
- Medir latência com distribuição estatística completa
- Avaliar throughput sob diferentes cargas de trabalho
- Testar resiliência em cenários de falha controlados
- Monitorar impacto no uso de recursos do sistema
- Analisar comportamento sob concorrência

## 3. Hipóteses de Pesquisa

### H1: Performance
**H₁₀**: Não há diferença significativa na latência média entre padrões Saga Orquestrado e Coreografado
**H₁₁**: Existe diferença significativa na latência média entre os padrões

### H2: Throughput
**H₂₀**: Não há diferença significativa no throughput máximo entre os padrões
**H₂₁**: Existe diferença significativa no throughput máximo entre os padrões

### H3: Resiliência
**H₃₀**: Não há diferença significativa na taxa de sucesso em cenários de falha
**H₃₁**: Existe diferença significativa na taxa de sucesso em cenários de falha

## 4. Metodologia Experimental

### 4.1 Desenho Experimental
- **Tipo**: Estudo experimental controlado
- **Abordagem**: Comparação entre grupos (between-subjects)
- **Controle**: Ambiente padronizado com Docker Compose
- **Aleatorização**: Ordem de execução dos padrões randomizada

### 4.2 Variáveis de Pesquisa

#### Variáveis Independentes
- Padrão Saga (Orquestrado vs. Coreografado)
- Carga de trabalho (10, 20, 30, 40, 50 requests)
- Nível de concorrência (1-5 threads)
- Cenário de falha (5 tipos diferentes)

#### Variáveis Dependentes
- **Latência**: Tempo de resposta (ms)
- **Throughput**: Requisições por segundo (req/s)
- **Taxa de Sucesso**: Percentual de requisições bem-sucedidas
- **Uso de CPU**: Percentual de utilização
- **Uso de Memória**: Percentual de utilização

### 4.3 População e Amostra
- **Domínio**: Sistemas de e-commerce com transações distribuídas
- **Tamanho da Amostra**: Mínimo 30 observações por métrica (teorema do limite central)
- **Critério de Inclusão**: Requisições com tempo de resposta < 60 segundos
- **Critério de Exclusão**: Falhas de conectividade de rede

## 5. Cenários de Teste

### 5.1 Teste de Carga Progressiva
**Objetivo**: Avaliar comportamento sob diferentes cargas
**Metodologia**:
- Cargas: 10, 20, 30, 40, 50 requisições
- Intervalo entre requisições: 50ms
- Métricas: Latência média, mediana, P95, throughput
- Repetições: 3 execuções por carga

### 5.2 Teste de Concorrência
**Objetivo**: Avaliar comportamento sob execução paralela
**Metodologia**:
- Threads: 5 threads concorrentes
- Requisições por thread: 4
- Total de requisições: 20 simultâneas
- Métricas: Throughput efetivo, latência sob concorrência

### 5.3 Teste de Resiliência
**Objetivo**: Avaliar comportamento em cenários de falha
**Cenários**:
1. **Operação Normal**: Produto válido, quantidade normal
2. **Falha de Inventário**: Quantidade excessiva (999 unidades)
3. **Produto Inválido**: Código de produto não existente
4. **Quantidade Zero**: Teste de validação de entrada
5. **Transação de Alto Valor**: Teste de limites de pagamento

**Metodologia**:
- 3 iterações por cenário
- Timeout: 45 segundos
- Métricas: Taxa de sucesso, tempo de resposta, consistência

### 5.4 Análise de Distribuição de Latência
**Objetivo**: Caracterizar estatisticamente a distribuição de latências
**Metodologia**:
- Amostra: 30 requisições
- Testes estatísticos: Shapiro-Wilk para normalidade
- Métricas: Média, mediana, desvio padrão, quartis, percentis

### 5.5 Monitoramento de Recursos
**Objetivo**: Avaliar impacto no sistema hospedeiro
**Metodologia**:
- Duração: 30 segundos de monitoramento contínuo
- Frequência: Amostragem a cada 2 segundos
- Métricas: CPU, memória, latência de requisições

## 6. Instrumentação e Medição

### 6.1 Ferramentas de Medição
- **Linguagem**: Python 3.x com bibliotecas científicas
- **Timing**: `time.time()` com precisão de microsegundos
- **Recursos**: `psutil` para métricas de sistema
- **HTTP**: `requests` com timeout configurável

### 6.2 Coleta de Dados
```python
# Estrutura de dados padronizada
measurement = {
    'timestamp': datetime.now().isoformat(),
    'duration_ms': float,
    'success': boolean,
    'status_code': int,
    'response_size': int,
    'cpu_usage': float,
    'memory_usage': float
}
```

### 6.3 Controle de Qualidade
- Validação de payload antes de cada teste
- Verificação de conectividade de serviços
- Logging detalhado de execução
- Persistência automática de resultados

## 7. Análise Estatística

### 7.1 Estatística Descritiva
- Medidas de tendência central (média, mediana)
- Medidas de dispersão (desvio padrão, IQR)
- Percentis (P90, P95, P99)
- Coeficiente de variação

### 7.2 Testes de Hipótese
- **Teste de Normalidade**: Shapiro-Wilk (n < 50)
- **Teste t de Student**: Para amostras normais
- **Teste Mann-Whitney U**: Para amostras não-normais
- **Nível de Significância**: α = 0.05

### 7.3 Análise de Variância
- ANOVA para comparação de múltiplas cargas
- Teste post-hoc de Tukey para diferenças específicas
- Análise de homogeneidade de variâncias

## 8. Critérios de Validade

### 8.1 Validade Interna
- **Controle de Variáveis**: Ambiente padronizado
- **Aleatorização**: Ordem de execução randomizada
- **Replicabilidade**: Scripts automatizados
- **Instrumentação**: Ferramentas validadas

### 8.2 Validade Externa
- **Representatividade**: Cenários baseados em casos reais
- **Generalização**: Aplicável a sistemas similares
- **Limitações**: Ambiente local (não distribuído)

### 8.3 Validade de Construto
- **Métricas Válidas**: Latência, throughput reconhecidos
- **Operacionalização**: Definições claras de medição
- **Triangulação**: Múltiplas métricas convergentes

## 9. Aspectos Éticos e Limitações

### 9.1 Limitações do Estudo
- Ambiente de teste local (não produção)
- Carga limitada (máximo 50 requisições)
- Ausência de tráfego de rede real
- Configuração específica de hardware

### 9.2 Ameaças à Validade
- **Efeito de ordem**: Mitigado por aleatorização
- **Aquecimento de JVM**: Mitigado por execuções de warm-up
- **Variabilidade do sistema**: Controlada por monitoramento

## 10. Cronograma de Execução

### Fase 1: Preparação (5 min)
- Instalação de dependências
- Verificação de conectividade
- Configuração de ambiente

### Fase 2: Testes Orquestrado (15 min)
- Teste de carga progressiva
- Teste de concorrência
- Teste de resiliência
- Análise de distribuição
- Monitoramento de recursos

### Fase 3: Transição (2 min)
- Shutdown de containers
- Mudança de configuração
- Reinicialização de ambiente

### Fase 4: Testes Coreografado (15 min)
- Repetição de todos os testes
- Coleta padronizada de dados

### Fase 5: Análise (3 min)
- Compilação de resultados
- Análise estatística comparativa
- Geração de relatórios

## 11. Entregáveis

### 11.1 Dados Brutos
- `academic_results_orchestrated.json`
- `academic_results_choreographed.json`

### 11.2 Análise Comparativa
- `academic_saga_comparison_final.json`

### 11.3 Relatórios
- Relatório técnico com análise estatística
- Gráficos de distribuição de latência
- Tabelas de comparação de métricas

## 12. Bibliografia Metodológica

- Box, G. E. P., Hunter, J. S., & Hunter, W. G. (2005). *Statistics for Experimenters*
- Montgomery, D. C. (2017). *Design and Analysis of Experiments*
- Field, A. (2013). *Discovering Statistics Using IBM SPSS Statistics*
- IEEE Standards for Software Engineering Experimentation

---

**Versão**: 2.0
**Data**: Setembro 2025
**Autor**: Sistema de Testes Automatizado
**Revisão**: Metodologia Acadêmica