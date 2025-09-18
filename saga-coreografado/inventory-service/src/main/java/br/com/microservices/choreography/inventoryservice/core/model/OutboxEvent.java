package br.com.microservices.choreography.inventoryservice.core.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "outbox_event")
public class OutboxEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "aggregate_id", nullable = false)
    private String aggregateId;

    @Column(name = "event_type", nullable = false)
    private String eventType;

    @Column(name = "event_data", columnDefinition = "TEXT", nullable = false)
    private String eventData;

    @Column(name = "destination", nullable = false)
    private String destination;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @Column(name = "processed", nullable = false)
    private Boolean processed = false;

    @Column(name = "processed_at")
    private LocalDateTime processedAt;

    @Column(name = "retry_count")
    private Integer retryCount = 0;

    @Column(name = "error_message")
    private String errorMessage;
}