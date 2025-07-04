#!/usr/bin/env python3
"""
Startup script for the Approval Workflow Streamlit app
Handles dynamic port configuration for Cloud Run deployment
"""
import os
import subprocess
import sys

def main():
    # Get port from environment variable (Cloud Run sets this)
    port = os.getenv('PORT', '5000')
    
    # Ensure port is valid
    try:
        port_int = int(port)
        if port_int < 1 or port_int > 65535:
            raise ValueError("Port must be between 1 and 65535")
    except ValueError as e:
        print(f"Invalid port value: {port}. Using default port 5000.")
        port = '5000'
    
    # Build the streamlit command
    cmd = [
        'streamlit', 'run', 'app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false'
    ]
    
    print(f"Starting Streamlit app on port {port}")
    print(f"Command: {' '.join(cmd)}")
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)

if __name__ == '__main__':
    main()