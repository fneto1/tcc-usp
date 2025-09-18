package br.com.microservices.orchestrated.inventoryservice.core.repository;

import br.com.microservices.orchestrated.inventoryservice.core.model.OutboxEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;

public interface OutboxEventRepository extends JpaRepository<OutboxEvent, Long> {

    @Query("SELECT o FROM OutboxEvent o WHERE o.processed = false ORDER BY o.createdAt")
    List<OutboxEvent> findByProcessedFalseOrderByCreatedAt();

    @Query("SELECT o FROM OutboxEvent o WHERE o.processed = false AND o.retryCount < :maxRetries ORDER BY o.createdAt")
    List<OutboxEvent> findByProcessedFalseAndRetryCountLessThan(@Param("maxRetries") int maxRetries);

    @Query("SELECT o FROM OutboxEvent o WHERE o.processed = true AND o.processedAt < :cutoffDate")
    List<OutboxEvent> findProcessedEventsBefore(@Param("cutoffDate") LocalDateTime cutoffDate);
}