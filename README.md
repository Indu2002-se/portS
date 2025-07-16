# PortSentinel - Advanced Port Scanning Solution

![PortSentinel Logo](scanner_tool/static/images/abs.jpg)

## Overview

PortSentinel is a comprehensive network port scanning application designed for security professionals, network administrators, and IT enthusiasts. It provides advanced capabilities for discovering open ports, identifying running services, analyzing security vulnerabilities, and managing scan results.

## Features

- **Multi-threaded Scanning**: Fast and efficient port discovery using parallel scanning threads
- **Service Identification**: Detailed information about services running on open ports
- **Banner Grabbing**: Extract service banners to identify software versions and configurations
- **SSL Certificate Analysis**: Inspect SSL/TLS certificates on secured services
- **Real-time Monitoring**: Watch scan progress with interactive interface updates
- **Export Capabilities**: Save results in multiple formats (CSV, Excel, PDF)
- **History Management**: Track and review previous scan exports
- **User Authentication**: Secure multi-user system with email verification
- **Dashboard Analytics**: Visualize scanning statistics and patterns

## System Architecture

PortSentinel follows a modular architecture organized into the following components:

### Core Components

1. **Scanner Engine (`scanner_engine.py`)**: 
   - Handles port scanning operations
   - Identifies services and grabs banners
   - Analyzes SSL certificates

2. **Threading Module (`threading_module.py`)**:
   - Manages parallel execution of scanning operations
   - Optimizes resource utilization

3. **Data Export Layer (`data_export_layer.py`)**:
   - Formats and exports scan results to different file formats
   - Manages export history

4. **Web Interface (`flask_web_interface.py`)**:
   - Provides a user-friendly web interface
   - Handles HTTP requests and responses
   - Manages templates and static assets

5. **Authentication System (`auth.py`)**:
   - User registration and login
   - Email verification
   - Session management

### Database

- **Supabase Backend**:
  - User management and authentication
  - Scan history storage
  - Export tracking
  - User feedback collection

### Frontend

- **HTML/CSS/JavaScript**:
  - Responsive web interface
  - Real-time scan monitoring
  - Interactive results display
  - Theme customization

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection for initial setup

### Method 1: Quick Installation

```bash
# Clone the repository
git clone <repository-url>

# Navigate to project directory
cd Portsentinal-Scanner

# Install dependencies
pip install -r requirements.txt

# Launch the application
python main.py
```

### Method 2: Development Setup

```bash
# Clone the repository
git clone <repository-url>

# Navigate to project directory
cd Portsentinal-Scanner

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch the web interface
python scanner_tool/flask_web_interface.py

# For command-line only mode
python scanner_tool/main.py
```

## Usage Process

### 1. User Authentication

1. Create an account via the signup page
2. Verify your email address using the confirmation link
3. Log in to access the scanner dashboard

### 2. Basic Scan Process

1. Navigate to the Scanner page
2. Enter target IP address or hostname
3. Configure scan parameters:
   - Port range (predefined or custom)
   - Thread count
   - Timeout settings
4. Click "Start Scan" to begin the process
5. Monitor real-time progress with the status bar
6. View results in table or log format

### 3. Working with Results

1. Review discovered open ports and services
2. Examine detailed service information and banners
3. Export results in your preferred format:
   - CSV for data processing
   - Excel for spreadsheet analysis
   - PDF for formal reports

### 4. Results Management

1. Access the Export History page
2. View statistics about your export patterns
3. Filter and search through previous exports
4. Download past exports as needed

## Command Line Interface

PortSentinel also provides a command-line interface for advanced users:

```bash
python scanner_tool/main.py -t <target> -p <ports> -th <threads>
```

Example:
```bash
python scanner_tool/main.py -t example.com -p 80,443,8000-8100 -th 20
```

Available options:
```
-t, --target      Target hostname or IP address
-p, --ports       Port range (e.g., 80,443,8000-8100)
-th, --threads    Number of scanning threads
-to, --timeout    Connection timeout in seconds
-o, --output      Output file format (csv, excel, pdf)
```

## System Workflow

1. **Initialization**:
   - Web server starts and loads templates
   - Authentication system connects to Supabase
   - Scanner components initialize

2. **Scan Execution**:
   - Target validation occurs
   - Port list is parsed and prepared
   - Multi-threaded scanning begins
   - Real-time progress updates flow to UI

3. **Port Analysis**:
   - Each open port triggers service identification
   - Banner grabbing extracts version information
   - SSL certificates are analyzed if applicable

4. **Results Processing**:
   - Scan results are compiled and organized
   - UI displays formatted results
   - Data is prepared for potential export

5. **Export Handling**:
   - User selects desired export format
   - Data Export Layer formats the results
   - File is generated and offered for download
   - Export record is saved to history

## Development Information

### Project Structure

```
Portsentinal-Scanner/
  ├── index.html              # Landing page HTML
  ├── main.py                 # CLI entry point
  ├── requirements.txt        # Python dependencies
  ├── scan_results/           # Storage for scan results
  └── scanner_tool/           # Main application package
      ├── auth.py             # Authentication system
      ├── data_export_layer.py # Export functionality
      ├── database/           # Database files
      ├── flask_web_interface.py # Web interface
      ├── main.py             # Scanner core
      ├── scanner_engine.py   # Port scanning logic
      ├── scanner_tool/       # Web assets subpackage
      ├── static/             # Static web assets
      │   ├── css/            # Stylesheets
      │   ├── images/         # Images
      │   └── js/             # JavaScript files
      ├── templates/          # HTML templates
      │   ├── admin/          # Admin templates
      │   ├── auth/           # Authentication templates
      │   └── ...             # Other templates
      └── threading_module.py # Multi-threading support
```

### Key Technologies

- **Backend**: Python, Flask
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Supabase Auth
- **Network Tools**: Socket, SSL, IPAddress libraries
- **Visualization**: Rich (terminal), custom CSS

## Security Considerations

- Only scan networks and systems you own or have explicit permission to scan
- Port scanning may trigger security alerts on monitored networks
- Use the application responsibly and within legal boundaries
- Protect your account credentials and scan data

## License

[Include license information here]

## Contributors

[List of contributors]

## Contact

[Contact information] 