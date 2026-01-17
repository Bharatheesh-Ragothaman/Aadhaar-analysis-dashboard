"""
Enhanced Analysis Module for UIDAI Aadhaar Data
Includes: Temporal, Geographic, Demographic, Biometric, Update, Quality & Trend Analysis
Provides metrics understandable to non-technical users
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')


class AdvancedTemporalAnalysis:
    """Analyze enrollment trends over time"""
    
    def __init__(self, df):
        self.df = df
        self.date_col = self._find_date_column()
        self.enrol_col = self._find_enrollment_column()
    
    def _find_date_column(self):
        for col in self.df.columns:
            if 'date' in col.lower():
                return col
        return None
    
    def _find_enrollment_column(self):
        for col in self.df.columns:
            if 'total' in col.lower() or 'enrol' in col.lower():
                return col
        return None
    
    def calculate_growth_rate(self) -> Dict[str, Any]:
        """Calculate daily, weekly, and monthly growth rates"""
        if not self.date_col or not self.enrol_col:
            return {}
        
        try:
            daily_data = self.df.groupby(self.date_col)[self.enrol_col].sum().reset_index()
            daily_data = daily_data.sort_values(self.date_col)
            
            if len(daily_data) < 2:
                return {'avg_growth_rate': 0, 'trend_direction': 'stable', 'peak_day': None}
            
            # Calculate growth rates
            daily_data['growth'] = daily_data[self.enrol_col].pct_change() * 100
            avg_growth = daily_data['growth'].mean()
            peak_growth = daily_data['growth'].max()
            lowest_growth = daily_data['growth'].min()
            
            # Determine trend
            recent_growth = daily_data['growth'].tail(10).mean()
            if recent_growth > 5:
                trend = 'upward'
            elif recent_growth < -5:
                trend = 'downward'
            else:
                trend = 'stable'
            
            # Peak day
            peak_idx = daily_data[self.enrol_col].idxmax()
            peak_day = daily_data.loc[peak_idx, self.date_col]
            peak_count = daily_data.loc[peak_idx, self.enrol_col]
            
            return {
                'avg_growth_rate': avg_growth,
                'peak_growth_rate': peak_growth,
                'lowest_growth_rate': lowest_growth,
                'trend_direction': trend,
                'peak_day': peak_day,
                'peak_count': peak_count,
                'total_records': int(daily_data[self.enrol_col].sum())
            }
        except Exception as e:
            return {'error': str(e)}
    
    def detect_anomalous_days(self) -> pd.DataFrame:
        """Identify unusual enrollment patterns using IQR method"""
        if not self.date_col or not self.enrol_col:
            return pd.DataFrame()
        
        try:
            daily_data = self.df.groupby(self.date_col)[self.enrol_col].sum().reset_index()
            daily_data = daily_data.sort_values(self.date_col)
            
            # IQR method
            Q1 = daily_data[self.enrol_col].quantile(0.25)
            Q3 = daily_data[self.enrol_col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            anomalies = daily_data[
                (daily_data[self.enrol_col] < lower_bound) | 
                (daily_data[self.enrol_col] > upper_bound)
            ].copy()
            
            return anomalies
        except Exception as e:
            return pd.DataFrame()
    
    def get_weekly_statistics(self) -> Dict[str, Any]:
        """Calculate weekly enrollment statistics"""
        if not self.date_col or not self.enrol_col:
            return {}
        
        try:
            weekly_data = self.df.copy()
            weekly_data[self.date_col] = pd.to_datetime(weekly_data[self.date_col])
            weekly_data['week'] = weekly_data[self.date_col].dt.isocalendar().week
            
            weekly_stats = weekly_data.groupby('week')[self.enrol_col].agg(['sum', 'mean', 'std']).reset_index()
            
            return {
                'avg_weekly': int(weekly_stats['sum'].mean()),
                'best_week': int(weekly_stats['sum'].max()),
                'worst_week': int(weekly_stats['sum'].min()),
                'weekly_variance': float(weekly_stats['sum'].std())
            }
        except Exception as e:
            return {}
    
    def get_monthly_trends(self) -> pd.DataFrame:
        """Get month-over-month enrollment trends"""
        if not self.date_col or not self.enrol_col:
            return pd.DataFrame()
        
        try:
            monthly_data = self.df.copy()
            monthly_data[self.date_col] = pd.to_datetime(monthly_data[self.date_col])
            monthly_data['year_month'] = monthly_data[self.date_col].dt.to_period('M')
            
            monthly_trends = monthly_data.groupby('year_month')[self.enrol_col].sum().reset_index()
            monthly_trends.columns = ['Month', 'Enrollments']
            
            return monthly_trends
        except Exception as e:
            return pd.DataFrame()


class GeographicAnalysis:
    """Analyze geographic distribution and concentration"""
    
    def __init__(self, df):
        self.df = df
        self.state_col = self._find_state_column()
        self.district_col = self._find_district_column()
        self.enrol_col = self._find_enrollment_column()
    
    def _find_state_column(self):
        for col in self.df.columns:
            if 'state' in col.lower():
                return col
        return None
    
    def _find_district_column(self):
        for col in self.df.columns:
            if 'district' in col.lower():
                return col
        return None
    
    def _find_enrollment_column(self):
        for col in self.df.columns:
            if 'total' in col.lower():
                return col
        return None
    
    def calculate_concentration(self) -> Dict[str, Any]:
        """Calculate HHI and Gini coefficient for geographic concentration"""
        if not self.state_col or not self.enrol_col:
            return {}
        
        try:
            state_data = self.df.groupby(self.state_col)[self.enrol_col].sum()
            total = state_data.sum()
            shares = (state_data / total) * 100
            
            # Herfindahl-Hirschman Index
            hhi = (shares ** 2).sum()
            
            # Gini Coefficient
            sorted_shares = np.sort(shares.values)
            n = len(sorted_shares)
            gini = (2 * np.sum((np.arange(1, n + 1) * sorted_shares))) / (n * sorted_shares.sum()) - (n + 1) / n
            
            # Top states share
            top_5_share = shares.nlargest(5).sum()
            top_10_share = shares.nlargest(10).sum()
            top_state = shares.idxmax()
            top_state_pct = shares.max()
            
            return {
                'herfindahl_index': hhi,
                'gini_coefficient': gini,
                'top_state': top_state,
                'top_state_percentage': top_state_pct,
                'top_5_states_share': top_5_share,
                'top_10_states_share': top_10_share,
                'num_states': len(state_data),
                'concentration_level': 'High' if hhi > 2500 else 'Moderate' if hhi > 2000 else 'Low'
            }
        except Exception as e:
            return {}
    
    def get_state_distribution(self) -> pd.DataFrame:
        """Get enrollment distribution by state"""
        if not self.state_col or not self.enrol_col:
            return pd.DataFrame()
        
        try:
            state_dist = self.df.groupby(self.state_col)[self.enrol_col].sum().reset_index()
            state_dist.columns = ['State', 'Enrollments']
            state_dist = state_dist.sort_values('Enrollments', ascending=False)
            state_dist['Percentage'] = (state_dist['Enrollments'] / state_dist['Enrollments'].sum() * 100).round(2)
            
            return state_dist
        except Exception as e:
            return pd.DataFrame()
    
    def get_district_distribution(self) -> pd.DataFrame:
        """Get enrollment distribution by district"""
        if not self.district_col or not self.enrol_col:
            return pd.DataFrame()
        
        try:
            district_dist = self.df.groupby(self.district_col)[self.enrol_col].sum().reset_index()
            district_dist.columns = ['District', 'Enrollments']
            district_dist = district_dist.sort_values('Enrollments', ascending=False)
            
            return district_dist.head(50)
        except Exception as e:
            return pd.DataFrame()


class DemographicAnalysis:
    """Analyze age and gender distributions"""
    
    def __init__(self, df):
        self.df = df
        self.age_cols = self._find_age_columns()
        self.gender_col = self._find_gender_column()
    
    def _find_age_columns(self):
        age_cols = []
        for col in self.df.columns:
            if 'age' in col.lower():
                age_cols.append(col)
        return age_cols
    
    def _find_gender_column(self):
        for col in self.df.columns:
            if 'gender' in col.lower():
                return col
        return None
    
    def analyze_age_distribution(self) -> Dict[str, Any]:
        """Analyze age group diversity and skewness"""
        if not self.age_cols:
            return {}
        
        try:
            age_totals = {}
            for col in self.age_cols:
                age_totals[col] = int(self.df[col].sum())
            
            total = sum(age_totals.values())
            age_percentages = {k: (v / total * 100) if total > 0 else 0 for k, v in age_totals.items()}
            
            # Diversity Index (Simpson's D)
            diversity = 1 - sum([(v / total) ** 2 for v in age_totals.values()]) if total > 0 else 0
            
            # Skewness - find dominant age group
            dominant_age = max(age_percentages.items(), key=lambda x: x[1])
            
            # Entropy
            entropy = -sum([(v / total) * np.log(v / total + 1e-10) for v in age_totals.values()]) if total > 0 else 0
            
            return {
                'age_diversity_index': diversity,
                'entropy': entropy,
                'dominant_age': dominant_age[0],
                'dominant_age_percentage': dominant_age[1],
                'age_groups': age_percentages,
                'age_totals': age_totals
            }
        except Exception as e:
            return {}
    
    def analyze_gender_distribution(self) -> Dict[str, Any]:
        """Analyze gender distribution"""
        if not self.gender_col:
            return {}
        
        try:
            gender_dist = self.df[self.gender_col].value_counts()
            total = gender_dist.sum()
            
            return {
                'gender_distribution': gender_dist.to_dict(),
                'percentages': {k: (v / total * 100) for k, v in gender_dist.items()},
                'balance_ratio': max(gender_dist.values) / min(gender_dist.values) if min(gender_dist.values) > 0 else 0
            }
        except Exception as e:
            return {}


class DataQualityAnalysis:
    """Analyze data quality metrics"""
    
    def __init__(self, df):
        self.df = df
    
    def calculate_completeness(self) -> Dict[str, Any]:
        """Calculate data completeness percentage"""
        try:
            total_cells = self.df.shape[0] * self.df.shape[1]
            non_null_cells = self.df.count().sum()
            completeness = (non_null_cells / total_cells * 100) if total_cells > 0 else 0
            
            column_completeness = (self.df.count() / len(self.df) * 100).to_dict()
            
            return {
                'overall_completeness': completeness,
                'column_completeness': column_completeness,
                'null_percentage': 100 - completeness
            }
        except Exception as e:
            return {}
    
    def identify_data_quality_issues(self) -> Dict[str, Any]:
        """Identify and count quality issues"""
        try:
            issues = {
                'duplicate_records': self.df.duplicated().sum(),
                'zero_enrollment_records': (self.df.select_dtypes(include=[np.number]).sum(axis=1) == 0).sum(),
                'outlier_records': 0,
                'null_percentage': (self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1]) * 100),
                'total_issues': 0
            }
            
            # Detect outliers using IQR for numeric columns
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            outlier_count = 0
            for col in numeric_cols:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((self.df[col] < Q1 - 1.5 * IQR) | (self.df[col] > Q3 + 1.5 * IQR)).sum()
                outlier_count += outliers
            
            issues['outlier_records'] = outlier_count
            issues['total_issues'] = sum([v for k, v in issues.items() if k != 'null_percentage'])
            
            return issues
        except Exception as e:
            return {}
    
    def get_quality_status(self) -> str:
        """Get overall data quality status"""
        completeness = self.calculate_completeness().get('overall_completeness', 0)
        
        if completeness >= 95:
            return 'Excellent'
        elif completeness >= 90:
            return 'Good'
        elif completeness >= 80:
            return 'Moderate'
        else:
            return 'Poor'


class BiometricAnalysis:
    """Analyze biometric enrollment patterns"""
    
    def __init__(self, df):
        self.df = df
        self.bio_age_cols = [col for col in df.columns if 'bioage' in col.lower()]
    
    def analyze_biometric_coverage(self) -> Dict[str, Any]:
        """Analyze biometric fingerprint age and coverage"""
        if not self.bio_age_cols:
            return {}
        
        try:
            coverage_stats = {}
            for col in self.bio_age_cols:
                coverage_stats[col] = {
                    'count': int(self.df[col].sum()),
                    'percentage': float(self.df[col].sum() / len(self.df) * 100)
                }
            
            return coverage_stats
        except Exception as e:
            return {}


class UpdateAnalysis:
    """Analyze update patterns across datasets"""
    
    def __init__(self, enrol_df, bio_df=None, demo_df=None):
        self.enrol_df = enrol_df
        self.bio_df = bio_df
        self.demo_df = demo_df
    
    def calculate_update_ratios(self) -> Dict[str, Any]:
        """Calculate update ratios between datasets"""
        try:
            enrol_count = len(self.enrol_df)
            
            bio_count = len(self.bio_df) if self.bio_df is not None else 0
            demo_count = len(self.demo_df) if self.demo_df is not None else 0
            
            return {
                'total_enrollments': enrol_count,
                'total_biometric_updates': bio_count,
                'total_demographic_updates': demo_count,
                'biometric_to_enrol_ratio': (bio_count / enrol_count) if enrol_count > 0 else 0,
                'demographic_to_enrol_ratio': (demo_count / enrol_count) if enrol_count > 0 else 0,
                'biometric_update_percentage': (bio_count / enrol_count * 100) if enrol_count > 0 else 0,
                'demographic_update_percentage': (demo_count / enrol_count * 100) if enrol_count > 0 else 0
            }
        except Exception as e:
            return {}


class TrendAnalysis:
    """Advanced trend analysis and forecasting insights"""
    
    def __init__(self, df):
        self.df = df
        self.date_col = self._find_date_column()
        self.enrol_col = self._find_enrollment_column()
    
    def _find_date_column(self):
        for col in self.df.columns:
            if 'date' in col.lower():
                return col
        return None
    
    def _find_enrollment_column(self):
        for col in self.df.columns:
            if 'total' in col.lower():
                return col
        return None
    
    def detect_trend_breakpoints(self) -> List[Dict[str, Any]]:
        """Detect significant trend changes"""
        if not self.date_col or not self.enrol_col:
            return []
        
        try:
            daily_data = self.df.groupby(self.date_col)[self.enrol_col].sum().reset_index()
            daily_data = daily_data.sort_values(self.date_col)
            daily_data['growth'] = daily_data[self.enrol_col].pct_change()
            
            # Find significant changes in growth rate
            mean_growth = daily_data['growth'].mean()
            std_growth = daily_data['growth'].std()
            
            breakpoints = []
            for idx, row in daily_data.iterrows():
                if abs(row['growth'] - mean_growth) > 2 * std_growth:
                    breakpoints.append({
                        'date': row[self.date_col],
                        'growth_rate': row['growth'],
                        'severity': 'high' if abs(row['growth'] - mean_growth) > 3 * std_growth else 'medium'
                    })
            
            return breakpoints
        except Exception as e:
            return []
    
    def get_volatility_metrics(self) -> Dict[str, Any]:
        """Calculate enrollment volatility"""
        if not self.date_col or not self.enrol_col:
            return {}
        
        try:
            daily_data = self.df.groupby(self.date_col)[self.enrol_col].sum().reset_index()
            daily_data = daily_data.sort_values(self.date_col)
            daily_data['growth'] = daily_data[self.enrol_col].pct_change()
            
            volatility = daily_data['growth'].std()
            mean_daily = daily_data[self.enrol_col].mean()
            cv = (daily_data[self.enrol_col].std() / mean_daily) if mean_daily > 0 else 0
            
            return {
                'volatility_std': volatility,
                'coefficient_of_variation': cv,
                'volatility_level': 'High' if cv > 0.5 else 'Medium' if cv > 0.2 else 'Low'
            }
        except Exception as e:
            return {}
