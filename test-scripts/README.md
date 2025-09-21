# Academic 48h Saga Pattern Experiment

## Overview

This is a comprehensive, scientifically rigorous test suite designed to compare **Orchestrated** vs **Choreographed** Saga patterns in microservices architecture. The experiment is optimized for 48-hour execution while maintaining academic validity.

## 🎯 Experiment Goals

- **Scientific Comparison**: Statistically rigorous comparison between Saga patterns
- **Chaos Engineering**: Controlled failure injection to simulate real-world conditions
- **Academic Rigor**: Proper statistical analysis with confidence intervals and effect sizes
- **Time Optimized**: Complete execution within 48 hours

## 📋 Test Methodology

### Test Configuration
- **Patterns Tested**: Orchestrated Saga, Choreographed Saga
- **Runs per Scenario**: 20 (statistically valid sample size)
- **Chaos Scenarios**: Baseline, Medium Stress, High Stress
- **Load Test Requests**: 200 per run (optimized for speed)
- **Concurrent Users**: 10 (realistic load)
- **Statistical Significance**: α = 0.05

### Metrics Collected
- **Latency**: Mean, Median, P95, P99
- **Throughput**: Requests per second
- **Success Rate**: Percentage of successful requests
- **Concurrency Performance**: Multi-threaded execution
- **Resilience**: Failure scenario handling

### Chaos Engineering Scenarios
1. **Baseline**: Normal network conditions (0ms latency, 0% loss)
2. **Medium Stress**: 150ms latency, 3% packet loss
3. **High Stress**: 300ms latency, 10% packet loss

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- 16GB+ RAM recommended
- 48 hours of continuous execution time

### Setup
```bash
# Make setup script executable and run
chmod +x setup_experiment.sh
./setup_experiment.sh
```

### Complete Automated Experiment
```bash
# Run full 48h experiment (12-16 hours actual execution)
python3 run_complete_experiment.py
```

### Manual Pattern Testing
```bash
# Test individual patterns
python3 academic_test_suite_48h.py orchestrated http://localhost:3000
python3 academic_test_suite_48h.py choreographed http://localhost:3000
```

### Statistical Analysis Only
```bash
# Run analysis on existing results
python3 statistical_analysis.py academic_results_orchestrated_48h.json academic_results_choreographed_48h.json
```

## 📊 Statistical Analysis

### Tests Performed
- **Normality Testing**: Shapiro-Wilk test
- **Comparison Tests**: T-test (normal data) or Mann-Whitney U (non-normal)
- **Effect Size**: Cohen's d with interpretation
- **Confidence Intervals**: 95% CI for difference in means
- **Variance Testing**: Levene's test for equal variances

### Interpretation Guidelines
- **p < 0.05**: Statistically significant difference
- **Cohen's d**:
  - < 0.2: Negligible effect
  - 0.2-0.5: Small effect
  - 0.5-0.8: Medium effect
  - > 0.8: Large effect

## 📁 File Structure

```
test-scripts/
├── academic_test_suite_48h.py      # Main test suite
├── chaos_controller.py             # Chaos engineering controller
├── statistical_analysis.py         # Statistical analysis module
├── run_complete_experiment.py      # Automated experiment runner
├── docker-compose-toxiproxy.yml    # Chaos infrastructure
├── setup_experiment.sh             # Environment setup
├── requirements.txt                # Python dependencies
└── README.md                       # This file

Results Generated:
├── academic_results_orchestrated_48h.json
├── academic_results_choreographed_48h.json
├── statistical_analysis_results_*.json
├── complete_experiment_results_*.json
├── academic_final_report_*.json
└── statistical_analysis_visualization_*.png
```

## ⏱️ Execution Timeline

### Complete Experiment (12-16 hours)
```
Phase 1: Orchestrated Testing    (5-7 hours)
├── Setup & Deploy              (30 min)
├── 3 scenarios × 20 runs       (4-6 hours)
└── Cleanup                     (30 min)

Phase 2: Choreographed Testing   (5-7 hours)
├── Setup & Deploy              (30 min)
├── 3 scenarios × 20 runs       (4-6 hours)
└── Cleanup                     (30 min)

Phase 3: Statistical Analysis    (1-2 hours)
├── Data processing             (30 min)
├── Statistical tests           (30 min)
├── Visualization generation    (30 min)
└── Report generation           (30 min)
```

### Individual Pattern Testing (5-7 hours)
- 60 total test runs (3 scenarios × 20 runs)
- ~5-6 minutes per test run
- Including setup, execution, and cleanup

## 🔧 Customization

### Modify Test Configuration
Edit `academic_test_suite_48h.py`:
```python
self.config = {
    'runs_per_scenario': 20,      # Increase for more statistical power
    'load_test_requests': 200,    # Increase for longer tests
    'concurrent_users': 10,       # Increase for higher load
    'scenarios': ['baseline', 'medium_stress', 'high_stress']
}
```

### Add Chaos Scenarios
Edit `chaos_controller.py`:
```python
self.scenarios = {
    "extreme_stress": {
        "name": "Extreme Stress",
        "latency_ms": 500,
        "packet_loss": 0.2,
        "description": "Extreme network conditions"
    }
}
```

### Change Statistical Significance
Edit `statistical_analysis.py`:
```python
analyzer = StatisticalAnalyzer(significance_level=0.01)  # 99% confidence
```

## 📈 Expected Results

### Academic Validity
- **Sample Size**: n=60 per pattern (20 runs × 3 scenarios)
- **Statistical Power**: >0.8 for medium effect sizes
- **Confidence Level**: 95%
- **Multiple Comparisons**: Bonferroni correction applied

### Performance Metrics
- **Latency Range**: 10-500ms depending on chaos scenario
- **Throughput Range**: 5-70 req/s depending on load and chaos
- **Success Rate**: 85-100% depending on resilience
- **Effect Sizes**: Expected small to medium differences (d=0.2-0.8)

## 🔍 Troubleshooting

### Common Issues

**Docker Memory Issues**
```bash
# Increase Docker memory limit to 8GB+
# Docker Desktop: Settings → Resources → Memory
```

**Port Conflicts**
```bash
# Check for port conflicts
netstat -tulpn | grep :3000
docker ps  # Check running containers
```

**Toxiproxy Connection Issues**
```bash
# Restart toxiproxy
docker-compose -f docker-compose-toxiproxy.yml restart
curl http://localhost:8474/version
```

**Saga Service Health Issues**
```bash
# Check service logs
docker logs order-service
docker logs kafka
```

### Debug Mode
Add debug flags to test execution:
```bash
python3 academic_test_suite_48h.py orchestrated http://localhost:3000 --debug
```

## 📚 Academic References

This experiment follows established practices in:
- **Software Performance Engineering**: Rigorous load testing methodology
- **Chaos Engineering**: Controlled failure injection (Netflix Chaos Monkey principles)
- **Statistical Analysis**: Appropriate statistical tests for performance data
- **Experimental Design**: Controlled variables, randomization, replication

## 🤝 Contributing

### Adding New Tests
1. Extend `Academic48hTestSuite` class
2. Add new chaos scenarios in `ChaosController`
3. Update statistical analysis for new metrics
4. Update documentation

### Improving Performance
1. Optimize Docker resource allocation
2. Tune test parameters for faster execution
3. Implement parallel test execution
4. Add caching mechanisms

## 📄 License

This experiment suite is designed for academic research purposes.

---

**⚠️ Important**: This is a research-grade experiment. Ensure adequate computational resources and time allocation before starting the complete experiment.