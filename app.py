import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# Initialize session state for storing submissions
if 'submissions' not in st.session_state:
    st.session_state.submissions = []

def add_submission(name, description, purpose):
    """Add a new submission to the session state"""
    submission = {
        'id': str(uuid.uuid4()),
        'name': name,
        'description': description,
        'purpose': purpose,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'data_approval': 'Pending',
        'security_approval': 'Pending',
        'legal_approval': 'Pending',
        'overall_status': 'Pending'
    }
    st.session_state.submissions.append(submission)
    return submission['id']

def update_approval(submission_id, team, status):
    """Update approval status for a specific team"""
    for submission in st.session_state.submissions:
        if submission['id'] == submission_id:
            if team == 'Data':
                submission['data_approval'] = status
            elif team == 'Security':
                submission['security_approval'] = status
            elif team == 'Legal':
                submission['legal_approval'] = status
            
            # Update overall status
            submission['overall_status'] = calculate_overall_status(submission)
            break

def calculate_overall_status(submission):
    """Calculate overall status based on team approvals"""
    approvals = [
        submission['data_approval'],
        submission['security_approval'],
        submission['legal_approval']
    ]
    
    if 'Rejected' in approvals:
        return 'Rejected'
    elif all(approval == 'Approved' for approval in approvals):
        return 'Fully Approved'
    else:
        return 'Pending'

def get_status_color(status):
    """Get color for status display"""
    if status == 'Approved' or status == 'Fully Approved':
        return 'green'
    elif status == 'Rejected':
        return 'red'
    else:
        return 'orange'

# Main app
st.set_page_config(
    page_title="Approval Workflow System",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Approval Workflow System")
st.markdown("---")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["📝 Submit Request", "📊 Dashboard", "✅ Approve Requests"])

# Tab 1: Form Submission
with tab1:
    st.header("Submit New Request")
    st.markdown("Fill out the form below to submit a new request for approval.")
    
    with st.form("submission_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Request Name*",
                placeholder="Enter a descriptive name for your request",
                help="A brief, descriptive name for your request"
            )
            
        with col2:
            purpose = st.selectbox(
                "Purpose*",
                ["Data Access", "System Integration", "Process Change", "Security Update", "Legal Review", "Other"],
                help="Select the primary purpose of this request"
            )
        
        description = st.text_area(
            "Description*",
            placeholder="Provide detailed information about your request...",
            height=150,
            help="Detailed description of what you're requesting and why"
        )
        
        submitted = st.form_submit_button("Submit Request", type="primary")
        
        if submitted:
            if name and description and purpose:
                submission_id = add_submission(name, description, purpose)
                st.success(f"✅ Request submitted successfully! ID: {submission_id[:8]}")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields marked with *")

# Tab 2: Dashboard
with tab2:
    st.header("Submissions Dashboard")
    
    if not st.session_state.submissions:
        st.info("📭 No submissions yet. Use the 'Submit Request' tab to create your first submission.")
    else:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_submissions = len(st.session_state.submissions)
        pending_submissions = sum(1 for s in st.session_state.submissions if s['overall_status'] == 'Pending')
        approved_submissions = sum(1 for s in st.session_state.submissions if s['overall_status'] == 'Fully Approved')
        rejected_submissions = sum(1 for s in st.session_state.submissions if s['overall_status'] == 'Rejected')
        
        with col1:
            st.metric("Total Submissions", total_submissions)
        with col2:
            st.metric("Pending", pending_submissions)
        with col3:
            st.metric("Approved", approved_submissions)
        with col4:
            st.metric("Rejected", rejected_submissions)
        
        st.markdown("---")
        
        # Submissions table
        st.subheader("All Submissions")
        
        for submission in reversed(st.session_state.submissions):  # Show newest first
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"**{submission['name']}**")
                    st.markdown(f"*{submission['purpose']}*")
                    st.markdown(f"📅 {submission['timestamp']}")
                
                with col2:
                    st.markdown("**Team Approvals:**")
                    
                    # Data team status
                    data_color = get_status_color(submission['data_approval'])
                    st.markdown(f"Data: :{data_color}[{submission['data_approval']}]")
                    
                    # Security team status
                    security_color = get_status_color(submission['security_approval'])
                    st.markdown(f"Security: :{security_color}[{submission['security_approval']}]")
                    
                    # Legal team status
                    legal_color = get_status_color(submission['legal_approval'])
                    st.markdown(f"Legal: :{legal_color}[{submission['legal_approval']}]")
                
                with col3:
                    overall_color = get_status_color(submission['overall_status'])
                    st.markdown("**Overall Status:**")
                    st.markdown(f":{overall_color}[{submission['overall_status']}]")
                
                # Expandable details
                with st.expander("View Details"):
                    st.markdown(f"**ID:** {submission['id']}")
                    st.markdown(f"**Description:** {submission['description']}")
                
                st.markdown("---")

# Tab 3: Approval Interface
with tab3:
    st.header("Approval Interface")
    
    if not st.session_state.submissions:
        st.info("📭 No submissions to approve yet.")
    else:
        # Team selector
        selected_team = st.selectbox(
            "Select Your Team",
            ["Data", "Security", "Legal"],
            help="Choose your team to view and approve relevant submissions"
        )
        
        st.markdown(f"### {selected_team} Team Approvals")
        
        # Filter submissions that need approval from this team
        pending_for_team = [
            s for s in st.session_state.submissions 
            if s[f'{selected_team.lower()}_approval'] == 'Pending'
        ]
        
        if not pending_for_team:
            st.success(f"✅ No pending approvals for {selected_team} team!")
        else:
            st.info(f"📋 {len(pending_for_team)} submission(s) pending {selected_team} team approval")
            
            for submission in pending_for_team:
                with st.container():
                    st.markdown(f"**{submission['name']}**")
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Purpose:** {submission['purpose']}")
                        st.markdown(f"**Description:** {submission['description']}")
                        st.markdown(f"**Submitted:** {submission['timestamp']}")
                        
                        # Show other team statuses
                        st.markdown("**Other Team Status:**")
                        if selected_team != 'Data':
                            data_color = get_status_color(submission['data_approval'])
                            st.markdown(f"Data: :{data_color}[{submission['data_approval']}]")
                        if selected_team != 'Security':
                            security_color = get_status_color(submission['security_approval'])
                            st.markdown(f"Security: :{security_color}[{submission['security_approval']}]")
                        if selected_team != 'Legal':
                            legal_color = get_status_color(submission['legal_approval'])
                            st.markdown(f"Legal: :{legal_color}[{submission['legal_approval']}]")
                    
                    with col2:
                        st.markdown("**Take Action:**")
                        
                        col_approve, col_reject = st.columns(2)
                        
                        with col_approve:
                            if st.button(
                                "✅ Approve", 
                                key=f"approve_{submission['id']}_{selected_team}",
                                type="primary"
                            ):
                                update_approval(submission['id'], selected_team, 'Approved')
                                st.success(f"Approved by {selected_team} team!")
                                st.rerun()
                        
                        with col_reject:
                            if st.button(
                                "❌ Reject", 
                                key=f"reject_{submission['id']}_{selected_team}"
                            ):
                                update_approval(submission['id'], selected_team, 'Rejected')
                                st.error(f"Rejected by {selected_team} team!")
                                st.rerun()
                    
                    st.markdown("---")

# Sidebar with additional information
with st.sidebar:
    st.header("ℹ️ System Information")
    st.markdown("""
    **Approval Workflow:**
    1. Submit request with required details
    2. Three teams review: Data, Security, Legal
    3. All teams must approve for full approval
    4. Any rejection stops the process
    """)
    
    st.markdown("---")
    st.markdown(f"**Total Submissions:** {len(st.session_state.submissions)}")
    
    if st.session_state.submissions:
        approved_count = sum(1 for s in st.session_state.submissions if s['overall_status'] == 'Fully Approved')
        approval_rate = (approved_count / len(st.session_state.submissions)) * 100
        st.markdown(f"**Approval Rate:** {approval_rate:.1f}%")
    
    st.markdown("---")
    
    # Clear all data button (for testing purposes)
    if st.button("🗑️ Clear All Data", type="secondary"):
        if st.session_state.submissions:
            st.session_state.submissions = []
            st.success("All data cleared!")
            st.rerun()
        else:
            st.info("No data to clear!")
