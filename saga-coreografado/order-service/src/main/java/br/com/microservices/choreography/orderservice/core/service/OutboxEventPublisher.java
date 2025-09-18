package br.com.microservices.choreography.orderservice.core.service;

import br.com.microservices.choreography.orderservice.core.document.OutboxEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class OutboxEventPublisher {

    private final OutboxEventService outboxEventService;
    private final KafkaTemplate<String, String> kafkaTemplate;

    @Value("${outbox.max-retry-count:3}")
    private int maxRetryCount;

    @Scheduled(fixedDelay = 5000)
    public void publishPendingEvents() {
        try {
            List<OutboxEvent> unprocessedEvents = outboxEventService.findUnprocessedEventsWithRetryLimit(maxRetryCount);

            for (OutboxEvent event : unprocessedEvents) {
                try {
                    publishEvent(event);
                    outboxEventService.markAsProcessed(event);
                    log.info("Successfully published outbox event: {}", event.getId());
                } catch (Exception ex) {
                    log.error("Failed to publish outbox event: {}", event.getId(), ex);
                    outboxEventService.incrementRetryCount(event, ex.getMessage());
                }
            }

            if (!unprocessedEvents.isEmpty()) {
                log.info("Processed {} outbox events", unprocessedEvents.size());
            }
        } catch (Exception ex) {
            log.error("Error during outbox event publishing", ex);
        }
    }

    private void publishEvent(OutboxEvent event) {
        log.info("Publishing event to topic {} with data {}", event.getDestination(), event.getEventData());
        kafkaTemplate.send(event.getDestination(), event.getEventData());
    }
}