package br.com.microservices.orchestrated.orderservice.core.utils;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Slf4j
@Component
public class TestMetrics {

    public void logSagaStart(String orderId, String transactionId) {
        log.info("SAGA_START | orderId={} | transactionId={} | timestamp={} | service=order-service",
                orderId, transactionId, LocalDateTime.now());
    }

    public void logSagaEnd(String orderId, String transactionId, String status, long durationMs) {
        log.info("SAGA_END | orderId={} | transactionId={} | status={} | duration_ms={} | timestamp={} | service=order-service",
                orderId, transactionId, status, durationMs, LocalDateTime.now());
    }

    public void logServiceCall(String orderId, String transactionId, String targetService, String action) {
        log.info("SERVICE_CALL | orderId={} | transactionId={} | target={} | action={} | timestamp={} | service=order-service",
                orderId, transactionId, targetService, action, LocalDateTime.now());
    }

    public void logServiceResponse(String orderId, String transactionId, String sourceService, String status, long durationMs) {
        log.info("SERVICE_RESPONSE | orderId={} | transactionId={} | source={} | status={} | duration_ms={} | timestamp={} | service=order-service",
                orderId, transactionId, sourceService, status, durationMs, LocalDateTime.now());
    }

    public void logRollback(String orderId, String transactionId, String reason) {
        log.info("ROLLBACK | orderId={} | transactionId={} | reason={} | timestamp={} | service=order-service",
                orderId, transactionId, reason, LocalDateTime.now());
    }
}