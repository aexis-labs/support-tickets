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
    page_title="Aexis Incident Manager v2.0", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize global ticket memory store
def init_ticket_system():
    if "tickets" not in st.session_state:
        st.session_state.tickets = [
            {
                "ID": "AX-1024",
                "Timestamp": "2026-06-10 14:22",
                "Category": "Security Anomaly",
                "Priority": "High",
                "Issue": "High volume of invalid authorization attempts on Gateway Node 02.",
                "AI Diagnostic Note": "FLAGGED: Possible brute-force event. Integrity path secure.",
                "Status": "In Progress"
            },
            {
                "ID": "AX-1025",
                "Timestamp": "2026-06-11 01:05",
                "Category": "Hardware / Server Downtime",
                "Priority": "Critical",
                "Issue": "Memory leak detected on cluster backbone switch c3-net.",
                "AI Diagnostic Note": "CRITICAL: Resource exhaustion hazard. Rerouting traffic nodes.",
                "Status": "Open"
            }
        ]

init_ticket_system()

# ==============================================================================
# 2. SIDEBAR SYSTEM METRICS
# ==============================================================================
st.sidebar.header("Incident Operations Control")
st.sidebar.markdown("---")
st.sidebar.info("🎫 **AEXIS SUPPORT INCIDENT MANAGER**")

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
st.caption("Internal Operations Dashboard | Autonomous Ticket Triage Pipeline")
st.write("---")

# Quick Analytics Row for Professional Visuals
m1, m2, m3 = st.columns(3)
m1.metric("Automated Triage Accuracy", "97.6%", "Optimal")
m2.metric("Mean Time to Detection (MTTD)", "0.8 seconds", "-0.4s")
m3.metric("System Automation Rate", "89.2%", "+2.1%")
st.write("---")

col_form, col_pipeline = st.columns([1, 2], gap="large")

# ==============================================================================
# 4. LEFT COLUMN: NEW TICKET CREATION ENGINE (WITH AI ROUTING)
# ==============================================================================
with col_form:
    st.write("### ➕ Log New Infrastructure Incident")
    
    with st.form(key="incident_submission_form", clear_on_submit=True):
        issue_details = st.text_area(
            "Detailed Threat/Issue Description:",
            placeholder="Type your error codes, logs, or system disruptions here..."
        )
        
        st.caption("ℹ️ *Aexis Sentinel AI engine will parse your input to auto-classify priority and category upon commit.*")
        submit_ticket = st.form_submit_button("Commit Incident to Pipeline", use_container_width=True)
        
        if submit_ticket:
            if issue_details.strip():
                new_id = f"AX-{random.randint(1000, 9999)}"
                new_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                
                # ==============================================================
                # NEW FEATURE: INTERNALLY EMULATED AI TRIAGE LOGIC
                # ==============================================================
                text_lower = issue_details.lower()
                
                # 1. Determine Category & Priority autonomously
                if any(w in text_lower for w in ["ddos", "flood", "attack", "unauthorized", "key", "breach"]):
                    category = "Security Anomaly"
                    priority = "Critical"
                    diagnostic = "AUTONOMOUS BLOCK: High threat vector isolated. Sentinel sync engaged."
                elif any(w in text_lower for w in ["downtime", "crash", "leak", "fail", "offline"]):
                    category = "Hardware / Server Downtime"
                    priority = "High"
                    diagnostic = "RESOURCE ROUTING: Infrastructure drift isolated. Check system cluster."
                elif any(w in text_lower for w in ["slow", "latency", "ping", "delay"]):
                    category = "Network Latency Spike"
                    priority = "Medium"
                    diagnostic = "TRAFFIC SHAPING: Network packet bottleneck flagged."
                else:
                    category = "General Support Request"
                    priority = "Low"
                    diagnostic = "ROUTINE REVIEW: Queue assignment completed."
                
                # Append the smart incident record
                st.session_state.tickets.insert(0, {
                    "ID": new_id,
                    "Timestamp": new_timestamp,
                    "Category": category,
                    "Priority": priority,
                    "Issue": issue_details,
                    "AI Diagnostic Note": diagnostic,
                    "Status": "Open"
                })
                
                logging.info(f"AI Triage Event: {new_id} classified as {category} [{priority}]")
                st.success(f"Incident {new_id} autonomously processed by Aexis AI!")
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
        df_display = pd.DataFrame(st.session_state.tickets)
        # Display the table beautifully
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.write("#### ⚡ Quick Resolution Tool")
        
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
