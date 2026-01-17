"""
Enhanced UIDAI Aadhaar Analysis Dashboard
Complete analytics platform with various analysis types, comprehensive visualizations,
and non-technical insights suitable for executives and stakeholders
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from analysis import (
    AdvancedTemporalAnalysis, GeographicAnalysis, DemographicAnalysis,
    DataQualityAnalysis, BiometricAnalysis, UpdateAnalysis, TrendAnalysis
)
from insightGenerator import InsightGenerator
from styling import apply_custom_theme, display_insight_card, create_divider

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title='UIDAI Aadhaar Analysis',
    page_icon='',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'https://data.gov.in',
        'Report a bug': None,
        'About': 'UIDAI Hackathon 2026 - Analytics Dashboard'
    }
)

apply_custom_theme()

# ============================================================================
# STYLING
# ============================================================================

_ = st.markdown("""
<style>
.main { padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.metric-card { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
h1 { color: #1f2937; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }
h2 { color: #374151; font-size: 1.8rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; border-bottom: 3px solid #667eea; padding-bottom: 0.5rem; }
.divider { height: 2px; background: linear-gradient(90deg, #667eea, #764ba2); margin: 2rem 0; }
.sidebar-content { background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_combined_data():
    """Load and combine all CSV files from data directory"""
    data_dir = Path('../data')
    
    if not data_dir.exists():
        _ = st.error('Data directory not found! Create ../data folder and add CSV files.')
        return None
    
    # Find all enrolment files
    enrolment_files = sorted(glob.glob(str(data_dir / '*enrolment*.csv')))
    
    if not enrolment_files:
        _ = st.error('No enrolment CSV files found in ../data directory!')
        return None
    
    # Load and combine enrolment data
    enrolment_dfs = []
    for file in enrolment_files:
        try:
            df = pd.read_csv(file)
            enrolment_dfs.append(df)
        except Exception as e:
            _ = st.warning(f'Could not load {Path(file).name}: {e}')
    
    if not enrolment_dfs:
        _ = st.error('Could not load any CSV files!')
        return None
    
    # Combine all enrolment data
    combined_df = pd.concat(enrolment_dfs, ignore_index=True)
    
    # Process date column
    if 'date' in combined_df.columns:
        combined_df['date'] = pd.to_datetime(combined_df['date'], format='%d-%m-%Y', errors='coerce')
    
    # Calculate total if age columns exist
    age_cols = [col for col in combined_df.columns if 'age' in col.lower()]
    if age_cols:
        combined_df['total'] = combined_df[age_cols].sum(axis=1)
    
    return combined_df

@st.cache_data
def load_biometric_data():
    """Load biometric data if available"""
    data_dir = Path('../data')
    biometric_files = sorted(glob.glob(str(data_dir / '*biometric*.csv')))
    
    if not biometric_files:
        return None
    
    bio_dfs = []
    for file in biometric_files:
        try:
            df = pd.read_csv(file)
            bio_dfs.append(df)
        except:
            pass
    
    if bio_dfs:
        combined = pd.concat(bio_dfs, ignore_index=True)
        if 'date' in combined.columns:
            combined['date'] = pd.to_datetime(combined['date'], format='%d-%m-%Y', errors='coerce')
        return combined
    
    return None

@st.cache_data
def load_demographic_data():
    """Load demographic data if available"""
    data_dir = Path('../data')
    demographic_files = sorted(glob.glob(str(data_dir / '*demographic*.csv')))
    
    if not demographic_files:
        return None
    
    demo_dfs = []
    for file in demographic_files:
        try:
            df = pd.read_csv(file)
            demo_dfs.append(df)
        except:
            pass
    
    if demo_dfs:
        combined = pd.concat(demo_dfs, ignore_index=True)
        if 'date' in combined.columns:
            combined['date'] = pd.to_datetime(combined['date'], format='%d-%m-%Y', errors='coerce')
        return combined
    
    return None

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def main():
    # Load data
    df = load_combined_data()
    bio_df = load_biometric_data()
    demo_df = load_demographic_data()
    
    if df is None:
        st.stop()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title('UIDAI Aadhaar Analysis')
        _ = st.markdown('*Interactive Dashboard for UIDAI Hackathon 2026 - Enhanced Analytics Platform*')
    
    with col2:
        st.metric('Dataset Status', 'Loaded', delta='All files combined')
    
    _ = st.markdown(create_divider(), unsafe_allow_html=True)
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    
    with st.sidebar:
        _ = st.header(' Filters & Settings')
        
        # State filter
        if 'state' in df.columns:
            available_states = sorted(df['state'].unique())
            selected_states = st.multiselect(
                'Select States',
                available_states,
                default=available_states[:5],
                help='Choose states to analyze'
            )
        else:
            selected_states = None
        
        # Date range filter
        if 'date' in df.columns:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input('Start Date', df['date'].min(), help='Analysis start date')
            with col2:
                end_date = st.date_input('End Date', df['date'].max(), help='Analysis end date')
        else:
            start_date, end_date = None, None
        
        _ = st.markdown('---')
        
        # Display options
        show_age = st.checkbox('Show Age Distribution', value=True)
        show_anomalies = st.checkbox('Show Anomaly Detection', value=True)
        show_detailed = st.checkbox('Show Detailed Data', value=False)
        
        _ = st.markdown('---')
        _ = st.subheader('Advanced Analysis')
        show_deep_analysis = st.checkbox('Enable Deep Analysis', value=True)
    
    # ========================================================================
    # DATA FILTERING
    # ========================================================================
    
    if 'state' in df.columns and selected_states:
        filtered_df = df[df['state'].isin(selected_states)].copy()
    else:
        filtered_df = df.copy()
    
    if start_date and end_date and 'date' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['date'] >= pd.Timestamp(start_date)) &
            (filtered_df['date'] <= pd.Timestamp(end_date))
        ]
    
    # ========================================================================
    # KEY METRICS DISPLAY
    # ========================================================================
    
    _ = st.subheader('Key Metrics Overview')
    
    total_records = len(filtered_df)
    unique_states = filtered_df['state'].nunique() if 'state' in filtered_df.columns else 0
    unique_districts = filtered_df['district'].nunique() if 'district' in filtered_df.columns else 0
    
    if 'total' in filtered_df.columns:
        total_enrollments = int(filtered_df['total'].sum())
    else:
        total_enrollments = total_records
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            'Total Enrollments',
            f'{total_enrollments:,}',
            delta=f'{total_enrollments/1e6:.2f}M' if total_enrollments > 0 else None,
            help='Total Aadhaar enrollments'
        )
    
    with col2:
        st.metric(
            'States/UTs',
            unique_states,
            help='States covered'
        )
    
    with col3:
        st.metric(
            'Districts',
            unique_districts,
            help='Districts covered'
        )
    
    with col4:
        if 'date' in filtered_df.columns and 'total' in filtered_df.columns:
            daily_avg = int(filtered_df.groupby('date')['total'].sum().mean())
        else:
            daily_avg = int(total_enrollments / max(len(filtered_df), 1))
        
        st.metric(
            'Avg Daily',
            f'{daily_avg:,}',
            help='Average daily enrollments'
        )
    
    _ = st.markdown(create_divider(), unsafe_allow_html=True)
    
    # ========================================================================
    # TEMPORAL ANALYSIS
    # ========================================================================
    
    _ = st.subheader('Temporal Trends & Growth Patterns')
    
    if 'date' in filtered_df.columns and 'total' in filtered_df.columns:
        col1, col2 = st.columns(2)
        
        # Daily trend
        with col1:
            daily_trend = filtered_df.groupby('date')['total'].sum().reset_index()
            daily_trend.columns = ['Date', 'Enrollments']
            
            fig_daily = px.line(
                daily_trend, x='Date', y='Enrollments',
                title='Daily Enrollment Trend',
                markers=True,
                template='plotly_white',
                height=400
            )
            fig_daily.update_traces(line=dict(color='#FD6F01', width=2))
            fig_daily.update_layout(hovermode='x unified')
            st.plotly_chart(fig_daily, use_container_width=True)
        
        # Monthly trend
        with col2:
            filtered_df['year_month'] = filtered_df['date'].dt.to_period('M')
            monthly_trend = filtered_df.groupby('year_month')['total'].sum().reset_index()
            monthly_trend['year_month'] = monthly_trend['year_month'].astype(str)
            monthly_trend.columns = ['Month', 'Enrollments']
            
            fig_monthly = px.bar(
                monthly_trend, x='Month', y='Enrollments',
                title='Monthly Volume',
                template='plotly_white',
                height=400,
                color='Enrollments',
                color_continuous_scale=['#ABE098', '#2EB62C']
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
    
    _ = st.markdown(create_divider(), unsafe_allow_html=True)
    
    # ========================================================================
    # GEOGRAPHIC ANALYSIS
    # ========================================================================
    
    _ = st.subheader('Geographic Distribution')
    
    if 'state' in filtered_df.columns and 'total' in filtered_df.columns:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            top_n = st.slider('Show Top N States', 5, 20, 15, key='top_states')
            
            state_data = filtered_df.groupby('state')['total'].sum().nlargest(top_n).reset_index()
            
            fig_states = px.bar(
                state_data.sort_values('total'),
                x='total', y='state',
                title=f'Top {top_n} States by Enrollment',
                template='plotly_white',
                height=400,
                color='total',
                color_continuous_scale='Viridis'
            )
            fig_states.update_xaxes(title_text='Enrollments')
            fig_states.update_yaxes(title_text='State')
            st.plotly_chart(fig_states, use_container_width=True)
        
        with col2:
            if len(state_data) > 0:
                st.metric(
                    'Top State',
                    state_data.iloc[0]['state'],
                    help='Leading state'
                )
                
                st.metric(
                    'Top Value',
                    f'{int(state_data.iloc[0]["total"]):,}',
                    help='Top state enrollments'
                )
                
                if len(state_data) > 1:
                    growth = ((state_data.iloc[0]['total'] - state_data.iloc[1]['total']) /
                             state_data.iloc[1]['total'] * 100)
                    st.metric(
                        'vs 2nd',
                        f'{growth:.1f}%',
                        delta='higher',
                        help='Difference with second state'
                    )
    
    _ = st.markdown(create_divider(), unsafe_allow_html=True)
    
    # ========================================================================
    # DEMOGRAPHIC ANALYSIS
    # ========================================================================
    
    if show_age:
        _ = st.subheader('Age Group Distribution')
        
        age_cols = [col for col in filtered_df.columns if 'age' in col.lower()]
        
        if age_cols:
            col1, col2 = st.columns([1.2, 1])
            
            # LEFT: Pie Chart
            with col1:
                age_totals = {col: int(filtered_df[col].sum()) for col in age_cols}
                total_age = sum(age_totals.values())
                
                # Create 3D pie chart with border
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(age_totals.keys()),
                    values=list(age_totals.values()),
                    marker=dict(
                        colors=['#FD6F01', '#DDDDDD', '#28a745'],
                        line=dict(
                            color='#1f2937',  # Border color (dark gray)
                            width=1           # Border width
                        )
                    ),
                    textfont=dict(
                        size=12,
                        family="Arial Black, sans-serif"
                    ),
                    textposition='inside',
                    textinfo='label+percent',
                    hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>',
                    
                )])

                fig_pie.update_layout(
                    title='Age Distribution',
                    template='plotly_white',
                    height=500,
                    showlegend=True,
                    font=dict(size=12, family="Arial Black")
                )

                st.plotly_chart(fig_pie, use_container_width=True)
            
            # RIGHT: Data Table (Clean, Centered, Bold)
            with col2:
                # Title
                _ = st.markdown(
                    "<h3 style='text-align: center; font-weight: bold; color: #1f2937;'>Age Statistics</h3>", 
                    unsafe_allow_html=True
                )
                
                # Header Row
                hdr1, hdr2, hdr3 = st.columns(3)
                with hdr1:
                    _ = st.markdown(
                        "<p style='text-align: center; font-weight: bold; color: #374151;'>Age Group</p>", 
                        unsafe_allow_html=True
                    )
                with hdr2:
                    _ = st.markdown(
                        "<p style='text-align: center; font-weight: bold; color: #374151;'>Count</p>", 
                        unsafe_allow_html=True
                    )
                with hdr3:
                    _ = st.markdown(
                        "<p style='text-align: center; font-weight: bold; color: #374151;'>Percentage</p>", 
                        unsafe_allow_html=True
                    )
                
                _ = st.divider()
                
                # Data Rows
                for group, value in age_totals.items():
                    pct = (value / total_age * 100) if total_age > 0 else 0
                    
                    # Convert label: age_0_5 → 0 5
                    short_label = group.replace('age_', '').replace('_', '-').title()
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    # Age Group (Centered + Bold)
                    with col_a:
                        _ = st.markdown(
                            f"<p style='text-align: center; font-weight: bold; color: #FD6F01;'>{short_label}</p>", 
                            unsafe_allow_html=True
                        )
                    
                    # Count (Centered + Bold + Formatted)
                    with col_b:
                        _ = st.markdown(
                            f"<p style='text-align: center; font-weight: bold; color: #191970;'>{value:,}</p>", 
                            unsafe_allow_html=True
                        )
                    
                    # Percentage (Centered + Bold + Color + 2 Decimals)
                    with col_c:
                        _ = st.markdown(
                            f"<p style='text-align: center; font-weight: bold; color: #28a745;'>{pct:.2f}%</p>", 
                            unsafe_allow_html=True
                        )

    _ = st.markdown(create_divider(), unsafe_allow_html=True)

    
    # ========================================================================
    # ANOMALY DETECTION
    # ========================================================================
    
    if show_anomalies:
        _ = st.subheader('Anomaly Detection & Data Quality')
        
        col1, col2 = st.columns(2)
        
        with col1:
            _ = st.write('**Zero Enrollment Districts**')
            
            # Find districts with issues
            if 'district' in filtered_df.columns and 'total' in filtered_df.columns:
                problem_districts = filtered_df[filtered_df['total'] == 0]
                
                if len(problem_districts) > 0:
                    _ = st.warning(f'⚠️ Found {len(problem_districts)} records with zero enrollments')
                    
                    with st.expander(f'View all {len(problem_districts)} records'):
                        st.dataframe(problem_districts, use_container_width=True, hide_index=True)
                else:
                    _ = st.success('No zero enrollment issues detected')
        
        with col2:
            _ = st.write('**Peak Activity Days**')
            
            if 'date' in filtered_df.columns and 'total' in filtered_df.columns:
                peak_days = filtered_df.groupby('date')['total'].sum().nlargest(10).reset_index()
                peak_days.columns = ['Date', 'Enrollments']
                peak_days['Date'] = peak_days['Date'].dt.strftime('%Y-%m-%d')
                st.dataframe(peak_days, use_container_width=True, hide_index=True)
    
    _ = st.markdown(create_divider(), unsafe_allow_html=True)
    
    # ========================================================================
    # DETAILED DATA TABLE
    # ========================================================================
    
    if show_detailed:
        _ = st.subheader('Detailed Data Table')
        
        col1, col2 = st.columns(2)
        
        with col1:
            sort_col = st.selectbox(
                'Sort by',
                ['date', 'state', 'total'],
                index=0
            )
        
        with col2:
            sort_order = st.radio('Order', ['Descending', 'Ascending'], index=0)
        
        display_df = filtered_df.sort_values(sort_col, ascending=(sort_order == 'Ascending'))
        
        # Select columns to display
        available_cols = [col for col in display_df.columns if col != 'year_month']
        display_cols = st.multiselect(
            'Select columns to display',
            available_cols,
            default=available_cols[:8]
        )
        
        st.dataframe(display_df[display_cols], use_container_width=True, height=500)
        
        # Download button
        csv = display_df[display_cols].to_csv(index=False)
        st.download_button(
            label='Download Data as CSV',
            data=csv,
            file_name=f'aadhaar_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )
    
    _ = st.markdown(create_divider(), unsafe_allow_html=True)
    
    # ========================================================================
    # DEEP ANALYSIS
    # ========================================================================
    
    if show_deep_analysis:
        _ = st.subheader('Deep Analysis Results')
        
        with st.spinner('Running comprehensive analysis...'):
            try:
                # Run all analyses
                temporal_analyzer = AdvancedTemporalAnalysis(filtered_df)
                geo_analyzer = GeographicAnalysis(filtered_df)
                demo_analyzer = DemographicAnalysis(filtered_df)
                quality_analyzer = DataQualityAnalysis(filtered_df)
                bio_analyzer = BiometricAnalysis(bio_df if bio_df is not None else filtered_df)
                update_analyzer = UpdateAnalysis(filtered_df, bio_df, demo_df)
                trend_analyzer = TrendAnalysis(filtered_df)
                
                # Compile results
                analysis_results = {
                    'temporal_metrics': temporal_analyzer.calculate_growth_rate(),
                    'geographic_metrics': geo_analyzer.calculate_concentration(),
                    'demographic_metrics': demo_analyzer.analyze_age_distribution(),
                    'quality_metrics': {
                        'overall_completeness': quality_analyzer.calculate_completeness().get('overall_completeness', 0),
                        'issues': quality_analyzer.identify_data_quality_issues()
                    },
                    'biometric_metrics': bio_analyzer.analyze_biometric_coverage(),
                    'update_metrics': update_analyzer.calculate_update_ratios(),
                    'trend_metrics': trend_analyzer.get_volatility_metrics()
                }
                
                # Generate insights
                insight_gen = InsightGenerator(analysis_results)
                insights = insight_gen.get_all_insights()
                
                # Display summary
                summary_text = insight_gen.get_summary_text()
                if summary_text is not None:
                    _ = st.markdown(summary_text, unsafe_allow_html=True)
                
                _ = st.markdown('---')
                
                # Display insights in columns - FIXED VERSION
                cols = st.columns(2)
                for idx, insight in enumerate(insights):
                    with cols[idx % 2]:
                        # Create insight card with title 
                        full_title = f"{insight.get('title', 'Insight')}"
                        display_insight_card(
                            title=full_title,
                            message=insight.get('message', ''),
                            action=insight.get('action', ''),
                            severity=insight.get('severity', 'info')
                        )
                
                _ = st.markdown('---')
                
                # Top Recommendations
                _ = st.subheader('Top Recommendations')
                recommendations = insight_gen.get_key_recommendations()
                for idx, rec in enumerate(recommendations, 1):
                    _ = st.markdown(f'{idx}. {rec}')
                

                
            except Exception as e:
                _ = st.error(f'Error during analysis: {str(e)}')
                _ = st.info('Make sure you have all required columns in your data (date, state, total, age_* columns)')

if __name__ == '__main__':
    main()