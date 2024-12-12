#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
LOG_DIR="logs"
BACKUP_DIR="backups"
DATA_DIR="data"

# Function to print colored header
print_header() {
    echo -e "${BLUE}==================================="
    echo -e "$1"
    echo -e "===================================${NC}"
}

# Function to check if command was successful
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Success!${NC}"
    else
        echo -e "${RED}Failed!${NC}"
        exit 1
    fi
}

# Function to setup environment
setup_environment() {
    print_header "Setting up environment"
    
    # Create necessary directories
    mkdir -p $LOG_DIR $BACKUP_DIR $DATA_DIR
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        check_status
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install requirements
    echo "Installing requirements..."
    pip install -r requirements.txt
    check_status
}

# Function to create backup
create_backup() {
    print_header "Creating Backup"
    
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_NAME="backup_${TIMESTAMP}.tar.gz"
    
    # Create backup of source code and data
    tar -czf "${BACKUP_DIR}/${BACKUP_NAME}" src/ data/ requirements.txt
    check_status
    
    echo -e "${GREEN}Backup created: ${BACKUP_NAME}${NC}"
}

# Function to restore backup
restore_backup() {
    print_header "Available Backups"
    
    # List available backups
    ls -1 $BACKUP_DIR
    
    read -p "Enter backup name to restore (or 'cancel'): " backup_name
    
    if [ "$backup_name" != "cancel" ] && [ -f "${BACKUP_DIR}/${backup_name}" ]; then
        tar -xzf "${BACKUP_DIR}/${backup_name}"
        check_status
        echo -e "${GREEN}Backup restored successfully${NC}"
    fi
}

# Function to manage logs
manage_logs() {
    print_header "Log Management"
    echo "1. View Recent Logs"
    echo "2. Clear Logs"
    echo "3. Export Logs"
    echo "4. Back to Main Menu"
    
    read -p "Select option (1-4): " log_choice
    
    case $log_choice in
        1)
            tail -n 50 ${LOG_DIR}/system.log
            ;;
        2)
            rm ${LOG_DIR}/*.log
            echo -e "${GREEN}Logs cleared${NC}"
            ;;
        3)
            zip -r logs_export.zip ${LOG_DIR}
            echo -e "${GREEN}Logs exported to logs_export.zip${NC}"
            ;;
    esac
}

# Function to run system diagnostics
run_diagnostics() {
    print_header "Running System Diagnostics"
    
    # Check disk space
    echo "Checking disk space..."
    df -h .
    
    # Check Python version
    echo -e "\nChecking Python version..."
    python --version
    
    # Check installed packages
    echo -e "\nChecking installed packages..."
    pip list
    
    # Test database connection
    echo -e "\nTesting components..."
    python -m src.tests.run_all_tests
}

# Function to run monitoring mode
run_monitoring() {
    print_header "Starting Monitoring Mode"
    
    # Start logging
    exec 1> >(tee -a "${LOG_DIR}/system.log")
    
    echo "Starting monitoring at $(date)"
    streamlit run dashboard.py
}

# Enhanced main menu
show_menu() {
    clear
    print_header "AI Maintenance Agent System"
    echo "1. Run Dashboard"
    echo "2. Run All Tests"
    echo "3. Run Individual Tests"
    echo "4. Setup/Reset Environment"
    echo "5. Create Backup"
    echo "6. Restore Backup"
    echo "7. Manage Logs"
    echo "8. Run System Diagnostics"
    echo "9. Run Monitoring Mode"
    echo "10. Clean System"
    echo "11. Exit"
    echo
    read -p "Select an option (1-11): " choice
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1)
            streamlit run dashboard.py
            ;;
        2)
            python -m src.tests.run_all_tests
            check_status
            read -p "Press Enter to continue..."
            ;;
        3)
            run_individual_tests
            ;;
        4)
            setup_environment
            read -p "Press Enter to continue..."
            ;;
        5)
            create_backup
            read -p "Press Enter to continue..."
            ;;
        6)
            restore_backup
            read -p "Press Enter to continue..."
            ;;
        7)
            manage_logs
            read -p "Press Enter to continue..."
            ;;
        8)
            run_diagnostics
            read -p "Press Enter to continue..."
            ;;
        9)
            run_monitoring
            ;;
        10)
            find . -type d -name "__pycache__" -exec rm -r {} +
            find . -type f -name "*.pyc" -delete
            check_status
            read -p "Press Enter to continue..."
            ;;
        11)
            print_header "Exiting..."
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            read -p "Press Enter to continue..."
            ;;
    esac
done
