package br.com.microservices.choreography.productvalidationservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ProductValidationServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(ProductValidationServiceApplication.class, args);
	}

}
