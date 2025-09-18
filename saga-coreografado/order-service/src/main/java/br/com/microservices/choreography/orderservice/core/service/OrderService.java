package br.com.microservices.choreography.orderservice.core.service;

import br.com.microservices.choreography.orderservice.core.document.Event;
import br.com.microservices.choreography.orderservice.core.document.Order;
import br.com.microservices.choreography.orderservice.core.dto.OrderRequest;
import br.com.microservices.choreography.orderservice.core.producer.SagaProducer;
import br.com.microservices.choreography.orderservice.core.repository.OrderRepository;
import br.com.microservices.choreography.orderservice.core.utils.JsonUtil;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.LocalDateTime;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class OrderService {

    private static final String TRANSACTION_ID_PATTERN = "%s_%s";

    private final EventService eventService;
    private final SagaProducer producer;
    private final JsonUtil jsonUtil;
    private final OrderRepository repository;
    private final OutboxEventService outboxEventService;

    @Value("${spring.kafka.topic.product-validation-start}")
    private String productValidationStartTopic;

    @Transactional
    public Order createOrder(OrderRequest orderRequest) {
        var order = Order
                .builder()
                .products(orderRequest.getProducts())
                .createdAt(LocalDateTime.now())
                .transactionId(
                        String.format(TRANSACTION_ID_PATTERN, Instant.now().toEpochMilli(), UUID.randomUUID()))
                .build();
        repository.save(order);

        var event = eventService.createEvent(order);
        outboxEventService.saveOutboxEvent(
                order.getId(),
                "ORDER_CREATED",
                jsonUtil.toJson(event),
                productValidationStartTopic
        );

        log.info("Order created with ID: {} and saved to outbox", order.getId());
        return order;
    }


}
