# Metodologia de Implementação: Sistema de Gestão de Vendas com Padrões Saga e Outbox

## Resumo Metodológico

Este documento detalha a metodologia utilizada para implementação de um sistema distribuído de gestão de vendas baseado na arquitetura de microsserviços, aplicando os padrões Saga Orquestrado e técnicas de consistência eventual através do padrão Outbox. A abordagem experimental permite avaliar o comportamento dos padrões em cenários controlados de sucesso e falha.

## 1. Abordagem Metodológica

### 1.1 Tipo de Pesquisa
A metodologia adotada segue uma **abordagem experimental**, permitindo explorar relações de causa e efeito entre as variáveis envolvidas nos padrões implementados e as condições de falha simuladas. Esta estratégia possibilita analisar diretamente a influência sobre a consistência dos dados e a resiliência do sistema.

### 1.2 Cenários de Validação
Os experimentos foram estruturados para cobrir:
- **Cenários de sucesso**: Fluxo completo de venda com validação de produtos, processamento de pagamento e atualização de estoque
- **Cenários de falha controlada**: Simulações de indisponibilidade de serviços e inconsistências de dados durante o fluxo transacional
- **Análise de recuperação**: Observação dos mecanismos de compensação e rollback automático

## 2. Arquitetura do Sistema

### 2.1 Stack Tecnológica Selecionada

#### Linguagem e Framework
- **Java 17**: Versão LTS com recursos avançados de performance e segurança
- **Spring Boot 3.1.2**: Framework para desenvolvimento de microsserviços REST com inicialização rápida e configuração simplificada

#### Comunicação e Mensageria
- **Apache Kafka**: Plataforma de streaming distribuído para comunicação assíncrona e desacoplada entre microsserviços
- **API REST**: Endpoints para iniciação de processos e consulta de eventos

#### Persistência de Dados
- **Abordagem híbrida de bancos de dados**:
  - **MongoDB**: Banco NoSQL para o serviço de entrada (order-service), adequado para dados semiestruturados de vendas
  - **PostgreSQL**: Banco relacional para demais serviços (product-validation, payment, inventory), garantindo consistência de dados estruturados

#### Infraestrutura e Monitoramento
- **Docker & Docker Compose**: Containerização e orquestração de microsserviços
- **Redpanda Console**: Interface para monitoramento de mensagens Kafka em tempo real

### 2.2 Componentes da Arquitetura

#### Microsserviços Implementados
1. **Order-Service**: Ponto de entrada para criação e gerenciamento de pedidos
2. **Orchestrator-Service**: Coordenador central da saga (exclusivo do padrão orquestrado)
3. **Product-Validation-Service**: Validação de existência e disponibilidade de produtos
4. **Payment-Service**: Processamento de pagamentos e cálculos financeiros
5. **Inventory-Service**: Gestão de estoque e baixa de produtos

#### Infraestrutura de Dados
- **4 bancos PostgreSQL** (product-db, payment-db, inventory-db, outbox tables)
- **1 instância MongoDB** (order-db, outbox collection)
- **Cluster Kafka** para mensageria distribuída

## 3. Implementação do Padrão Saga Orquestrado

### 3.1 Arquitetura Centralizada
```
Order-Service → Orchestrator-Service → Product-Validation-Service
                       ↓
Notify-End ← Orchestrator-Service ← Inventory-Service
                       ↓
              Payment-Service
```

### 3.2 Componentes de Coordenação

#### SagaExecutionController
Classe responsável pela lógica de orquestração, implementando:
- **Matriz de mapeamento**: Associação entre status do evento, origem e próximo tópico
- **Estados de transação**: SUCCESS, ROLLBACK_PENDING, FAIL
- **Determinação de fluxo**: Algoritmo para definir próximos passos baseado no estado atual

#### Mapeamento de Tópicos
| Serviço | Tópico | Tipo |
|---------|--------|------|
| order-service | start-saga | producer |
| orchestrator | orchestrator | consumer |
| product-validation | product-validation-success | consumer |
| payment-service | payment-success | consumer |
| inventory-service | inventory-success | consumer |

### 3.3 Fluxo de Execução
1. **Iniciação**: Order-service publica evento start-saga
2. **Coordenação**: Orchestrator-service direciona sequência de execução
3. **Validação sequencial**: Cada serviço executa sua função e reporta status
4. **Decisão de continuidade**: Orchestrator determina próximo passo ou rollback
5. **Finalização**: Notificação de conclusão (sucesso ou falha)

## 4. Implementação do Padrão Outbox

### 4.1 Motivação Técnica
Complementando o padrão Saga, o padrão Outbox resolve problemas de infraestrutura relacionados à **atomicidade entre persistência de dados e publicação de eventos**, eliminando riscos de inconsistência em falhas de rede ou indisponibilidade do Kafka.

### 4.2 Componentes do Padrão Outbox

#### Entidades OutboxEvent
**MongoDB (Order-Service):**
```javascript
{
  _id: ObjectId,
  aggregateId: String,
  eventType: String,
  eventData: String,
  topic: String,
  createdAt: Date,
  processed: Boolean,
  processedAt: Date,
  retryCount: Number,
  errorMessage: String
}
```

**PostgreSQL (Demais Serviços):**
```sql
CREATE TABLE outbox_event (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data TEXT NOT NULL,
    topic VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT
);
```

#### OutboxEventPublisher
Componente assíncrono responsável por:
- **Polling periódico**: Busca eventos não processados a cada 5 segundos
- **Publicação garantida**: Tentativas de envio para Kafka com retry limitado
- **Marcação de status**: Atualização de eventos como processados após sucesso
- **Limpeza automática**: Remoção de eventos antigos (>7 dias) diariamente

### 4.3 Fluxo Transacional com Outbox
```java
@Transactional
public Order createOrder(OrderRequest request) {
    // 1. Persistir dados do negócio
    var order = repository.save(buildOrder(request));

    // 2. Salvar evento na outbox (mesma transação)
    outboxEventService.saveOutboxEvent(
        order.getId(),
        "ORDER_CREATED",
        jsonUtil.toJson(event),
        "start-saga"
    );

    return order; // Transação atômica garantida
}
```

## 5. Configuração e Deployment

### 5.1 Configuração do Kafka
Cada microsserviço possui configurações específicas:
- **Endereçamento**: Conexão com cluster Kafka
- **Tópicos específicos**: Definição de producers e consumers
- **Group-ID**: Distribuição correta de eventos entre instâncias
- **Auto-offset-reset**: Configurado como `latest` para novos eventos

### 5.2 Estrutura de Pacotes Padronizada
```
src/main/java/br/com/microservices/orchestrated/{service}/
├── config/          # Configurações Kafka e exceções
├── core/
│   ├── consumer/    # Classes de consumo de eventos
│   ├── producer/    # Classes de produção de eventos
│   ├── service/     # Lógica de negócio
│   ├── repository/  # Acesso a dados
│   ├── model/       # Entidades JPA/MongoDB
│   ├── dto/         # Objetos de transferência
│   └── saga/        # Lógica de coordenação (se aplicável)
└── {Service}Application.java
```

### 5.3 Containerização
**Docker Compose** orquestra:
- 5 microsserviços Spring Boot
- 4 bancos PostgreSQL independentes
- 1 instância MongoDB
- Cluster Kafka com Zookeeper
- Redpanda Console para monitoramento

## 6. Validação e Testes

### 6.1 Cenários de Teste

#### Cenário de Sucesso
- **Entrada**: Pedido com produtos válidos e estoque disponível
- **Fluxo**: Order → Product-Validation → Payment → Inventory → Success
- **Validação**: Verificação de consistência em todos os bancos

#### Cenário de Falha
- **Entrada**: Pedido com quantidade superior ao estoque
- **Fluxo**: Order → Product-Validation → Payment → Inventory-Fail → Rollback
- **Validação**: Verificação de compensação completa (payment refund, product rollback)

### 6.2 Métricas de Observabilidade
- **Eventos processados**: Contagem de eventos outbox por status
- **Tempo de processamento**: Latência entre criação e processamento
- **Taxa de retry**: Eventos que necessitaram múltiplas tentativas
- **Consistência eventual**: Verificação de estado final consistente

## 7. Garantias e Benefícios Alcançados

### 7.1 Consistência de Dados
- **Atomicidade**: Transação única para dados de negócio + evento outbox
- **Durabilidade**: Eventos persistidos mesmo com Kafka indisponível
- **Idempotência**: Processamento seguro de eventos duplicados

### 7.2 Tolerância a Falhas
- **Recuperação automática**: Retry com backoff exponencial
- **Observabilidade**: Logs detalhados de falhas e recuperação
- **Degradação graceful**: Sistema continua funcionando com componentes indisponíveis

### 7.3 Performance e Escalabilidade
- **Processamento assíncrono**: Publicação não bloqueia transações
- **Paralelização**: Múltiplas instâncias processando eventos
- **Otimização de queries**: Índices específicos nas tabelas outbox

## 8. Considerações de Implementação

### 8.1 Desafios Identificados
- **Complexidade adicional**: Overhead do padrão outbox
- **Gestão de estado**: Coordenação entre múltiplos bancos
- **Monitoramento**: Necessidade de observabilidade detalhada

### 8.2 Melhores Práticas Aplicadas
- **Separação de responsabilidades**: Cada serviço com banco dedicado
- **Versionamento de eventos**: Estrutura extensível para evolução
- **Configuração externalizada**: Flexibilidade de deployment
- **Testes de resiliência**: Simulação de falhas de infraestrutura

Esta metodologia demonstra uma abordagem sistemática para implementação de microsserviços com garantias de consistência eventual, combinando padrões estabelecidos (Saga) com técnicas modernas de confiabilidade (Outbox) em um contexto de sistema de gestão de vendas distribuído.