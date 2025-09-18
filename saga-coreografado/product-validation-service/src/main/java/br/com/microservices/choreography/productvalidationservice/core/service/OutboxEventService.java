package br.com.microservices.choreography.productvalidationservice.core.service;

import br.com.microservices.choreography.productvalidationservice.core.model.OutboxEvent;
import br.com.microservices.choreography.productvalidationservice.core.repository.OutboxEventRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Service
@AllArgsConstructor
public class OutboxEventService {

    private final OutboxEventRepository outboxEventRepository;

    @Transactional
    public void saveOutboxEvent(String aggregateId, String eventType, String eventData, String destination) {
        var outboxEvent = OutboxEvent.builder()
                .aggregateId(aggregateId)
                .eventType(eventType)
                .eventData(eventData)
                .destination(destination)
                .createdAt(LocalDateTime.now())
                .processed(false)
                .retryCount(0)
                .build();

        outboxEventRepository.save(outboxEvent);
        log.info("Outbox event saved for aggregate {} with type {}", aggregateId, eventType);
    }

    public List<OutboxEvent> findUnprocessedEvents() {
        return outboxEventRepository.findByProcessedFalseOrderByCreatedAtAsc();
    }

    public List<OutboxEvent> findUnprocessedEventsWithRetryLimit(int maxRetryCount) {
        return outboxEventRepository.findByProcessedFalseAndRetryCountLessThanOrderByCreatedAtAsc(maxRetryCount);
    }

    @Transactional
    public void markAsProcessed(OutboxEvent event) {
        event.setProcessed(true);
        event.setProcessedAt(LocalDateTime.now());
        outboxEventRepository.save(event);
        log.info("Outbox event {} marked as processed", event.getId());
    }

    @Transactional
    public void incrementRetryCount(OutboxEvent event, String errorMessage) {
        event.setRetryCount(event.getRetryCount() + 1);
        event.setErrorMessage(errorMessage);
        outboxEventRepository.save(event);
        log.warn("Outbox event {} retry count incremented to {}", event.getId(), event.getRetryCount());
    }
}