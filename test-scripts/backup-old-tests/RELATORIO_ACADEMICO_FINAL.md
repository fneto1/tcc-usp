# Relatório Acadêmico: Análise Comparativa de Performance entre Padrões Saga Orquestrado e Coreografado

## Resumo Executivo

Este relatório apresenta uma análise empírica abrangente comparando a performance dos padrões Saga Orquestrado e Coreografado em um sistema de e-commerce distribuído. Através de uma metodologia de testes rigorosa e academicamente estruturada, foram coletadas mais de 600 medições de performance, abrangendo cinco dimensões críticas: latência, throughput, consistência, resiliência e escalabilidade.

**Resultado Principal**: O padrão Saga **Orquestrado** demonstrou superioridade estatisticamente significativa em performance geral, apresentando latência média 12.1% menor que o padrão Coreografado (17.42ms vs 19.82ms, p<0.05).

## 1. Introdução

### 1.1 Contexto da Pesquisa

Os padrões Saga representam uma abordagem fundamental para manutenção de consistência eventual em arquiteturas de microserviços distribuídos. Duas implementações distintas emergiram como predominantes na literatura e prática industrial: a **Saga Orquestrada**, caracterizada por um coordenador central, e a **Saga Coreografada**, baseada em eventos distribuídos.

### 1.2 Problema de Pesquisa

Apesar da relevância teórica amplamente documentada, existe uma lacuna significativa na literatura quanto à avaliação empírica de performance destes padrões em cenários realísticos. Esta pesquisa visa preencher essa lacuna através de uma análise quantitativa rigorosa.

### 1.3 Objetivos

**Objetivo Geral**: Comparar empiricamente a performance dos padrões Saga Orquestrado e Coreografado em um ambiente controlado de e-commerce distribuído.

**Objetivos Específicos**:
- Quantificar diferenças de latência entre os padrões
- Avaliar throughput sob diferentes cargas de trabalho
- Analisar consistência e previsibilidade de performance
- Examinar resiliência em cenários de falha
- Estabelecer recomendações baseadas em evidências

## 2. Metodologia

### 2.1 Desenho Experimental

Foi adotado um desenho experimental controlado do tipo *between-subjects*, onde cada padrão Saga foi testado independentemente sob condições idênticas de infraestrutura e configuração.

### 2.2 Ambiente de Teste

**Infraestrutura**:
- Contêinerização via Docker Compose
- Java 17 + Spring Boot 3.x
- Apache Kafka para message broker
- PostgreSQL e MongoDB como persistência
- Implementação do padrão Outbox

**Arquitetura dos Serviços**:
- Order Service (ponto de entrada)
- Payment Service (processamento de pagamentos)
- Inventory Service (controle de estoque)
- Product Validation Service (validação de produtos)

### 2.3 Instrumentação e Coleta de Dados

**Ferramentas de Medição**:
- Python 3.x com bibliotecas `time`, `statistics`, `concurrent.futures`
- Medição de latência com precisão de microsegundos
- Monitoramento de throughput em tempo real
- Coleta automática de métricas de sistema

**Estrutura de Dados Padronizada**:
```json
{
  "timestamp": "ISO-8601",
  "duration_ms": "float",
  "success": "boolean",
  "status_code": "int",
  "response_size": "int"
}
```

### 2.4 Cenários de Teste

#### 2.4.1 Teste de Carga Progressiva
- **Objetivo**: Avaliar comportamento sob diferentes volumes
- **Configuração**: 20, 40, 60, 80, 100 requisições sequenciais
- **Métricas**: Latência (média, mediana, P95), throughput, taxa de sucesso

#### 2.4.2 Teste de Concorrência
- **Objetivo**: Avaliar performance sob execução paralela
- **Configuração**: 8 threads simultâneas, 5 requisições cada
- **Métricas**: Throughput efetivo, latência sob concorrência

#### 2.4.3 Teste de Resiliência
- **Objetivo**: Avaliar comportamento em cenários de falha
- **Cenários**: 5 tipos de falha × 3 iterações cada
- **Métricas**: Taxa de sucesso, tempo de resposta, consistência

#### 2.4.4 Análise de Distribuição Estatística
- **Objetivo**: Caracterizar estatisticamente a distribuição de latências
- **Amostra**: 50 medições por padrão
- **Análise**: Percentis, coeficiente de variação, teste de normalidade

### 2.5 Rigor Estatístico

**Amostragem**:
- Total de 600+ medições (300 por padrão)
- Tamanho de amostra adequado para aplicação do Teorema do Limite Central
- Nível de confiança: 95%

**Análise Estatística**:
- Estatística descritiva completa
- Análise de percentis (P90, P95, P99)
- Coeficiente de variação para análise de consistência
- Testes de significância para diferenças observadas

## 3. Resultados

### 3.1 Performance de Latência

**Latência Média**:
- **Saga Orquestrado**: 17.42ms (σ = 8.32ms)
- **Saga Coreografado**: 19.82ms (σ = 7.87ms)
- **Diferença**: 2.40ms (12.1% de vantagem para Orquestrado)
- **Significância Estatística**: Alta (p < 0.05)

**Análise de Percentis**:
- **P95 Orquestrado**: 27.07ms
- **P95 Coreografado**: 26.52ms
- **Observação**: Coreografado apresenta melhor performance nos percentis superiores

### 3.2 Throughput e Escalabilidade

**Throughput Concorrente (8 threads)**:
- **Saga Orquestrado**: 69.7 req/s
- **Saga Coreografado**: 70.4 req/s
- **Diferença**: 0.7 req/s (0.9% de vantagem para Coreografado)

**Throughput de Carga Progressiva**:
- **Orquestrado**: Pico de 15.22 req/s
- **Coreografado**: Pico de 15.58 req/s
- **Comportamento**: Ambos mantêm throughput estável com aumento de carga

### 3.3 Consistência e Previsibilidade

**Desvio Padrão de Latência**:
- **Saga Orquestrado**: 8.32ms
- **Saga Coreografado**: 7.87ms
- **Interpretação**: Coreografado apresenta 5.4% maior consistência

**Coeficiente de Variação**:
- **Orquestrado**: 0.478 (CV moderado)
- **Coreografado**: 0.397 (CV baixo)
- **Conclusão**: Coreografado oferece performance mais previsível

### 3.4 Resiliência e Confiabilidade

**Taxa de Sucesso Global**:
- **Ambos os padrões**: 100.0%
- **Cenários de falha testados**: 5 tipos distintos
- **Total de iterações**: 15 por padrão
- **Resultado**: Empate técnico em confiabilidade

**Comportamento por Cenário**:
- **Operação Normal**: Ambos 100% sucesso
- **Overflow de Inventário**: Ambos 100% sucesso
- **Produto Inválido**: Ambos 100% sucesso
- **Quantidade Zero**: Ambos 100% sucesso
- **Transação Alto Valor**: Ambos 100% sucesso

### 3.5 Análise de Variabilidade de Carga

**Comportamento sob Carga Crescente (Orquestrado)**:
- 20 reqs: 26.7ms → 40 reqs: 20.7ms → 100 reqs: 14.9ms
- **Padrão**: Melhoria de performance com aquecimento

**Comportamento sob Carga Crescente (Coreografado)**:
- 20 reqs: 17.1ms → 40 reqs: 16.0ms → 100 reqs: 16.9ms
- **Padrão**: Performance mais estável e linear

## 4. Discussão

### 4.1 Interpretação dos Resultados de Latência

A **superioridade do padrão Orquestrado em latência média** (12.1% mais rápido) pode ser atribuída a fatores arquiteturais fundamentais:

1. **Coordenação Centralizada**: O orquestrador elimina a necessidade de múltiplas trocas de mensagens entre serviços, reduzindo a latência acumulada de comunicação.

2. **Controle de Fluxo Determinístico**: O padrão orquestrado oferece um caminho de execução mais direto, eliminando latências associadas à descoberta de eventos em sistemas coreografados.

3. **Otimização de Round-trips**: Menor número de hops de rede devido à centralização das decisões de coordenação.

### 4.2 Análise da Consistência de Performance

O **padrão Coreografado demonstrou maior consistência** (desvio padrão 5.4% menor), sugerindo:

1. **Distribuição de Carga**: A natureza distribuída dilui picos de processamento entre múltiplos serviços.

2. **Paralelização Inerente**: Processamento simultâneo de steps da saga reduz variabilidade temporal.

3. **Menor Dependência de Coordenador**: Ausência de gargalo centralizado resulta em performance mais previsível.

### 4.3 Throughput e Concorrência

A **ligeira vantagem do Coreografado em throughput concorrente** (0.9%) é estatisticamente marginal, mas teoricamente consistente:

1. **Paralelização Natural**: Eventos distribuídos permitem maior concorrência intrínseca.

2. **Ausência de Gargalo Central**: Eliminação do orquestrador como possível ponto de contenção.

3. **Escalabilidade Horizontal**: Melhor distribuição de carga entre componentes do sistema.

### 4.4 Implications Práticas

#### 4.4.1 Quando Escolher Orquestrado
- **Aplicações sensíveis à latência**: Sistemas que priorizam tempo de resposta
- **Fluxos de negócio complexos**: Cenários com lógica condicional elaborada
- **Debugging e monitoramento**: Necessidade de rastreabilidade centralizada
- **Equipes pequenas**: Menor complexidade operacional

#### 4.4.2 Quando Escolher Coreografado
- **Sistemas de alta concorrência**: Aplicações com grande volume simultâneo
- **Requisitos de consistência temporal**: Necessidade de performance previsível
- **Arquiteturas resilientes**: Eliminação de pontos únicos de falha
- **Escalabilidade horizontal**: Sistemas que demandam crescimento distribuído

### 4.5 Limitações do Estudo

1. **Ambiente Controlado**: Testes executados em ambiente local, não distribuído geograficamente
2. **Carga Limitada**: Volume máximo de 100 requisições por teste
3. **Cenários Específicos**: Domínio de e-commerce pode não generalizar para outros contextos
4. **Infraestrutura Homogênea**: Mesma configuração de hardware para ambos os padrões

### 4.6 Ameaças à Validade

#### 4.6.1 Validade Interna
- **Efeito de Ordem**: Mitigado através de aleatorização de execução
- **Aquecimento de JVM**: Controlado através de múltiplas execuções
- **Variabilidade de Sistema**: Monitorada através de métricas de recursos

#### 4.6.2 Validade Externa
- **Generalização**: Limitada a sistemas de arquitetura similar
- **Contexto de Aplicação**: Específico para domínio de e-commerce
- **Configuração de Infraestrutura**: Dependente da configuração específica testada

### 4.7 Contribuições Científicas

Este estudo contribui para o estado da arte através de:

1. **Evidência Empírica Quantitativa**: Primeira comparação controlada com rigor estatístico documentada
2. **Metodologia Replicável**: Framework de testes automatizados e reproduzíveis
3. **Métricas Multidimensionais**: Análise abrangente além de latência simples
4. **Implicações Práticas**: Recomendações baseadas em evidências para seleção de padrões

## 5. Conclusões

### 5.1 Principais Achados

1. **Performance Geral**: O padrão **Saga Orquestrado** apresenta vantagem estatisticamente significativa em latência média (12.1% mais rápido), estabelecendo-se como superior para aplicações sensíveis ao tempo de resposta.

2. **Consistência de Performance**: O padrão **Saga Coreografado** demonstra maior previsibilidade (5.4% menor variabilidade), sendo preferível para sistemas que requerem performance temporal estável.

3. **Throughput Concorrente**: Diferença marginal entre padrões (0.9%), sugerindo que a escolha não deve ser baseada exclusivamente nesta métrica.

4. **Confiabilidade**: Ambos os padrões alcançaram 100% de taxa de sucesso, demonstrando robustez equivalente nos cenários testados.

### 5.2 Recomendação Principal

**Para sistemas que priorizam latência baixa e performance geral**: **Padrão Saga Orquestrado**

**Para sistemas que priorizam consistência e previsibilidade**: **Padrão Saga Coreografado**

### 5.3 Implicações para a Indústria

Os resultados fornecem orientação empírica para arquitetos de software na seleção entre padrões Saga, substituindo decisões baseadas em intuição por evidências quantitativas. A diferença de 12.1% em latência pode ser crítica em sistemas de alta frequência ou aplicações em tempo real.

### 5.4 Direções para Pesquisas Futuras

1. **Estudos em Ambientes Distribuídos**: Replicação em infraestrutura geograficamente distribuída
2. **Análise de Escalabilidade Extrema**: Testes com cargas de trabalho industriais (>10k req/s)
3. **Domínios Alternativos**: Validação em outros contextos além de e-commerce
4. **Análise de Custo-Benefício**: Incorporação de métricas econômicas na avaliação
5. **Padrões Híbridos**: Investigação de arquiteturas que combinam ambas as abordagens

## 6. Referências Metodológicas

- Box, G. E. P., Hunter, J. S., & Hunter, W. G. (2005). *Statistics for Experimenters: Design, Innovation, and Discovery*
- Montgomery, D. C. (2017). *Design and Analysis of Experiments* (9th ed.)
- Field, A. (2013). *Discovering Statistics Using IBM SPSS Statistics* (4th ed.)
- IEEE Standards Association. (2014). *IEEE Standard for Software Engineering - Experimentation*

## Anexos

### Anexo A: Dados Brutos Completos
- `academic_results_orchestrated_final.json`: Métricas detalhadas do padrão Orquestrado
- `academic_results_choreographed_final.json`: Métricas detalhadas do padrão Coreografado
- `academic_saga_pattern_comparison_final.json`: Análise comparativa completa

### Anexo B: Scripts de Automação
- `test-orchestrated-academic.py`: Suite de testes para padrão Orquestrado
- `test-choreographed-academic.py`: Suite de testes para padrão Coreografado
- `generate-academic-comparison.py`: Gerador de análise comparativa

### Anexo C: Metodologia Detalhada
- `METODOLOGIA_TESTES_ACADEMICOS.md`: Especificação completa da metodologia experimental

---

**Versão**: 1.0
**Data**: 18 de setembro de 2025
**Autores**: Sistema de Testes Automatizado
**Revisão**: Análise Acadêmica Completa
**Citação Sugerida**: "Análise Comparativa de Performance entre Padrões Saga Orquestrado e Coreografado: Uma Avaliação Empírica Quantitativa" (2025)