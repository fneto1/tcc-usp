package br.com.microservices.orchestrated.orderservice.core.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import br.com.microservices.orchestrated.orderservice.core.service.OrderService;
import br.com.microservices.orchestrated.orderservice.core.dto.OrderRequest;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/test")
public class TestController {

    @Autowired
    private OrderService orderService;

    @PostMapping("/load-test")
    public ResponseEntity<Map<String, Object>> loadTest(@RequestParam(defaultValue = "10") int requests) {
        Map<String, Object> result = new HashMap<>();
        long startTime = System.currentTimeMillis();

        for (int i = 0; i < requests; i++) {
            OrderRequest request = createTestOrder(i);
            try {
                orderService.createOrder(request);
            } catch (Exception e) {
                result.put("error_at_request", i);
                result.put("error_message", e.getMessage());
                break;
            }
        }

        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;

        result.put("total_requests", requests);
        result.put("duration_ms", duration);
        result.put("requests_per_second", requests * 1000.0 / duration);
        result.put("avg_response_time_ms", (double) duration / requests);
        result.put("timestamp", LocalDateTime.now());

        return ResponseEntity.ok(result);
    }

    @PostMapping("/failure-test/{service}")
    public ResponseEntity<Map<String, Object>> failureTest(@PathVariable String service) {
        Map<String, Object> result = new HashMap<>();
        long startTime = System.currentTimeMillis();

        // Configurar produto com quantidade alta para forçar falha no inventory
        OrderRequest request = service.equals("inventory") ?
            createFailureOrder() : createTestOrder(1);

        try {
            var order = orderService.createOrder(request);
            result.put("order_id", order.getId());
            result.put("status", "created");
        } catch (Exception e) {
            result.put("error", e.getMessage());
        }

        long endTime = System.currentTimeMillis();
        result.put("duration_ms", endTime - startTime);
        result.put("service_target", service);
        result.put("timestamp", LocalDateTime.now());

        return ResponseEntity.ok(result);
    }

    @GetMapping("/metrics")
    public ResponseEntity<Map<String, Object>> getMetrics() {
        Map<String, Object> metrics = new HashMap<>();

        Runtime runtime = Runtime.getRuntime();
        metrics.put("memory_used_mb", (runtime.totalMemory() - runtime.freeMemory()) / 1024 / 1024);
        metrics.put("memory_total_mb", runtime.totalMemory() / 1024 / 1024);
        metrics.put("cpu_cores", runtime.availableProcessors());
        metrics.put("timestamp", LocalDateTime.now());

        return ResponseEntity.ok(metrics);
    }

    private OrderRequest createTestOrder(int index) {
        // Criar payload com estrutura correta
        return new OrderRequest(); // Placeholder - estrutura será definida pela classe OrderRequest
    }

    private OrderRequest createFailureOrder() {
        // Criar payload com estrutura correta para falha
        return new OrderRequest(); // Placeholder - estrutura será definida pela classe OrderRequest
    }
}