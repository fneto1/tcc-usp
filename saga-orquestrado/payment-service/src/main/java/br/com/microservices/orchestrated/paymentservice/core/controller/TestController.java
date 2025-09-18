package br.com.microservices.orchestrated.paymentservice.core.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/test")
public class TestController {

    private static boolean simulateFailure = false;

    @PostMapping("/simulate-failure")
    public ResponseEntity<Map<String, String>> toggleFailure(@RequestParam boolean enable) {
        simulateFailure = enable;
        Map<String, String> response = new HashMap<>();
        response.put("message", "Failure simulation " + (enable ? "enabled" : "disabled"));
        response.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/failure-status")
    public ResponseEntity<Map<String, Object>> getFailureStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("failure_simulation_enabled", simulateFailure);
        status.put("timestamp", LocalDateTime.now());
        return ResponseEntity.ok(status);
    }

    public static boolean isFailureSimulationEnabled() {
        return simulateFailure;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("service", "payment-service");
        health.put("timestamp", LocalDateTime.now());
        return ResponseEntity.ok(health);
    }
}