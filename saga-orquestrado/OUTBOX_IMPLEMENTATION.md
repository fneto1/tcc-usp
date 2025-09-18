# Implementação do Padrão Outbox

Este documento descreve a implementação do padrão Outbox nos microserviços da saga orquestrada.

## O que foi implementado

### 1. Entidades OutboxEvent
- **order-service**: `OutboxEvent` para MongoDB
- **product-validation-service**: `OutboxEvent` para PostgreSQL
- **payment-service**: `OutboxEvent` para PostgreSQL
- **inventory-service**: `OutboxEvent` para PostgreSQL

### 2. Repositórios
- `OutboxEventRepository` para cada serviço com queries customizadas
- Métodos para buscar eventos não processados, com retry limitado e limpeza

### 3. Serviços
- **OutboxEventService**: Encapsula criação de eventos outbox
- **OutboxEventPublisher**: Processa eventos outbox e publica no Kafka

### 4. Modificações nos Serviços Principais
- **@Transactional**: Garante atomicidade entre persistência e outbox
- **Substituição**: `producer.sendEvent()` → `outboxEventService.saveOutboxEvent()`

### 5. Scheduling
- **@EnableScheduling** habilitado em todas as aplicações
- **Scheduler a cada 5 segundos**: Processa eventos outbox pendentes
- **Limpeza diária**: Remove eventos processados com mais de 7 dias

## Estrutura do Fluxo

### Antes (Publicação Direta)
```java
@Service
public class OrderService {
    public Order createOrder(OrderRequest request) {
        var order = buildOrder(request);
        repository.save(order);
        producer.sendEvent(event); // ❌ Risco de inconsistência
        return order;
    }
}
```

### Depois (Padrão Outbox)
```java
@Service
public class OrderService {
    @Transactional
    public Order createOrder(OrderRequest request) {
        var order = buildOrder(request);
        repository.save(order);

        // ✅ Transação atômica
        outboxEventService.saveOutboxEvent(
            order.getId(),
            "ORDER_CREATED",
            eventJson,
            "start-saga"
        );
        return order;
    }
}
```

### Publisher Assíncrono
```java
@Scheduled(fixedDelay = 5000)
@Transactional
public void publishPendingEvents() {
    // 1. Busca eventos não processados
    // 2. Publica no Kafka
    // 3. Marca como processado
    // 4. Implementa retry com limite
}
```

## Scripts de Migração

Execute os scripts SQL em cada banco PostgreSQL:
- `product-validation-service/src/main/resources/outbox_migration.sql`
- `payment-service/src/main/resources/outbox_migration.sql`
- `inventory-service/src/main/resources/outbox_migration.sql`

Para MongoDB (order-service), a coleção `outbox_event` será criada automaticamente.

## Benefícios Obtidos

### 1. **Consistência Eventual Garantida**
- Transação atômica: dados + evento outbox
- Eliminação da janela de inconsistência

### 2. **Tolerância a Falhas**
- Eventos persistidos mesmo se Kafka estiver indisponível
- Retry automático com limite configurável
- Logs detalhados para debugging

### 3. **Observabilidade**
- Histórico completo de eventos na outbox
- Tracking de retry_count e error_message
- Limpeza automática de eventos antigos

### 4. **Performance**
- Publicação assíncrona não bloqueia transações
- Índices otimizados para queries da outbox
- Batch processing a cada 5 segundos

## Monitoramento

### Métricas Importantes
- Eventos pendentes na outbox
- Taxa de sucesso de publicação
- Eventos com retry_count > 0
- Tempo médio de processamento

### Logs para Observar
```
INFO: Saved outbox event: ORDER_CREATED for aggregate: 12345
INFO: Found 3 pending outbox events to process
INFO: Successfully published outbox event: 67890
ERROR: Failed to publish outbox event: 11111 - Error: Connection timeout
```

## Troubleshooting

### Eventos Acumulando na Outbox
1. Verificar conectividade com Kafka
2. Verificar se scheduler está habilitado
3. Analisar logs de erro no OutboxEventPublisher

### Performance Degradada
1. Verificar índices nas tabelas outbox_event
2. Ajustar frequência do scheduler (fixedDelay)
3. Implementar limpeza mais agressiva de eventos antigos

Esta implementação garante a confiabilidade da saga orquestrada através do padrão Outbox, eliminando riscos de inconsistência entre persistência de dados e publicação de eventos.