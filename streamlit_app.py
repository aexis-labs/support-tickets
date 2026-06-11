import streamlit as st
import datetime
import random
import pandas as pd
import logging

# ==============================================================================
# 1. SYSTEM CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.set_page_config(
    page_title="Aexis Incident Manager", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize global ticket memory store
def init_ticket_system():
    if "tickets" not in st.session_state:
        # Starting baseline tickets for demonstration
        st.session_state.tickets = [
            {
                "ID": "AX-1024",
                "Timestamp": "2026-06-10 14:22",
                "Category": "Security Anomaly",
                "Issue": "High volume of invalid authorization attempts on Gateway Node 02.",
                "Status": "In Progress",
                "Priority": "High"
            },
            {
                "ID": "AX-1025",
                "Timestamp": "2026-06-11 01:05",
                "Category": "Hardware / Server Downtime",
                "Issue": "Memory leak detected on cluster backbone switch c3-net.",
                "Status": "Open",
                "Priority": "Critical"
            }
        ]

init_ticket_system()

# ==============================================================================
# 2. SIDEBAR SYSTEM METRICS
# ==============================================================================
st.sidebar.header("Incident Operations Control")
st.sidebar.markdown("---")
st.sidebar.info("🎫 **AEXIS SUPPORT INCIDENT MANAGER**")

# Calculate metrics live
total_tickets = len(st.session_state.tickets)
open_tickets = sum(1 for t in st.session_state.tickets if t["Status"] == "Open")
resolved_tickets = sum(1 for t in st.session_state.tickets if t["Status"] == "Resolved")

st.sidebar.metric(label="Total Logged Incidents", value=total_tickets)
st.sidebar.metric(label="Active Open Incidents", value=open_tickets, delta=f"{open_tickets} pending", delta_color="inverse")
st.sidebar.metric(label="Resolved Exceptions", value=resolved_tickets)

st.sidebar.markdown("---")
st.sidebar.caption(f"System Epoch: {datetime.datetime.now().year}")
st.sidebar.success("Incident sync pipeline: ONLINE")

# ==============================================================================
# 3. MAIN DASHBOARD HEADER
# ==============================================================================
st.title("🎫 Aexis Support Incident Manager")
st.caption("Internal Operations Dashboard | Infrastructure Ticket Pipeline")
st.write("---")

col_form, col_pipeline = st.columns([1, 2], gap="large")

# ==============================================================================
# 4. LEFT COLUMN: NEW TICKET CREATION ENGINE
# ==============================================================================
with col_form:
    st.write("### ➕ Log New Infrastructure Incident")
    
    with st.form(key="incident_submission_form", clear_on_submit=True):
        category = st.selectbox(
            "Select Incident Category:",
            ["Security Anomaly", "Hardware / Server Downtime", "Network Latency Spike", "General Support Request"]
        )
        
        priority = st.select_slider(
            "Select Operational Priority:",
            options=["Low", "Medium", "High", "Critical"]
        )
        
        issue_details = st.text_area(
            "Detailed Threat/Issue Description:",
            placeholder="Describe the anomalies, error codes, or infrastructure disruption..."
        )
        
        submit_ticket = st.form_submit_button("Commit Incident to Pipeline", use_container_width=True)
        
        if submit_ticket:
            if issue_details.strip():
                new_id = f"AX-{random.randint(1000, 9999)}"
                new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                
                # Append new incident record
                st.session_state.tickets.insert(0, {
                    "ID": new_id,
                    "Timestamp": new_timestamp,
                    "Category": category,
                    "Issue": issue_details,
                    "Status": "Open",
                    "Priority": priority
                })
                
                logging.info(f"New incident logged: {new_id} - {category} [{priority}]")
                st.success(f"Incident {new_id} recorded successfully!")
                st.rerun()
            else:
                st.error("Please supply valid issue descriptions before submitting.")

# ==============================================================================
# 5. RIGHT COLUMN: LIVE PIPELINE & INTERACTIVE MANAGEMENT
# ==============================================================================
with col_pipeline:
    st.write("### 📋 Active Incident Tracking Pipeline")
    
    if not st.session_state.tickets:
        st.info("No current infrastructure incidents logged in system memory.")
    else:
        # Convert to Pandas Dataframe for high-speed scannable rendering
        df_display = pd.DataFrame(st.session_state.tickets)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.write("#### ⚡ Quick Resolution Tool")
        
        # Interactive ticket status management selector
        ticket_ids = [t["ID"] for t in st.session_state.tickets]
        selected_id = st.selectbox("Select Ticket ID to Update:", ticket_ids)
        new_status = st.radio("Modify Operational Status:", ["Open", "In Progress", "Resolved"], horizontal=True)
        
        if st.button("Update System Records", use_container_width=True):
            for ticket in st.session_state.tickets:
                if ticket["ID"] == selected_id:
                    ticket["Status"] = new_status
                    logging.info(f"Ticket {selected_id} status updated to {new_status}")
                    st.toast(f"Ticket {selected_id} marked as {new_status}!", icon="🔄")
                    st.rerun()
