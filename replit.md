# IT Request Approval System

## Overview

This is a Streamlit-based web application for managing IT request approvals. The system allows users to submit IT requests and tracks approval status across multiple teams (Data, Security, and Legal). The application uses session-based storage for simplicity and real-time updates.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit (Python web framework)
- **Architecture Pattern**: Single-page application with session state management
- **UI Components**: Native Streamlit widgets for forms, tables, and status displays
- **State Management**: Streamlit session state for in-memory data persistence

### Backend Architecture
- **Runtime**: Python-based server-side application
- **Database**: PostgreSQL with SQLAlchemy ORM for data persistence
- **Data Processing**: Pandas for data manipulation and display
- **Business Logic**: Functional programming approach with utility functions
- **Session Management**: Database-backed storage with SQLAlchemy models

## Key Components

### Core Functions
1. **add_submission()**: Creates new IT requests with unique IDs and timestamps
2. **update_approval()**: Manages approval status updates from different teams
3. **calculate_overall_status()**: Determines final approval status based on team decisions

### Data Model
- **Submission Entity**: SQLAlchemy model with ID, name, description, purpose, timestamp, and approval statuses
- **Database Schema**: PostgreSQL table with columns for each approval team status
- **Approval Teams**: Data, Security, and Legal teams with independent approval workflows
- **Status Values**: Pending, Approved, Rejected for granular tracking

### User Interface
- Form-based submission interface
- Real-time status dashboard
- Team-specific approval interfaces
- Historical submission tracking

## Data Flow

1. **Request Submission**: Users input request details through Streamlit forms
2. **ID Generation**: System assigns unique UUID to each submission
3. **Initial State**: All approvals set to "Pending" status
4. **Team Review**: Each team can independently update their approval status
5. **Status Calculation**: Overall status computed based on individual team decisions
6. **Real-time Updates**: Interface reflects changes immediately through session state

## External Dependencies

### Python Packages
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **sqlalchemy**: ORM for database operations
- **psycopg2-binary**: PostgreSQL database adapter
- **uuid**: Unique identifier generation
- **datetime**: Timestamp management

### Runtime Requirements
- Python 3.7+ environment
- Streamlit server for web hosting
- PostgreSQL database for persistent storage

## Deployment Strategy

### Current Implementation
- **Storage**: PostgreSQL database (persistent across sessions)
- **Hosting**: Streamlit server deployment
- **Scalability**: Multi-user support with shared database state

### Limitations
- No user authentication or authorization system
- All users can see and modify all submissions
- Basic approval workflow without advanced features

### Future Considerations
- User authentication and authorization system
- Role-based access control for different approval teams
- Email notifications for approval workflows
- Advanced reporting and analytics
- API integration for external systems

## Changelog

```
Changelog:
- July 04, 2025. Initial setup
- July 04, 2025. Added PostgreSQL database integration for persistent storage
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```

## Notes for Development

The application now uses PostgreSQL database for persistent data storage, allowing submissions to persist across sessions. The architecture is designed for easy extension to include:

- User authentication and authorization
- Role-based access control for approval teams
- Email notifications for approval workflows
- Advanced reporting and analytics
- Integration with external IT service management tools

The modular function design makes it straightforward to add new approval teams, modify approval workflows, or integrate with external data sources. Database operations are handled through SQLAlchemy ORM with proper session management.