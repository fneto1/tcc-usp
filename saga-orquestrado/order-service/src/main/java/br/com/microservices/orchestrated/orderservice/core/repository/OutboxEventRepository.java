package br.com.microservices.orchestrated.orderservice.core.repository;

import br.com.microservices.orchestrated.orderservice.core.document.OutboxEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.time.LocalDateTime;
import java.util.List;

public interface OutboxEventRepository extends MongoRepository<OutboxEvent, String> {

    @Query("{ 'processed': false }")
    List<OutboxEvent> findByProcessedFalseOrderByCreatedAt();

    @Query("{ 'processed': false, 'retryCount': { $lt: ?0 } }")
    List<OutboxEvent> findByProcessedFalseAndRetryCountLessThan(int maxRetries);

    @Query("{ 'processed': true, 'processedAt': { $lt: ?0 } }")
    List<OutboxEvent> findProcessedEventsBefore(LocalDateTime cutoffDate);
}