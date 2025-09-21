#!/usr/bin/env python3
"""
Statistical Analysis Module - Academic Rigor for 48h Results
Comprehensive statistical comparison between Saga patterns
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import mannwhitneyu, shapiro, levene
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import statistics
import os


class StatisticalAnalyzer:
    def __init__(self, significance_level=0.05):
        self.alpha = significance_level
        self.results = {}

    def load_pattern_results(self, orchestrated_file, choreographed_file):
        """Load results from both patterns"""
        print("[LOAD] Loading pattern results...")

        try:
            with open(orchestrated_file, 'r') as f:
                self.orchestrated_data = json.load(f)
            print(f"[OK] Loaded orchestrated results from {orchestrated_file}")

            with open(choreographed_file, 'r') as f:
                self.choreographed_data = json.load(f)
            print(f"[OK] Loaded choreographed results from {choreographed_file}")

            return True
        except FileNotFoundError as e:
            print(f"[ERROR] Error loading files: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"[ERROR] Error parsing JSON: {e}")
            return False

    def extract_metrics(self, pattern_data):
        """Extract key metrics from pattern results"""
        metrics = {
            'latencies': [],
            'throughputs': [],
            'success_rates': [],
            'p95_latencies': [],
            'concurrent_throughputs': []
        }

        # Extract from all scenarios
        for scenario_key, scenario_data in pattern_data.get('scenarios', {}).items():
            if 'tests' in scenario_data:
                # Load test metrics
                if 'load_test' in scenario_data['tests']:
                    load_test = scenario_data['tests']['load_test']
                    if 'latency_stats' in load_test:
                        metrics['latencies'].append(load_test['latency_stats'].get('mean_ms', 0))
                        metrics['p95_latencies'].append(load_test['latency_stats'].get('p95_ms', 0))

                    metrics['throughputs'].append(load_test.get('throughput_req_s', 0))
                    metrics['success_rates'].append(load_test.get('success_rate', 0))

                # Concurrent test metrics
                if 'concurrent_test' in scenario_data['tests']:
                    concurrent_test = scenario_data['tests']['concurrent_test']
                    metrics['concurrent_throughputs'].append(
                        concurrent_test.get('effective_throughput_req_s', 0)
                    )

        # Remove zeros and invalid values
        for key in metrics:
            metrics[key] = [x for x in metrics[key] if x > 0]

        return metrics

    def test_normality(self, data, data_name):
        """Test for normality using Shapiro-Wilk test"""
        if len(data) < 3:
            return {
                'test': 'insufficient_data',
                'statistic': None,
                'p_value': None,
                'is_normal': False,
                'sample_size': len(data)
            }

        try:
            statistic, p_value = shapiro(data)
            is_normal = p_value > self.alpha

            print(f"  Normality test for {data_name}:")
            print(f"    Shapiro-Wilk statistic: {statistic:.4f}")
            print(f"    p-value: {p_value:.4f}")
            print(f"    Is normal (={self.alpha}): {is_normal}")

            return {
                'test': 'shapiro_wilk',
                'statistic': statistic,
                'p_value': p_value,
                'is_normal': is_normal,
                'sample_size': len(data)
            }
        except Exception as e:
            print(f"    Error in normality test: {e}")
            return {
                'test': 'error',
                'error': str(e),
                'is_normal': False,
                'sample_size': len(data)
            }

    def compare_metrics(self, orch_metrics, choreo_metrics, metric_name):
        """Statistical comparison between patterns for a specific metric"""
        print(f"\n Comparing {metric_name}...")

        orch_data = orch_metrics[metric_name]
        choreo_data = choreo_metrics[metric_name]

        if len(orch_data) < 3 or len(choreo_data) < 3:
            return {
                'metric': metric_name,
                'error': 'insufficient_data',
                'orchestrated_samples': len(orch_data),
                'choreographed_samples': len(choreo_data)
            }

        # Descriptive statistics
        comparison = {
            'metric': metric_name,
            'descriptive_stats': {
                'orchestrated': {
                    'mean': statistics.mean(orch_data),
                    'median': statistics.median(orch_data),
                    'std_dev': statistics.stdev(orch_data) if len(orch_data) > 1 else 0,
                    'min': min(orch_data),
                    'max': max(orch_data),
                    'sample_size': len(orch_data)
                },
                'choreographed': {
                    'mean': statistics.mean(choreo_data),
                    'median': statistics.median(choreo_data),
                    'std_dev': statistics.stdev(choreo_data) if len(choreo_data) > 1 else 0,
                    'min': min(choreo_data),
                    'max': max(choreo_data),
                    'sample_size': len(choreo_data)
                }
            }
        }

        # Test for normality
        orch_normality = self.test_normality(orch_data, f"Orchestrated {metric_name}")
        choreo_normality = self.test_normality(choreo_data, f"Choreographed {metric_name}")

        comparison['normality_tests'] = {
            'orchestrated': orch_normality,
            'choreographed': choreo_normality
        }

        # Choose appropriate statistical test
        both_normal = orch_normality['is_normal'] and choreo_normality['is_normal']

        if both_normal:
            # Use t-test if both distributions are normal
            try:
                # Test for equal variances
                levene_stat, levene_p = levene(orch_data, choreo_data)
                equal_var = levene_p > self.alpha

                statistic, p_value = stats.ttest_ind(
                    orch_data, choreo_data, equal_var=equal_var
                )
                test_used = f"Independent t-test (equal_var={equal_var})"

                comparison['statistical_test'] = {
                    'test': test_used,
                    'statistic': statistic,
                    'p_value': p_value,
                    'significant': p_value < self.alpha,
                    'levene_test': {'statistic': levene_stat, 'p_value': levene_p}
                }
            except Exception as e:
                print(f"    Error in t-test: {e}")
                both_normal = False

        if not both_normal:
            # Use Mann-Whitney U test for non-normal data
            try:
                statistic, p_value = mannwhitneyu(
                    orch_data, choreo_data, alternative='two-sided'
                )
                test_used = "Mann-Whitney U test"

                comparison['statistical_test'] = {
                    'test': test_used,
                    'statistic': statistic,
                    'p_value': p_value,
                    'significant': p_value < self.alpha
                }
            except Exception as e:
                print(f"    Error in Mann-Whitney U test: {e}")
                comparison['statistical_test'] = {
                    'test': 'error',
                    'error': str(e)
                }

        # Effect size (Cohen's d)
        try:
            effect_size = self.calculate_cohens_d(orch_data, choreo_data)
            comparison['effect_size'] = {
                'cohens_d': effect_size,
                'interpretation': self.interpret_effect_size(effect_size)
            }
        except Exception as e:
            print(f"    Error calculating effect size: {e}")
            comparison['effect_size'] = {'error': str(e)}

        # Confidence interval for difference in means
        try:
            ci_lower, ci_upper = self.confidence_interval_difference(orch_data, choreo_data)
            comparison['confidence_interval'] = {
                'lower': ci_lower,
                'upper': ci_upper,
                'confidence_level': (1 - self.alpha) * 100
            }
        except Exception as e:
            comparison['confidence_interval'] = {'error': str(e)}

        # Performance winner
        orch_mean = comparison['descriptive_stats']['orchestrated']['mean']
        choreo_mean = comparison['descriptive_stats']['choreographed']['mean']

        if metric_name in ['latencies', 'p95_latencies']:
            # For latency, lower is better
            winner = 'orchestrated' if orch_mean < choreo_mean else 'choreographed'
            improvement = abs(orch_mean - choreo_mean) / max(orch_mean, choreo_mean) * 100
        else:
            # For throughput/success_rate, higher is better
            winner = 'orchestrated' if orch_mean > choreo_mean else 'choreographed'
            improvement = abs(orch_mean - choreo_mean) / min(orch_mean, choreo_mean) * 100

        comparison['performance_analysis'] = {
            'winner': winner,
            'improvement_percent': improvement,
            'statistically_significant': comparison.get('statistical_test', {}).get('significant', False)
        }

        # Print summary
        print(f"   {metric_name} Summary:")
        print(f"    Orchestrated: ={orch_mean:.3f}, ={comparison['descriptive_stats']['orchestrated']['std_dev']:.3f}")
        print(f"    Choreographed: ={choreo_mean:.3f}, ={comparison['descriptive_stats']['choreographed']['std_dev']:.3f}")
        print(f"    Winner: {winner} ({improvement:.1f}% improvement)")

        if 'statistical_test' in comparison:
            print(f"    Statistical test: {comparison['statistical_test'].get('test', 'N/A')}")
            print(f"    Significant: {comparison['statistical_test'].get('significant', False)}")

        return comparison

    def calculate_cohens_d(self, group1, group2):
        """Calculate Cohen's d effect size"""
        mean1, mean2 = statistics.mean(group1), statistics.mean(group2)
        std1, std2 = statistics.stdev(group1), statistics.stdev(group2)
        n1, n2 = len(group1), len(group2)

        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))

        # Cohen's d
        cohens_d = (mean1 - mean2) / pooled_std
        return cohens_d

    def interpret_effect_size(self, cohens_d):
        """Interpret Cohen's d effect size"""
        abs_d = abs(cohens_d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"

    def confidence_interval_difference(self, group1, group2, confidence=0.95):
        """Calculate confidence interval for difference in means"""
        alpha = 1 - confidence

        mean1, mean2 = statistics.mean(group1), statistics.mean(group2)
        var1, var2 = statistics.variance(group1), statistics.variance(group2)
        n1, n2 = len(group1), len(group2)

        # Standard error of the difference
        se_diff = np.sqrt(var1/n1 + var2/n2)

        # Degrees of freedom (Welch's formula)
        df = (var1/n1 + var2/n2)**2 / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1))

        # t critical value
        t_crit = stats.t.ppf(1 - alpha/2, df)

        # Difference in means
        diff = mean1 - mean2

        # Confidence interval
        margin_error = t_crit * se_diff
        ci_lower = diff - margin_error
        ci_upper = diff + margin_error

        return ci_lower, ci_upper

    def run_complete_analysis(self):
        """Run complete statistical analysis"""
        print(f"\n{'='*80}")
        print(" STATISTICAL ANALYSIS - SAGA PATTERN COMPARISON")
        print(f"{'='*80}")

        # Extract metrics
        print("\n Extracting metrics from results...")
        orch_metrics = self.extract_metrics(self.orchestrated_data)
        choreo_metrics = self.extract_metrics(self.choreographed_data)

        print(f"Orchestrated samples: {len(orch_metrics['latencies'])} latency measurements")
        print(f"Choreographed samples: {len(choreo_metrics['latencies'])} latency measurements")

        # Perform statistical comparisons
        metrics_to_compare = ['latencies', 'throughputs', 'success_rates', 'p95_latencies']
        self.results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'significance_level': self.alpha,
            'sample_sizes': {
                'orchestrated': len(orch_metrics['latencies']),
                'choreographed': len(choreo_metrics['latencies'])
            },
            'comparisons': {},
            'summary': {}
        }

        for metric in metrics_to_compare:
            if orch_metrics[metric] and choreo_metrics[metric]:
                comparison = self.compare_metrics(orch_metrics, choreo_metrics, metric)
                self.results['comparisons'][metric] = comparison

        # Generate summary
        self.generate_summary()

        # Generate visualizations
        self.create_visualizations(orch_metrics, choreo_metrics)

        return self.results

    def generate_summary(self):
        """Generate executive summary of statistical analysis"""
        print(f"\n EXECUTIVE SUMMARY")
        print("=" * 50)

        summary = {
            'overall_winner': {},
            'significant_differences': [],
            'effect_sizes': {},
            'recommendations': []
        }

        # Count wins for each pattern
        wins = {'orchestrated': 0, 'choreographed': 0}
        significant_wins = {'orchestrated': 0, 'choreographed': 0}

        for metric, comparison in self.results['comparisons'].items():
            if 'performance_analysis' in comparison:
                winner = comparison['performance_analysis']['winner']
                wins[winner] += 1

                if comparison['performance_analysis']['statistically_significant']:
                    significant_wins[winner] += 1
                    summary['significant_differences'].append({
                        'metric': metric,
                        'winner': winner,
                        'improvement': comparison['performance_analysis']['improvement_percent'],
                        'p_value': comparison.get('statistical_test', {}).get('p_value', 'N/A')
                    })

            # Collect effect sizes
            if 'effect_size' in comparison and 'cohens_d' in comparison['effect_size']:
                summary['effect_sizes'][metric] = {
                    'cohens_d': comparison['effect_size']['cohens_d'],
                    'interpretation': comparison['effect_size']['interpretation']
                }

        # Determine overall winner
        if significant_wins['orchestrated'] > significant_wins['choreographed']:
            overall_winner = 'orchestrated'
        elif significant_wins['choreographed'] > significant_wins['orchestrated']:
            overall_winner = 'choreographed'
        else:
            overall_winner = 'tie'

        summary['overall_winner'] = {
            'pattern': overall_winner,
            'significant_wins': significant_wins,
            'total_wins': wins
        }

        # Generate recommendations
        if len(summary['significant_differences']) > 0:
            summary['recommendations'].append(
                f"Statistical analysis shows significant performance differences in {len(summary['significant_differences'])} metrics"
            )
        else:
            summary['recommendations'].append(
                "No statistically significant performance differences detected between patterns"
            )

        if overall_winner != 'tie':
            summary['recommendations'].append(
                f"Based on statistical evidence, {overall_winner} pattern shows superior performance"
            )

        self.results['summary'] = summary

        # Print summary
        print(f"Overall Winner: {overall_winner}")
        print(f"Statistically Significant Differences: {len(summary['significant_differences'])}")
        for diff in summary['significant_differences']:
            print(f"   {diff['metric']}: {diff['winner']} wins by {diff['improvement']:.1f}%")

    def create_visualizations(self, orch_metrics, choreo_metrics):
        """Create statistical visualizations"""
        print(f"\n Creating visualizations...")

        try:
            # Set style
            try:
                plt.style.use('seaborn-v0_8')
            except:
                plt.style.use('seaborn')
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Saga Pattern Performance Comparison', fontsize=16, fontweight='bold')

            # Latency comparison
            if orch_metrics['latencies'] and choreo_metrics['latencies']:
                axes[0,0].hist(orch_metrics['latencies'], alpha=0.7, label='Orchestrated', bins=15)
                axes[0,0].hist(choreo_metrics['latencies'], alpha=0.7, label='Choreographed', bins=15)
                axes[0,0].set_title('Latency Distribution')
                axes[0,0].set_xlabel('Latency (ms)')
                axes[0,0].set_ylabel('Frequency')
                axes[0,0].legend()

            # Throughput comparison
            if orch_metrics['throughputs'] and choreo_metrics['throughputs']:
                axes[0,1].hist(orch_metrics['throughputs'], alpha=0.7, label='Orchestrated', bins=15)
                axes[0,1].hist(choreo_metrics['throughputs'], alpha=0.7, label='Choreographed', bins=15)
                axes[0,1].set_title('Throughput Distribution')
                axes[0,1].set_xlabel('Throughput (req/s)')
                axes[0,1].set_ylabel('Frequency')
                axes[0,1].legend()

            # Box plot comparison
            latency_data = [orch_metrics['latencies'], choreo_metrics['latencies']]
            axes[1,0].boxplot(latency_data, labels=['Orchestrated', 'Choreographed'])
            axes[1,0].set_title('Latency Box Plot')
            axes[1,0].set_ylabel('Latency (ms)')

            # Success rate comparison
            if orch_metrics['success_rates'] and choreo_metrics['success_rates']:
                axes[1,1].hist(orch_metrics['success_rates'], alpha=0.7, label='Orchestrated', bins=10)
                axes[1,1].hist(choreo_metrics['success_rates'], alpha=0.7, label='Choreographed', bins=10)
                axes[1,1].set_title('Success Rate Distribution')
                axes[1,1].set_xlabel('Success Rate')
                axes[1,1].set_ylabel('Frequency')
                axes[1,1].legend()

            plt.tight_layout()

            # Save visualization
            viz_filename = f"statistical_analysis_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(viz_filename, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"[OK] Visualization saved: {viz_filename}")

        except Exception as e:
            print(f"[WARN] Error creating visualizations: {e}")

    def save_results(self, filename=None):
        """Save statistical analysis results"""
        if filename is None:
            filename = f"statistical_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"[OK] Statistical analysis saved: {filename}")
            return filename
        except Exception as e:
            print(f"[ERROR] Error saving results: {e}")
            return None


def main():
    """Main execution function"""
    import sys

    if len(sys.argv) != 3:
        print("Usage: python statistical_analysis.py <orchestrated_results.json> <choreographed_results.json>")
        sys.exit(1)

    orchestrated_file = sys.argv[1]
    choreographed_file = sys.argv[2]

    # Create analyzer
    analyzer = StatisticalAnalyzer(significance_level=0.05)

    # Load data
    if not analyzer.load_pattern_results(orchestrated_file, choreographed_file):
        print("[ERROR] Failed to load pattern results")
        sys.exit(1)

    # Run analysis
    results = analyzer.run_complete_analysis()

    # Save results
    output_file = analyzer.save_results()

    print(f"\n Statistical analysis complete!")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()