#!/usr/bin/env python3
"""
Complete 48h Academic Experiment Runner
Automated execution of both patterns with statistical analysis
"""

import subprocess
import time
import json
import os
import sys
from datetime import datetime
from academic_test_suite_48h import Academic48hTestSuite
from statistical_analysis import StatisticalAnalyzer


class ExperimentRunner:
    def __init__(self):
        self.experiment_start = datetime.now()
        self.results = {
            'experiment_metadata': {
                'start_time': self.experiment_start.isoformat(),
                'version': '48h_academic',
                'configuration': {
                    'runs_per_scenario': 20,
                    'scenarios': ['baseline', 'medium_stress', 'high_stress'],
                    'load_test_requests': 200,
                    'concurrent_users': 10
                }
            },
            'orchestrated_results': None,
            'choreographed_results': None,
            'statistical_analysis': None,
            'execution_log': []
        }

    def log_event(self, message, event_type="INFO"):
        """Log experiment events"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'type': event_type,
            'message': message
        }
        self.results['execution_log'].append(log_entry)
        print(f"[{timestamp}] {event_type}: {message}")

    def setup_environment(self):
        """Setup experimental environment"""
        self.log_event("[SETUP] Setting up experimental environment")

        # Create external network for Docker services
        try:
            subprocess.run([
                "docker", "network", "create", "saga-test-network"
            ], check=False, capture_output=True)
            self.log_event("✓ Docker network 'saga-test-network' ready")
        except Exception as e:
            self.log_event(f"[WARN] Network creation warning: {e}", "WARNING")

        # Start Toxiproxy for chaos engineering
        try:
            self.log_event("Starting Toxiproxy for chaos engineering...")
            subprocess.run([
                "docker-compose", "-f", "docker-compose-toxiproxy.yml", "up", "-d"
            ], check=True)
            self.log_event("✓ Toxiproxy started successfully")

            # Wait for Toxiproxy to be ready
            time.sleep(10)
            self.log_event("✓ Toxiproxy ready for chaos scenarios")

        except subprocess.CalledProcessError as e:
            self.log_event(f"[ERROR] Failed to start Toxiproxy: {e}", "ERROR")
            return False

        return True

    def deploy_pattern(self, pattern_name):
        """Deploy specific Saga pattern"""
        self.log_event(f"[START] Deploying {pattern_name} pattern")

        # Stop any running containers first
        try:
            subprocess.run([
                "docker", "stop", "$(docker ps -q)"
            ], shell=True, check=False, capture_output=True)
            time.sleep(5)
        except:
            pass

        # Deploy the pattern
        if pattern_name == "orchestrated":
            compose_path = "../saga-orquestrado/docker-compose.yml"
        elif pattern_name == "choreographed":
            compose_path = "../saga-coreografado/docker-compose.yml"
        else:
            self.log_event(f"[ERROR] Unknown pattern: {pattern_name}", "ERROR")
            return False

        try:
            subprocess.run([
                "docker-compose", "-f", compose_path, "up", "-d"
            ], check=True)
            self.log_event(f"✓ {pattern_name} services started")

            # Wait for services to be ready
            self.log_event("[WAIT] Waiting for services to initialize...")
            time.sleep(60)  # Give services time to start

            # Health check
            if self.health_check():
                self.log_event(f"[OK] {pattern_name} pattern ready for testing")
                return True
            else:
                self.log_event(f"[ERROR] {pattern_name} pattern health check failed", "ERROR")
                return False

        except subprocess.CalledProcessError as e:
            self.log_event(f"[ERROR] Failed to deploy {pattern_name}: {e}", "ERROR")
            return False

    def health_check(self, max_attempts=10):
        """Check if services are healthy"""
        import requests

        for attempt in range(max_attempts):
            try:
                response = requests.get("http://localhost:3000/actuator/health", timeout=5)
                if response.status_code == 200:
                    return True
            except:
                pass

            self.log_event(f"Health check attempt {attempt + 1}/{max_attempts}")
            time.sleep(10)

        return False

    def run_pattern_test(self, pattern_name, base_url="http://localhost:3000"):
        """Run complete test suite for a pattern"""
        self.log_event(f"[TEST] Starting {pattern_name} pattern testing")

        try:
            # Create test suite
            test_suite = Academic48hTestSuite(base_url, pattern_name)

            # Run complete test
            pattern_results = test_suite.run_complete_pattern_test()

            # Save intermediate results
            output_filename = f"academic_results_{pattern_name.lower()}_48h.json"
            with open(output_filename, 'w') as f:
                json.dump(pattern_results, f, indent=2)

            self.log_event(f"[OK] {pattern_name} testing completed")
            self.log_event(f"[FILE] Results saved to {output_filename}")

            return pattern_results

        except Exception as e:
            self.log_event(f"[ERROR] {pattern_name} testing failed: {e}", "ERROR")
            return None

    def cleanup_pattern(self, pattern_name):
        """Cleanup pattern deployment"""
        self.log_event(f"[CLEAN] Cleaning up {pattern_name} pattern")

        if pattern_name == "orchestrated":
            compose_path = "../saga-orquestrado/docker-compose.yml"
        elif pattern_name == "choreographed":
            compose_path = "../saga-coreografado/docker-compose.yml"
        else:
            return

        try:
            subprocess.run([
                "docker-compose", "-f", compose_path, "down", "-v"
            ], check=True)
            self.log_event(f"✓ {pattern_name} services stopped")
        except subprocess.CalledProcessError as e:
            self.log_event(f"[WARN] Cleanup warning for {pattern_name}: {e}", "WARNING")

        # Additional cleanup
        time.sleep(10)

    def run_statistical_analysis(self):
        """Run statistical analysis on both patterns"""
        self.log_event("[DATA] Starting statistical analysis")

        try:
            analyzer = StatisticalAnalyzer(significance_level=0.05)

            # Load results
            orchestrated_file = "academic_results_orchestrated_48h.json"
            choreographed_file = "academic_results_choreographed_48h.json"

            if not os.path.exists(orchestrated_file) or not os.path.exists(choreographed_file):
                self.log_event("[ERROR] Results files not found for statistical analysis", "ERROR")
                return None

            if not analyzer.load_pattern_results(orchestrated_file, choreographed_file):
                self.log_event("[ERROR] Failed to load pattern results", "ERROR")
                return None

            # Run complete analysis
            analysis_results = analyzer.run_complete_analysis()

            # Save analysis results
            analysis_filename = analyzer.save_results()
            self.log_event(f"[OK] Statistical analysis completed")
            self.log_event(f"[FILE] Analysis saved to {analysis_filename}")

            return analysis_results

        except Exception as e:
            self.log_event(f"[ERROR] Statistical analysis failed: {e}", "ERROR")
            return None

    def cleanup_environment(self):
        """Cleanup experimental environment"""
        self.log_event("[CLEAN] Cleaning up experimental environment")

        try:
            # Stop Toxiproxy
            subprocess.run([
                "docker-compose", "-f", "docker-compose-toxiproxy.yml", "down"
            ], check=False)

            # Stop all containers
            subprocess.run([
                "docker", "stop", "$(docker ps -q)"
            ], shell=True, check=False, capture_output=True)

            self.log_event("✓ Environment cleanup completed")
        except Exception as e:
            self.log_event(f"[WARN] Cleanup warning: {e}", "WARNING")

    def run_complete_experiment(self):
        """Run the complete 48h experiment"""
        self.log_event("[START] Starting Complete 48h Academic Experiment")
        self.log_event("=" * 80)

        try:
            # Setup
            if not self.setup_environment():
                self.log_event("[ERROR] Environment setup failed", "ERROR")
                return False

            # Test Orchestrated Pattern
            self.log_event("\n" + "=" * 60)
            self.log_event("[TARGET] PHASE 1: ORCHESTRATED PATTERN TESTING")
            self.log_event("=" * 60)

            if self.deploy_pattern("orchestrated"):
                orchestrated_results = self.run_pattern_test("orchestrated")
                self.results['orchestrated_results'] = orchestrated_results
                self.cleanup_pattern("orchestrated")
            else:
                self.log_event("[ERROR] Orchestrated pattern deployment failed", "ERROR")
                return False

            # Pause between patterns
            self.log_event("⏸️ Pausing between patterns (60s)...")
            time.sleep(60)

            # Test Choreographed Pattern
            self.log_event("\n" + "=" * 60)
            self.log_event("[TARGET] PHASE 2: CHOREOGRAPHED PATTERN TESTING")
            self.log_event("=" * 60)

            if self.deploy_pattern("choreographed"):
                choreographed_results = self.run_pattern_test("choreographed")
                self.results['choreographed_results'] = choreographed_results
                self.cleanup_pattern("choreographed")
            else:
                self.log_event("[ERROR] Choreographed pattern deployment failed", "ERROR")
                return False

            # Statistical Analysis
            self.log_event("\n" + "=" * 60)
            self.log_event("[TARGET] PHASE 3: STATISTICAL ANALYSIS")
            self.log_event("=" * 60)

            analysis_results = self.run_statistical_analysis()
            self.results['statistical_analysis'] = analysis_results

            # Complete experiment
            self.results['experiment_metadata']['end_time'] = datetime.now().isoformat()
            self.results['experiment_metadata']['total_duration_hours'] = (
                datetime.now() - self.experiment_start
            ).total_seconds() / 3600

            # Save final experiment results
            final_filename = f"complete_experiment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(final_filename, 'w') as f:
                json.dump(self.results, f, indent=2)

            self.log_event(f"\n[SUCCESS] EXPERIMENT COMPLETED SUCCESSFULLY!")
            self.log_event(f"[FILE] Complete results saved to: {final_filename}")
            self.log_event(f"[TIME] Total duration: {self.results['experiment_metadata']['total_duration_hours']:.2f} hours")

            return True

        except Exception as e:
            self.log_event(f"[ERROR] Experiment failed: {e}", "ERROR")
            return False

        finally:
            self.cleanup_environment()

    def generate_final_report(self):
        """Generate final academic report"""
        self.log_event("[REPORT] Generating final academic report")

        report = {
            'title': 'Academic Comparison of Saga Patterns in Microservices Architecture',
            'methodology': {
                'experimental_design': '48-hour controlled experiment',
                'patterns_tested': ['Orchestrated Saga', 'Choreographed Saga'],
                'metrics_collected': ['Latency', 'Throughput', 'Success Rate', 'P95 Latency'],
                'statistical_significance_level': 0.05,
                'chaos_engineering': ['Baseline', 'Medium Stress', 'High Stress'],
                'sample_size': 20
            },
            'results_summary': {},
            'conclusions': [],
            'academic_validity': {
                'statistical_rigor': 'Shapiro-Wilk normality testing, Mann-Whitney U or t-test comparison',
                'effect_size_analysis': 'Cohen\'s d calculation with interpretation',
                'confidence_intervals': '95% confidence intervals for all comparisons',
                'chaos_engineering': 'Controlled network conditions simulation'
            }
        }

        if self.results.get('statistical_analysis'):
            analysis = self.results['statistical_analysis']
            if 'summary' in analysis:
                summary = analysis['summary']
                report['results_summary'] = {
                    'overall_winner': summary.get('overall_winner', {}),
                    'significant_differences': len(summary.get('significant_differences', [])),
                    'effect_sizes': summary.get('effect_sizes', {})
                }

                # Generate conclusions
                if summary.get('overall_winner', {}).get('pattern') != 'tie':
                    winner = summary['overall_winner']['pattern']
                    report['conclusions'].append(
                        f"Statistical analysis demonstrates {winner} pattern superiority"
                    )
                else:
                    report['conclusions'].append(
                        "No statistically significant difference between patterns detected"
                    )

        # Save report
        report_filename = f"academic_final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)

        self.log_event(f"[REPORT] Final report saved: {report_filename}")
        return report


def main():
    """Main execution function"""
    print("[ACADEMIC] Academic 48h Saga Pattern Experiment")
    print("=" * 60)
    print("This experiment will run comprehensive tests on both Saga patterns")
    print("Expected duration: 12-16 hours of automated execution")
    print("=" * 60)

    # Confirm execution
    response = input("\nProceed with complete experiment? (y/N): ")
    if response.lower() != 'y':
        print("Experiment cancelled.")
        sys.exit(0)

    # Create and run experiment
    runner = ExperimentRunner()

    success = runner.run_complete_experiment()

    if success:
        # Generate final report
        runner.generate_final_report()
        print("\n[TARGET] Academic experiment completed successfully!")
        print("Check the generated files for detailed results and analysis.")
    else:
        print("\n[ERROR] Experiment failed. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()