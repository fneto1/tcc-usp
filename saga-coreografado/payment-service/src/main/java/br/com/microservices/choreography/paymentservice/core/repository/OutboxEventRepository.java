package br.com.microservices.choreography.paymentservice.core.repository;

import br.com.microservices.choreography.paymentservice.core.model.OutboxEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OutboxEventRepository extends JpaRepository<OutboxEvent, Long> {

    List<OutboxEvent> findByProcessedFalseOrderByCreatedAtAsc();

    List<OutboxEvent> findByProcessedFalseAndRetryCountLessThanOrderByCreatedAtAsc(Integer maxRetryCount);
}