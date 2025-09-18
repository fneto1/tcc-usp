package br.com.microservices.orchestrated.inventoryservice.core.service;

import br.com.microservices.orchestrated.inventoryservice.core.model.OutboxEvent;
import br.com.microservices.orchestrated.inventoryservice.core.producer.KafkaProducer;
import br.com.microservices.orchestrated.inventoryservice.core.repository.OutboxEventRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Service
@AllArgsConstructor
public class OutboxEventPublisher {

    private static final int MAX_RETRIES = 3;
    private final OutboxEventRepository outboxEventRepository;
    private final KafkaProducer kafkaProducer;

    @Scheduled(fixedDelay = 5000)
    @Transactional
    public void publishPendingEvents() {
        List<OutboxEvent> pendingEvents = outboxEventRepository
                .findByProcessedFalseAndRetryCountLessThan(MAX_RETRIES);

        log.info("Found {} pending outbox events to process", pendingEvents.size());

        for (OutboxEvent event : pendingEvents) {
            try {
                publishEvent(event);
                markAsProcessed(event);
                log.info("Successfully published outbox event: {}", event.getId());
            } catch (Exception ex) {
                handlePublishError(event, ex);
                log.error("Failed to publish outbox event: {} - Error: {}",
                        event.getId(), ex.getMessage());
            }
        }
    }

    private void publishEvent(OutboxEvent event) {
        kafkaProducer.sendEvent(event.getEventData());
    }

    private void markAsProcessed(OutboxEvent event) {
        event.setProcessed(true);
        event.setProcessedAt(LocalDateTime.now());
        outboxEventRepository.save(event);
    }

    private void handlePublishError(OutboxEvent event, Exception ex) {
        event.setRetryCount(event.getRetryCount() + 1);
        event.setErrorMessage(ex.getMessage());

        if (event.getRetryCount() >= MAX_RETRIES) {
            log.error("Max retries reached for outbox event: {}", event.getId());
        }

        outboxEventRepository.save(event);
    }

    @Scheduled(cron = "0 0 2 * * *")
    @Transactional
    public void cleanupProcessedEvents() {
        LocalDateTime cutoffDate = LocalDateTime.now().minusDays(7);
        List<OutboxEvent> oldEvents = outboxEventRepository.findProcessedEventsBefore(cutoffDate);

        if (!oldEvents.isEmpty()) {
            outboxEventRepository.deleteAll(oldEvents);
            log.info("Cleaned up {} processed outbox events older than 7 days", oldEvents.size());
        }
    }
}