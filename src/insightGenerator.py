"""
Insight Generator - Comprehensive Insights for Non-Technical Users
Transforms complex metrics into simple, actionable, and understandable insights
Includes different analysis types with clear language suitable for all audiences
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any


class InsightGenerator:
    """Generate human-readable insights from UIDAI analysis metrics"""

    def __init__(self, analysis_results: Dict[str, Any]):
        """Initialize with analysis results from enhanced analysis module"""
        self.results = analysis_results
        self.insights = []
        self.recommendations = []
        self.generate_all_insights()

    # ============================================================================
    # TEMPORAL INSIGHTS (Growth & Trends)
    # ============================================================================

    def generate_temporal_insight(self) -> Dict[str, Any]:
        """Generate growth trajectory insight (non-technical language)"""
        temporal = self.results.get('temporal_metrics', {})
        growth = temporal.get('avg_growth_rate', 0)
        trend = temporal.get('trend_direction', 'stable')
        peak_count = temporal.get('peak_count', 0)

        if growth > 20:
            return {
                'title': 'EXCEPTIONAL GROWTH - Accelerating Fast',
                'message': f'The enrollment is growing at {growth:.1f}% daily - this is outstanding! '
                          f'It is experiencing rapid expansion with peak day reaching {peak_count:,} enrollments. '
                          f'Trend: {trend.upper()}',
                'details': 'Growth above 20% daily indicates explosive expansion. This is exceptional and requires '
                          'infrastructure scaling to handle the volume.',
                'action': 'Scale infrastructure immediately to handle increased volume',
                'severity': 'positive',
                'type': 'temporal'
            }
        elif growth > 10:
            return {
                'title': 'STRONG GROWTH - On Track',
                'message': f'Daily growth rate is {growth:.1f}% - excellent performance! '
                          f'This system is expanding well with consistent positive momentum. '
                          f'Trend: {trend.upper()}',
                'details': 'Growth between 10-20% is strong and sustainable. The enrollment system is performing well.',
                'action': 'Maintain momentum and continue monitoring capacity',
                'severity': 'positive',
                'type': 'temporal'
            }
        elif growth > 5:
            return {
                'title': 'STEADY GROWTH - Healthy Progress',
                'message': f'Enrollment is growing steadily at {growth:.1f}% daily. '
                          f'This is on track with consistent, healthy expansion. '
                          f'Trend: {trend.upper()}',
                'details': '5-10% daily growth is healthy and sustainable long-term.',
                'action': 'Continue current strategy while planning for scaling',
                'severity': 'info',
                'type': 'temporal'
            }
        else:
            return {
                'title': 'SLOW GROWTH - Needs Attention',
                'message': f'Growth rate is {growth:.1f}% daily - below target. '
                          f'Trend: {trend.upper()}. The enrollment needs a boost.',
                'details': 'Below 5% daily growth suggests the need for campaign improvements.',
                'action': 'Review marketing campaigns and identify growth barriers',
                'severity': 'warning',
                'type': 'temporal'
            }

    def generate_peak_activity_insight(self) -> Dict[str, Any]:
        """Insight about peak enrollment days"""
        temporal = self.results.get('temporal_metrics', {})
        peak_count = temporal.get('peak_count', 0)
        peak_day = temporal.get('peak_day', 'N/A')

        return {
            'title': 'PEAK ACTIVITY - The Busiest Day',
            'message': f'The peak enrollment day recorded {peak_count:,} registrations on {peak_day}. '
                      f'This shows the system\'s maximum capacity and user interest level.',
            'details': 'Understanding peak capacity helps with infrastructure planning and resource allocation.',
            'action': 'Use peak day data to plan infrastructure and staffing',
            'severity': 'info',
            'type': 'temporal'
        }

    def generate_weekly_consistency_insight(self) -> Dict[str, Any]:
        """Insight about week-to-week consistency"""
        temporal = self.results.get('temporal_metrics', {})
        weekly_stats = temporal.get('weekly_stats', {})
        avg_weekly = weekly_stats.get('avg_weekly', 0)
        variance = weekly_stats.get('weekly_variance', 0)

        if variance and avg_weekly:
            cv = (variance / avg_weekly) * 100
        else:
            cv = 0

        if cv < 15:
            status = 'Highly Consistent - Predictable patterns'
            severity = 'positive'
        elif cv < 30:
            status = 'Moderately Consistent - Some variation'
            severity = 'info'
        else:
            status = 'Highly Variable - Unpredictable patterns'
            severity = 'warning'

        return {
            'title': 'WEEKLY PATTERNS - Predictability Check',
            'message': f'Average weekly enrollment: {avg_weekly:,} registrations. '
                      f'Status: {status}. This tells how predictable the enrollment patterns are.',
            'details': 'Low variation means you can forecast demand accurately. High variation requires flexible resources.',
            'action': 'Plan staffing and resources based on consistency level',
            'severity': severity,
            'type': 'temporal'
        }

    # ============================================================================
    # GEOGRAPHIC INSIGHTS (Distribution & Concentration)
    # ============================================================================

    def generate_geographic_insight(self) -> Dict[str, Any]:
        """Generate geographic concentration insight in simple terms"""
        geo = self.results.get('geographic_metrics', {})
        hhi = geo.get('herfindahl_index', 0)
        top_state_pct = geo.get('top_state_percentage', 0)
        top_state = geo.get('top_state', 'N/A')

        if hhi > 2500:
            return {
                'title': 'HIGH CONCENTRATION - Unbalanced Distribution',
                'message': f'{top_state} dominates with {top_state_pct:.1f}% of all enrollments. '
                          f'The enrollment is heavily concentrated in one region. This means most of the '
                          f'users are from a specific area.',
                'details': 'High concentration (HHI > 2500) indicates unbalanced geographic distribution. '
                          'This creates risk if that region experiences disruption.',
                'action': 'Launch targeted campaigns in underserved regions',
                'severity': 'warning',
                'type': 'geographic'
            }
        elif hhi > 2000:
            return {
                'title': 'MODERATE CONCENTRATION - Room for Growth',
                'message': f'{top_state} leads with {top_state_pct:.1f}% of enrollments. '
                          f'The distribution is somewhat unbalanced but manageable. '
                          f'There\'s good opportunity for geographic expansion.',
                'details': 'Moderate concentration suggests some regional imbalance but with diversification potential.',
                'action': 'Focus on expanding in tier-2 and tier-3 cities',
                'severity': 'info',
                'type': 'geographic'
            }
        else:
            return {
                'title': 'BALANCED DISTRIBUTION - Well Spread',
                'message': f'Enrollments are well-distributed across regions. '
                          f'Top state ({top_state}) has only {top_state_pct:.1f}%. '
                          f'This excellent geographic diversity reduces regional risk.',
                'details': 'Low concentration (HHI < 2000) indicates healthy geographic distribution.',
                'action': 'Continue expanding in new regions',
                'severity': 'positive',
                'type': 'geographic'
            }

    def generate_state_coverage_insight(self) -> Dict[str, Any]:
        """Insight about number of states covered"""
        geo = self.results.get('geographic_metrics', {})
        num_states = geo.get('num_states', 0)
        coverage_pct = (num_states / 36) * 100  # India has 36 states/UTs

        if num_states >= 30:
            status = 'Excellent - Nearly complete coverage'
            severity = 'positive'
        elif num_states >= 20:
            status = 'Good - Significant coverage'
            severity = 'info'
        else:
            status = 'Limited - Room for expansion'
            severity = 'warning'

        return {
            'title': 'GEOGRAPHIC COVERAGE - State Distribution',
            'message': f'The service covers {num_states} states/UTs ({coverage_pct:.0f}% of India). '
                      f'Status: {status}. This shows the national reach.',
            'details': 'Higher coverage means better national presence and reduced geographic risk.',
            'action': f'Plan expansion to reach remaining {36 - num_states} regions' if num_states < 36 else 'Maintain national coverage',
            'severity': severity,
            'type': 'geographic'
        }

    # ============================================================================
    # DEMOGRAPHIC INSIGHTS (Age & Gender)
    # ============================================================================

    def generate_demographic_insight(self) -> Dict[str, Any]:
        """Generate demographic diversity insight"""
        demo = self.results.get('demographic_metrics', {})
        diversity = demo.get('age_diversity_index', 0)
        dominant_pct = demo.get('dominant_age_percentage', 0)
        dominant_age = demo.get('dominant_age', 'N/A')

        if diversity > 0.8:
            return {
                'title': 'EXCELLENT DIVERSITY - All Groups Well Represented',
                'message': f'The enrollment is highly diverse across all age groups. '
                          f'No single age group dominates (largest is {dominant_pct:.1f}%). '
                          f'This indicates inclusive outreach and balanced participation.',
                'details': 'High diversity (>0.8) means the service appeals to all demographics.',
                'action': 'Maintain inclusive engagement strategies',
                'severity': 'positive',
                'type': 'demographic'
            }
        elif diversity > 0.6:
            return {
                'title': 'GOOD DIVERSITY - Balanced Participation',
                'message': f'Most age groups are well-represented, though {dominant_age} leads '
                          f'with {dominant_pct:.1f}%. The enrollment is reasonably balanced.',
                'details': 'Moderate diversity (0.6-0.8) shows balanced but not perfect representation.',
                'action': 'Monitor underrepresented groups for equity',
                'severity': 'info',
                'type': 'demographic'
            }
        elif diversity > 0.4:
            return {
                'title': 'MODERATE SKEW - Some Groups Underrepresented',
                'message': f'{dominant_age} accounts for {dominant_pct:.1f}% of enrollments. '
                          f'Other age groups are underrepresented. This needs attention.',
                'details': 'Lower diversity suggests some demographic groups are not being reached.',
                'action': 'Launch targeted outreach for underrepresented age groups',
                'severity': 'warning',
                'type': 'demographic'
            }
        else:
            return {
                'title': 'CRITICAL SKEW - Severe Demographic Imbalance',
                'message': f'{dominant_age} dominates with {dominant_pct:.1f}% of enrollments. '
                          f'Other demographic groups are significantly underrepresented. '
                          f'This is a critical gap that needs immediate action.',
                'details': 'Very low diversity indicates major demographic gaps in the service.',
                'action': 'Launch immediate diversity and inclusion campaigns',
                'severity': 'critical',
                'type': 'demographic'
            }

    def generate_gender_insight(self) -> Dict[str, Any]:
        """Insight about gender distribution"""
        demo = self.results.get('demographic_metrics', {})
        gender_dist = demo.get('gender_distribution', {})

        if not gender_dist:
            return {}

        # Calculate gender ratio
        sorted_gender = sorted(gender_dist.items(), key=lambda x: x[1], reverse=True)
        max_gender = sorted_gender[0]
        min_gender = sorted_gender[-1]
        ratio = max_gender[1] / min_gender[1] if min_gender[1] > 0 else 0

        if ratio < 1.2:
            status = 'Excellent - Nearly equal participation'
            severity = 'positive'
        elif ratio < 1.5:
            status = 'Good - Fairly balanced'
            severity = 'info'
        else:
            status = 'Imbalanced - One gender dominates'
            severity = 'warning'

        return {
            'title': 'GENDER BALANCE - Equality Check',
            'message': f'Gender distribution ratio is {ratio:.2f}:1 ({max_gender[0]} to {min_gender[0]}). '
                      f'Status: {status}. Aim for equal participation from all genders.',
            'details': 'Balanced gender representation ensures inclusive service delivery.',
            'action': 'If imbalanced, increase outreach to underrepresented gender',
            'severity': severity,
            'type': 'demographic'
        }

    # ============================================================================
    # DATA QUALITY INSIGHTS
    # ============================================================================

    def generate_quality_insight(self) -> Dict[str, Any]:
        """Generate data quality insight"""
        quality = self.results.get('quality_metrics', {})
        completeness = quality.get('overall_completeness', 0)
        issues = quality.get('issues', {})
        total_issues = issues.get('total_issues', 0)

        if completeness > 97:
            return {
                'title': 'EXCELLENT DATA QUALITY - Premium Standard',
                'message': f'Data completeness is {completeness:.1f}%. The data is pristine with minimal issues. '
                          f'This ensures reliable analysis and decision-making.',
                'details': 'Excellent data quality (>97%) means high confidence in analytics.',
                'action': 'Maintain current data collection standards',
                'severity': 'positive',
                'type': 'quality'
            }
        elif completeness > 93:
            return {
                'title': 'GOOD DATA QUALITY - Reliable',
                'message': f'Data completeness is {completeness:.1f}%. Quality is good with minimal issues. '
                          f'The data is reliable for analysis.',
                'details': 'Good data quality (93-97%) is acceptable for most purposes.',
                'action': 'Monitor and continue gradual improvements',
                'severity': 'info',
                'type': 'quality'
            }
        elif completeness > 85:
            return {
                'title': 'MODERATE QUALITY - Needs Attention',
                'message': f'Data completeness is {completeness:.1f}% with {total_issues:,} identified issues. '
                          f'Quality needs improvement for reliable analysis.',
                'details': 'Below 93% completeness means important data gaps exist.',
                'action': 'Identify and fix data collection gaps systematically',
                'severity': 'warning',
                'type': 'quality'
            }
        else:
            return {
                'title': 'POOR DATA QUALITY - Critical',
                'message': f'Data completeness is only {completeness:.1f}% with {total_issues:,} critical issues. '
                          f'Data quality is severely compromised.',
                'details': 'Below 85% completeness severely impacts reliability.',
                'action': 'Urgently review and fix data collection procedures',
                'severity': 'critical',
                'type': 'quality'
            }

    def generate_duplicates_insight(self) -> Dict[str, Any]:
        """Insight about duplicate records"""
        quality = self.results.get('quality_metrics', {})
        issues = quality.get('issues', {})
        duplicates = issues.get('duplicate_records', 0)
        total_records = quality.get('total_records', 1)
        dup_pct = (duplicates / total_records * 100) if total_records > 0 else 0

        if duplicates == 0:
            status = 'Perfect - No duplicates'
            severity = 'positive'
        elif dup_pct < 0.5:
            status = 'Acceptable - Minimal duplicates'
            severity = 'info'
        else:
            status = 'Concerning - Significant duplication'
            severity = 'warning'

        return {
            'title': 'DUPLICATE RECORDS - Data Integrity Check',
            'message': f'Found {duplicates:,} duplicate records ({dup_pct:.2f}%). '
                      f'Status: {status}. This affects data accuracy.',
            'details': 'Duplicates can skew analysis results and inflate enrollment numbers.',
            'action': 'Implement duplicate detection and removal procedures',
            'severity': severity,
            'type': 'quality'
        }

    # ============================================================================
    # BIOMETRIC INSIGHTS
    # ============================================================================

    def generate_biometric_insight(self) -> Dict[str, Any]:
        """Insight about biometric coverage"""
        bio = self.results.get('biometric_metrics', {})

        if not bio:
            return {}

        # Calculate average biometric coverage
        bio_ages = []
        for key, val in bio.items():
            if isinstance(val, dict):
                bio_ages.append(val.get('percentage', 0))

        if bio_ages:
            avg_coverage = np.mean(bio_ages)
        else:
            avg_coverage = 0

        if avg_coverage > 90:
            status = 'Excellent - High biometric collection'
            severity = 'positive'
        elif avg_coverage > 70:
            status = 'Good - Solid coverage'
            severity = 'info'
        else:
            status = 'Low - Needs improvement'
            severity = 'warning'

        return {
            'title': 'BIOMETRIC COVERAGE - Fingerprint Enrollment',
            'message': f'Biometric enrollment coverage is {avg_coverage:.1f}%. '
                      f'Status: {status}. This shows fingerprint data collection rates.',
            'details': 'Higher biometric coverage ensures better identity verification capability.',
            'action': 'Increase biometric collection during enrollment',
            'severity': severity,
            'type': 'biometric'
        }

    # ============================================================================
    # UPDATE INSIGHTS
    # ============================================================================

    def generate_update_insight(self) -> Dict[str, Any]:
        """Insight about update patterns"""
        updates = self.results.get('update_metrics', {})
        bio_ratio = updates.get('biometric_to_enrol_ratio', 0)
        demo_ratio = updates.get('demographic_to_enrol_ratio', 0)
        total_update_ratio = bio_ratio + demo_ratio

        if total_update_ratio > 0.5:
            status = 'High - Frequent updates'
            severity = 'positive'
        elif total_update_ratio > 0.2:
            status = 'Moderate - Regular updates'
            severity = 'info'
        else:
            status = 'Low - Limited updates'
            severity = 'warning'

        return {
            'title': 'UPDATE FREQUENCY - System Activity',
            'message': f'Update-to-enrollment ratio is {total_update_ratio:.2f}. '
                      f'Status: {status}. This shows how active users are updating their data.',
            'details': 'Higher update ratios indicate engaged users maintaining accurate information.',
            'action': 'Encourage regular data updates and maintenance',
            'severity': severity,
            'type': 'update'
        }

    # ============================================================================
    # TREND INSIGHTS (Advanced)
    # ============================================================================

    def generate_volatility_insight(self) -> Dict[str, Any]:
        """Insight about enrollment volatility"""
        trends = self.results.get('trend_metrics', {})
        volatility_level = trends.get('volatility_level', 'Medium')

        volatility_msg = {
            'High': ('Highly Variable - Unpredictable daily changes', 'warning'),
            'Medium': ('Moderate Variability - Some daily fluctuation', 'info'),
            'Low': ('Stable - Consistent daily patterns', 'positive')
        }

        msg, severity = volatility_msg.get(volatility_level, ('Unknown', 'info'))

        return {
            'title': 'ENROLLMENT VOLATILITY - Stability Check',
            'message': f'Volatility Level: {msg}. This affects resource planning and forecasting.',
            'details': f'{volatility_level} volatility means daily enrollments {"vary significantly" if volatility_level == "High" else "fluctuate moderately" if volatility_level == "Medium" else "remain stable"}.',
            'action': f'{"Use flexible resource planning" if volatility_level == "High" else "Maintain current planning" if volatility_level == "Medium" else "Optimize fixed resource allocation"}',
            'severity': severity,
            'type': 'trend'
        }

    # ============================================================================
    # CAPACITY INSIGHTS
    # ============================================================================

    def generate_capacity_insight(self) -> Dict[str, Any]:
        """Insight about system capacity utilization"""
        temporal = self.results.get('temporal_metrics', {})
        peak_count = temporal.get('peak_count', 0)
        avg_daily = temporal.get('total_records', 0)

        if avg_daily > 0:
            avg_daily = avg_daily / 365  # rough estimate

        utilization = (avg_daily / peak_count * 100) if peak_count > 0 else 0

        if utilization > 80:
            status = 'High Load - Operating near capacity'
            severity = 'warning'
        elif utilization > 50:
            status = 'Moderate Load - Good headroom'
            severity = 'info'
        else:
            status = 'Low Load - Plenty of capacity'
            severity = 'positive'

        return {
            'title': 'SYSTEM CAPACITY - Load Analysis',
            'message': f'Average-to-peak utilization is {utilization:.1f}%. Status: {status}. '
                      f'This shows how efficiently the system capacity is being used.',
            'details': 'Capacity planning ensures it can handle peak loads without degradation.',
            'action': f'{"Upgrade infrastructure urgently" if utilization > 80 else "Monitor capacity trends" if utilization > 50 else "Maintain current capacity"}',
            'severity': severity,
            'type': 'capacity'
        }

    # ============================================================================
    # RECOMMENDATION GENERATION
    # ============================================================================

    def generate_all_insights(self) -> None:
        """Generate all insights in priority order"""
        # Priority order: Critical, High-impact, Informational

        # Critical insights first
        self.insights.append(self.generate_quality_insight())
        self.insights.append(self.generate_temporal_insight())

        # High-impact insights
        self.insights.append(self.generate_geographic_insight())
        self.insights.append(self.generate_demographic_insight())

        # Supporting insights
        self.insights.append(self.generate_peak_activity_insight())
        self.insights.append(self.generate_weekly_consistency_insight())
        self.insights.append(self.generate_state_coverage_insight())
        self.insights.append(self.generate_gender_insight())
        self.insights.append(self.generate_duplicates_insight())
        self.insights.append(self.generate_biometric_insight())
        self.insights.append(self.generate_update_insight())
        self.insights.append(self.generate_volatility_insight())
        self.insights.append(self.generate_capacity_insight())

        # Filter out None/empty insights
        self.insights = [i for i in self.insights if i]

        # Generate recommendations
        self.generate_recommendations()

    def generate_recommendations(self) -> None:
        """Generate actionable recommendations"""
        self.recommendations = []

        # Add critical action items
        for insight in self.insights:
            if insight.get('severity') in ['critical', 'warning']:
                self.recommendations.append(f"{insight.get('action', 'Review insight')}")

        # Add positive reinforcements
        for insight in self.insights:
            if insight.get('severity') == 'positive':
                self.recommendations.append(f"{insight.get('action', 'Continue current approach')}")

        # Default recommendations
        if not self.recommendations:
            self.recommendations = [
                "Monitor all key metrics regularly",
                "Maintain current data collection standards",
                "Review system performance weekly",
                "Plan quarterly improvement initiatives"
            ]

        # Limit to top 10
        self.recommendations = self.recommendations[:10]

    # ============================================================================
    # RETRIEVAL METHODS
    # ============================================================================

    def get_all_insights(self) -> List[Dict[str, Any]]:
        """Get all generated insights"""
        return self.insights

    def get_insights_by_type(self, insight_type: str) -> List[Dict[str, Any]]:
        """Get insights filtered by type"""
        return [i for i in self.insights if i.get('type') == insight_type]

    def get_insights_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Get insights filtered by severity"""
        return [i for i in self.insights if i.get('severity') == severity]

    def get_key_recommendations(self) -> List[str]:
        """Get top 5 recommendations"""
        return self.recommendations[:5]

    def get_summary_text(self) -> str:
        """Get summary for dashboard display"""
        critical = len(self.get_insights_by_severity('critical'))
        warning = len(self.get_insights_by_severity('warning'))
        positive = len(self.get_insights_by_severity('positive'))

        if critical > 0:
            status = ' CRITICAL - Immediate Action Required'
            color = '#ef4444'
        elif warning > 0:
            status = ' CAUTION - Review Needed'
            color = '#f59e0b'
        else:
            status = ' ON TRACK - Healthy Performance'
            color = '#10b981'

        summary = (
            f'<div style="background-color:{color}; color:white; padding:15px; border-radius:8px; margin-bottom:20px;">'
            f'<h1 style="margin:8 px; font-size:18px;"> {status}</h2>'
            f'<p style="margin:8px 0 0 0; font-size:14px; font-weight:bold;">'
            f'Dashboard shows: {positive} positive metrics, {warning} warnings, {critical} critical issues. '
            f'Review details below.</p>'
            f'</div>'
        )

        return summary

    def to_json_safe(self) -> Dict[str, Any]:
        """Convert all insights to JSON-safe format"""
        return {
            'insights': self.insights,
            'recommendations': self.recommendations,
            'summary': {
                'total_insights': len(self.insights),
                'critical': len(self.get_insights_by_severity('critical')),
                'warning': len(self.get_insights_by_severity('warning')),
                'positive': len(self.get_insights_by_severity('positive')),
                'info': len(self.get_insights_by_severity('info'))
            }
        }