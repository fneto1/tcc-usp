package br.com.microservices.orchestrated.inventoryservice.core.service;

import br.com.microservices.orchestrated.inventoryservice.core.model.OutboxEvent;
import br.com.microservices.orchestrated.inventoryservice.core.repository.OutboxEventRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Slf4j
@Service
@AllArgsConstructor
public class OutboxEventService {

    private final OutboxEventRepository outboxEventRepository;

    public void saveOutboxEvent(String aggregateId, String eventType, String eventData, String topic) {
        OutboxEvent outboxEvent = OutboxEvent.builder()
                .aggregateId(aggregateId)
                .eventType(eventType)
                .eventData(eventData)
                .topic(topic)
                .createdAt(LocalDateTime.now())
                .processed(false)
                .retryCount(0)
                .build();

        outboxEventRepository.save(outboxEvent);
        log.info("Saved outbox event: {} for aggregate: {}", eventType, aggregateId);
    }
}