package br.com.microservices.choreography.orderservice.core.document;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "outbox_event")
public class OutboxEvent {

    @Id
    private String id;
    private String aggregateId;
    private String eventType;
    private String eventData;
    private String destination;
    private LocalDateTime createdAt;
    private Boolean processed;
    private LocalDateTime processedAt;
    private Integer retryCount;
    private String errorMessage;
}