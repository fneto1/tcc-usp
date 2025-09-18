# Metodologia de Implementação do Padrão Saga Coreografado com Outbox Pattern

## Resumo da Metodologia

Este documento descreve a metodologia utilizada para implementação e análise do padrão Saga Coreografado integrado ao padrão Outbox, aplicado a um sistema de gestão de vendas baseado em arquitetura de microsserviços. A abordagem experimental permitiu avaliar a eficácia, robustez e complexidade de implementação desta solução para transações distribuídas.

## 1. Abordagem Metodológica

### 1.1 Tipo de Pesquisa

A abordagem adotada para este trabalho é a de **pesquisa experimental**, devido à necessidade de analisar o comportamento do padrão Saga Coreografado em um ambiente controlado. Este tipo de pesquisa permite explorar relações de causa e efeito entre as variáveis envolvidas, como os padrões implementados entre os microsserviços e as condições de falha simuladas, buscando entender a influência sobre a consistência dos dados envolvidos na transação e a resiliência do sistema.

### 1.2 Cenários de Validação

Neste projeto, foi implementado o padrão coreografado, trabalhando em cenários que simulam casos práticos, como:

- **Transações de fluxo de venda padrão**: validando produtos em estoque, processamento do pagamento, atualização do estoque
- **Simulações de falha controladas** durante o fluxo de venda
- **Cenários de recuperação automática** através do padrão Outbox

Esta abordagem experimental permite que a recuperação das transações em um cenário de falha e a consistência dos dados entre os serviços sejam observados de forma direta, pois permite a manipulação das variáveis de implementação e condições operacionais, gerando uma análise precisa dos resultados obtidos.

## 2. Tecnologias e Ferramentas

Os sistemas de gerenciamento dos microsserviços foram implementados utilizando tecnologias modernas adequadas ao cenário de sistemas distribuídos. É necessário garantir que o sistema seja altamente escalonável, resiliente e que as operações sejam consistentes. As seguintes são as ferramentas/tecnologias escolhidas para a implementação:

### 2.1 Stack Tecnológica Principal

- **Java 17 e Spring Boot 3**: Framework robusto para desenvolvimento de microsserviços REST com inicialização rápida e modelo de programação produtivo, além de fornecer um conjunto completo de módulos e ferramentas prontos para produção.

- **Apache Kafka**: Plataforma de streaming de eventos distribuída, que proporciona uma comunicação assíncrona e desacoplada entre microsserviços. O Kafka coordena os eventos no sistema, atuando como intermediador de mensageria entre os serviços.

- **PostgreSQL e MongoDB**: Sistema híbrido de bancos de dados. MongoDB para o serviço de entrada (dados semiestruturados) e PostgreSQL para os demais serviços (dados estruturados e consistentes).

### 2.2 Infraestrutura e Containerização

- **Docker e docker-compose**: Containerização de cada microsserviço e seu ambiente, permitindo replicação e implantação facilitada do sistema. O Docker Compose gerencia a execução coordenada de todos os contêineres.

- **Redpanda Console**: Plataforma de gerenciamento e monitoramento das mensagens trocadas entre os microsserviços via Kafka, permitindo visualização dos eventos em tempo real.

### 2.3 Padrões de Arquitetura Implementados

- **Padrão Saga Coreografado**: Implementação descentralizada onde cada microsserviço possui autonomia para gerenciar a comunicação e decidir o próximo passo do fluxo transacional.

- **Padrão Outbox**: Integrado ao Saga para garantir atomicidade entre operações de banco de dados e publicação de eventos, eliminando riscos de perda de dados em cenários de falha.

## 3. Arquitetura do Sistema

### 3.1 Microsserviços Implementados

O sistema foi estruturado com **4 microsserviços principais**:

1. **Order-Service**:
   - Ponto inicial e final do fluxo
   - Responsável pela criação de pedidos
   - Banco de dados: MongoDB
   - Porta: 3000

2. **Product-Validation-Service**:
   - Validação de existência e disponibilidade de produtos
   - Banco de dados: PostgreSQL
   - Porta: 8090

3. **Payment-Service**:
   - Processamento de pagamentos baseado em valores e quantidades
   - Banco de dados: PostgreSQL
   - Porta: 8091

4. **Inventory-Service**:
   - Gestão e atualização de estoque
   - Banco de dados: PostgreSQL
   - Porta: 8092

### 3.2 Fluxo de Comunicação Coreografado

Diferente do padrão orquestrado, no coreografado **não há serviço central de coordenação**. Cada microsserviço possui a responsabilidade de:

- Executar sua transação local
- Determinar o próximo serviço no fluxo
- Publicar eventos para comunicação assíncrona
- Gerenciar cenários de compensação em caso de falhas

## 4. Implementação do Padrão Outbox

### 4.1 Componentes do Padrão Outbox

Para cada microsserviço, foram implementados os seguintes componentes:

**Entidades/Documentos Outbox**:
- `OutboxEvent.java` (PostgreSQL services)
- `OutboxEvent.java` (MongoDB service)

**Repositórios**:
- `OutboxEventRepository.java` com queries específicas para eventos não processados

**Serviços**:
- `OutboxEventService.java` para gerenciamento transacional de eventos
- `OutboxEventPublisher.java` para publicação assíncrona via scheduler

### 4.2 Estrutura da Tabela Outbox

```sql
CREATE TABLE outbox_event (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    event_data TEXT NOT NULL,
    destination VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT
);
```

### 4.3 Garantias Transacionais

O padrão Outbox implementado garante:

- **Atomicidade**: Dados de negócio e eventos salvos na mesma transação
- **Consistência**: Estado sempre sincronizado entre serviços
- **Durabilidade**: Eventos nunca são perdidos
- **At-least-once delivery**: Garantia de entrega com retry automático

## 5. Configuração e Organização do Código

### 5.1 Tópicos Kafka Mapeados

| Serviço | Tópico | Tipo |
|---------|--------|------|
| order-service | product-validation-start | producer |
| order-service | notify-ending | consumer |
| product-validation-service | payment-success | producer |
| product-validation-service | product-validation-fail | consumer/producer |
| payment-service | inventory-success | producer |
| payment-service | payment-fail | consumer/producer |
| inventory-service | notify-ending | producer |
| inventory-service | inventory-fail | consumer/producer |

### 5.2 Estrutura de Pacotes Padronizada

Cada microsserviço segue a organização:

- **Consumer**: Classes responsáveis por consumir eventos Kafka
- **Producer**: Classes para publicação de eventos
- **Service**: Lógica de negócio e integração com Outbox
- **Repository**: Interfaces de acesso a dados
- **Model/Document**: Entidades de domínio
- **DTO**: Objetos de transferência de dados
- **Saga**: Classes de controle de fluxo transacional (SagaExecutionController)

### 5.3 Configurações de Publicação Outbox

**Scheduler Configuration**:
```yaml
outbox:
  max-retry-count: 3
```

**Publisher Settings**:
- Intervalo de execução: 5 segundos
- Retry automático: até 3 tentativas
- Processamento em lote de eventos pendentes

## 6. Implementação da Lógica de Controle

### 6.1 SagaExecutionController

Cada serviço possui uma classe `SagaExecutionController` que implementa:

- **Tratamento de status**: SUCCESS, ROLLBACK_PENDING, FAIL
- **Roteamento de eventos**: Determinação do próximo tópico/serviço
- **Integração com Outbox**: Persistência transacional de eventos

### 6.2 Matriz de Decisão Distribuída

Cada serviço mantém sua própria lógica de decisão baseada em:
- Status do evento recebido
- Contexto local do serviço
- Regras de negócio específicas

### 6.3 Tratamento de Compensação

Em cenários de falha, cada serviço é responsável por:
- Identificar a necessidade de rollback
- Executar ações compensatórias locais
- Propagar eventos de falha para serviços anteriores

## 7. Ambiente de Desenvolvimento e Deploy

### 7.1 Containerização

**docker-compose.yml** configurado com:
- 4 microsserviços Java
- 4 bancos de dados (1 MongoDB + 3 PostgreSQL)
- Apache Kafka + Zookeeper
- Redpanda Console para monitoramento

### 7.2 Build Paralelo

Script Python (`build.py`) para:
- Build simultâneo de todos os serviços
- Gestão de dependências entre containers
- Deploy automatizado do ambiente completo

### 7.3 Rede e Comunicação

**Rede Docker**: `choreography-saga`
- Comunicação interna entre serviços
- Isolamento do ambiente de desenvolvimento
- Configuração de portas específicas por serviço

## 8. Metodologia de Testes

### 8.1 Cenários de Validação

**Teste de Sucesso**:
- Fluxo completo de venda com todos os serviços executando corretamente
- Validação da consistência final dos dados

**Teste de Falha**:
- Simulação de indisponibilidade de estoque
- Verificação do processo de compensação automática
- Análise da integridade dos dados após rollback

### 8.2 Observabilidade

**Monitoramento implementado**:
- Logs estruturados em cada serviço
- Rastreamento de eventos via Redpanda Console
- Histórico completo de transações no banco

### 8.3 Métricas de Avaliação

- **Consistência**: Verificação do estado final dos dados
- **Resiliência**: Comportamento em cenários de falha
- **Performance**: Tempo de processamento end-to-end
- **Observabilidade**: Capacidade de rastreamento e debug

## 9. Vantagens e Considerações da Implementação

### 9.1 Benefícios Observados

- **Autonomia**: Cada serviço gerencia seu próprio fluxo
- **Escalabilidade**: Ausência de gargalo central
- **Robustez**: Padrão Outbox elimina pontos de falha
- **Flexibilidade**: Facilidade para adicionar novos serviços

### 9.2 Complexidades Identificadas

- **Debugging**: Fluxo distribuído mais difícil de rastrear
- **Manutenção**: Lógica de controle espalhada entre serviços
- **Consistency**: Coordenação manual entre serviços
- **Testing**: Cenários de teste mais complexos

## 10. Conclusão Metodológica

A metodologia experimental aplicada permitiu uma análise abrangente do padrão Saga Coreografado integrado ao Outbox Pattern. A implementação demonstrou que esta abordagem é viável para sistemas de gestão de vendas, oferecendo robustez transacional com autonomia distribuída.

Os resultados obtidos validam a eficácia da solução em cenários de sucesso e falha, evidenciando as características de cada padrão e fornecendo base sólida para comparações arquiteturais em sistemas de microsserviços.

Esta metodologia serve como framework replicável para implementações similares, fornecendo diretrizes claras para desenvolvimento, teste e deploy de sistemas distribuídos com garantias transacionais robustas.