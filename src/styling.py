"""
Styling Module for UIDAI Aadhaar Dashboard
"""

import streamlit as st


def apply_custom_theme():
    """Apply Indian-themed custom styling"""
    st.markdown("""
    <style>
    /* Indian Color Theme */
    :root {
        --saffron: #FF9933;
        --white: #FFFFFF;
        --green: #138808;
        --navy: #001F3F;
        --cream: #F5F5F5;
        --gray: #666666;
    }
    
    /* Main Background */
    [data-testid="stAppViewContainer"] {
        background-color: #FAFAFA;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F8F8F8;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #F8F8F8;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #138808;
        font-weight: 600;
    }
    
    h1 {
        color: #138808;
        border-bottom: 3px solid #FF9933;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #138808;
        margin-top: 20px;
        padding-top: 10px;
        border-left: 4px solid #FF9933;
        padding-left: 10px;
    }
    
    h3 {
        color: #001F3F;
        margin-top: 15px;
    }
    
    /* Metric Cards */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        border-left: 4px solid #FF9933;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="metric-container"] > div:first-child {
        color: #666666;
        font-size: 12px;
        font-weight: 500;
    }
    
    [data-testid="metric-container"] > div:nth-child(2) {
        color: #138808;
        font-size: 24px;
        font-weight: 700;
    }
    
    /* Alert Boxes */
    .stAlert > div {
        padding: 1rem 1.25rem;
        border-radius: 6px;
    }
    
    /* Success Alert */
    [data-testid="stNotification"] > div:has-text('success') {
        background-color: #F0FFF4;
        border-left: 4px solid #138808;
        color: #138808;
    }
    
    /* Warning Alert */
    [data-testid="stNotification"] > div:has-text('warning') {
        background-color: #FFFBF0;
        border-left: 4px solid #FF9933;
        color: #FF9933;
    }
    
    /* Info Alert */
    [data-testid="stNotification"] > div:has-text('info') {
        background-color: #F0F4FF;
        border-left: 4px solid #001F3F;
        color: #001F3F;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #138808;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        padding: 8px 16px;
    }
    
    .stButton > button:hover {
        background-color: #0F6604;
        border: none;
    }
    
    .stButton > button:active {
        background-color: #0A4403;
        border: none;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        border: 1px solid #DDD;
        border-radius: 6px;
        padding: 8px 12px;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #FF9933;
        box-shadow: 0 0 0 0.2rem rgba(255, 153, 51, 0.25);
    }
    
    /* Select Box */
    .stSelectbox > div > div > select {
        border: 1px solid #DDD;
        border-radius: 6px;
        padding: 8px 12px;
    }
    
    /* Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #DDD;
        border-radius: 6px;
        overflow: hidden;
    }
    
    [data-testid="stDataFrame"] table {
        font-size: 13px;
    }
    
    [data-testid="stDataFrame"] thead {
        background-color: #F5F5F5;
        border-bottom: 2px solid #FF9933;
    }
    
    [data-testid="stDataFrame"] thead th {
        color: #138808;
        font-weight: 600;
        padding: 12px;
    }
    
    [data-testid="stDataFrame"] tbody td {
        padding: 10px 12px;
        border-bottom: 1px solid #F0F0F0;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background-color: #FAFAFA;
    }
    
    /* Divider */
    hr {
        border: 1px solid #FF9933;
        margin: 30px 0;
    }
    
    /* Link Styling */
    a {
        color: #138808;
        text-decoration: none;
    }
    
    a:hover {
        color: #FF9933;
        text-decoration: underline;
    }
    
    /* Plotly Chart Background */
    .plotly-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E5E5E5;
    }
    
    /* Code Block */
    code {
        background-color: #F5F5F5;
        color: #001F3F;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    
    pre {
        background-color: #F5F5F5;
        border-left: 4px solid #FF9933;
        padding: 12px;
        border-radius: 6px;
        overflow-x: auto;
    }
    
    /* Markdown Text */
    p {
        color: #333333;
        line-height: 1.6;
    }
    
    /* Custom Classes */
    .metric-good {
        color: #138808;
        font-weight: 600;
    }
    
    .metric-warning {
        color: #FF9933;
        font-weight: 600;
    }
    
    .metric-critical {
        color: #D32F2F;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)


def display_insight_card(title, message, action, severity='info'):
    """Display a custom insight card with styling"""
    
    # Color mapping
    colors = {
        'success': {'bg': '#E8F5E9', 'border': '#4CAF50', 'text': '#1B5E20'},
        'warning': {'bg': '#FFF8E1', 'border': '#FF9933', 'text': '#F57F17'},
        'error': {'bg': '#FFEBEE', 'border': '#D32F2F', 'text': '#B71C1C'},
        'info': {'bg': '#E3F2FD', 'border': '#001F3F', 'text': '#001F3F'}
    }
    
    color = colors.get(severity, colors['info'])
    
    st.markdown(f"""
    <div style='
        background-color: {color["bg"]};
        border-left: 4px solid {color["border"]};
        border-radius: 6px;
        padding: 16px;
        margin: 16px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    '>
        <div style='color: {color["text"]}; font-weight: 600; font-size: 16px; margin-bottom: 8px;'>
            {title}
        </div>
        <div style='color: #333333; font-size: 14px; margin-bottom: 12px; line-height: 1.5;'>
            {message}
        </div>
        <div style='color: {color["text"]}; font-size: 13px; font-weight: 500;'>
            Action: {action}
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_divider(text=None, color='#FF9933', thickness=2, style='solid'):
    """Create a custom divider line"""
    
    if text:
        st.markdown(f"""
        <div style='
            display: flex;
            align-items: center;
            margin: 20px 0;
        '>
            <div style='
                flex-grow: 1;
                border-top: {thickness}px {style} {color};
            '></div>
            <div style='
                padding: 0 10px;
                color: #666666;
                font-weight: 500;
                font-size: 14px;
            '>
                {text}
            </div>
            <div style='
                flex-grow: 1;
                border-top: {thickness}px {style} {color};
            '></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='
            border-top: {thickness}px {style} {color};
            margin: 20px 0;
        '></div>
        """, unsafe_allow_html=True)


def display_stat_box(title, value, subtitle=None, color='#138808'):
    """Display a statistics box"""
    
    st.markdown(f"""
    <div style='
        background-color: #FFFFFF;
        border-radius: 8px;
        border-left: 4px solid {color};
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 10px 0;
    '>
        <div style='
            color: #666666;
            font-size: 12px;
            font-weight: 500;
            margin-bottom: 8px;
            text-transform: uppercase;
        '>
            {title}
        </div>
        <div style='
            color: {color};
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 4px;
        '>
            {value}
        </div>
        {f'<div style="color: #999999; font-size: 12px;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def display_progress_bar(label, value, max_value=100, color='#138808'):
    """Display a custom progress bar"""
    
    percentage = min((value / max_value) * 100, 100) if max_value > 0 else 0
    
    st.markdown(f"""
    <div style='margin: 16px 0;'>
        <div style='
            color: #333333;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
        '>
            <span>{label}</span>
            <span style='color: {color}; font-weight: 600;'>{percentage:.1f}%</span>
        </div>
        <div style='
            width: 100%;
            height: 8px;
            background-color: #E5E5E5;
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        '>
            <div style='
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, {color}, {color});
                transition: width 0.3s ease;
            '></div>
        </div>
    </div>
    """, unsafe_allow_html=True)