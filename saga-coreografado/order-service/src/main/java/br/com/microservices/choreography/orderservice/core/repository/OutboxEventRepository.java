package br.com.microservices.choreography.orderservice.core.repository;

import br.com.microservices.choreography.orderservice.core.document.OutboxEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OutboxEventRepository extends MongoRepository<OutboxEvent, String> {

    List<OutboxEvent> findByProcessedFalseOrderByCreatedAtAsc();

    List<OutboxEvent> findByProcessedFalseAndRetryCountLessThanOrderByCreatedAtAsc(Integer maxRetryCount);
}