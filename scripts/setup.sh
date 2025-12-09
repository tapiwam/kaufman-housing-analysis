#!/usr/bin/env bash
# Kaufman CAD Data Loader - Automated Setup Script
# This script sets up the complete environment, starts services, and loads data

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create log file
LOG_FILE="logs/setup_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=========================================="
echo "Kaufman CAD Data Loader - Setup Script"
echo "=========================================="
echo "Started: $(date)"
echo "Log file: $LOG_FILE"
echo ""

# Step 1: Check prerequisites
log_info "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
log_success "Python $PYTHON_VERSION found"

if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Please install Docker."
    exit 1
fi
log_success "Docker found"

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    log_error "Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi
log_success "Docker Compose found"

if ! command -v unzip &> /dev/null; then
    log_warn "unzip is not installed. Will skip automated data download."
    UNZIP_AVAILABLE=false
else
    UNZIP_AVAILABLE=true
fi

# Step 2: Download and extract CAD data (if needed)
DATA_DIR_2025="Kaufman-CAD-2025-Certified-Full-Roll-Download-updated-with-Supp-5"
DATA_URL_2025="https://kaufman-cad.org/wp-content/uploads/2025/11/Kaufman-CAD-2025-Certified-Full-Roll-Download-updated-with-Supp-5.zip"

if [ ! -d "$DATA_DIR_2025" ]; then
    log_info "CAD data directory not found: $DATA_DIR_2025"
    
    if [ "$UNZIP_AVAILABLE" = true ]; then
        read -p "Would you like to download 2025 CAD data automatically? (y/N): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Downloading 2025 CAD data from kaufman-cad.org..."
            log_info "This may take a few minutes (file is ~100MB)..."
            
            if command -v curl &> /dev/null; then
                curl -L -o "cad_data_2025.zip" "$DATA_URL_2025" --progress-bar
            elif command -v wget &> /dev/null; then
                wget -O "cad_data_2025.zip" "$DATA_URL_2025"
            else
                log_error "Neither curl nor wget found. Cannot download data automatically."
                log_info "Please download manually from: $DATA_URL_2025"
                exit 1
            fi
            
            log_success "Download complete"
            log_info "Extracting data files..."
            
            unzip -q "cad_data_2025.zip"
            rm "cad_data_2025.zip"
            
            log_success "Data extracted to $DATA_DIR_2025"
        else
            log_warn "Data download skipped"
            log_info "Please download manually from: $DATA_URL_2025"
            log_info "Extract to project root and re-run this script"
            exit 1
        fi
    else
        log_warn "unzip not available - cannot download data automatically"
        log_info "Please download manually from: $DATA_URL_2025"
        log_info "Extract to project root and re-run this script"
        exit 1
    fi
else
    log_success "CAD data directory found: $DATA_DIR_2025"
fi

# Step 3: Create virtual environment
log_info "Creating Python virtual environment..."

if [ -d ".venv" ]; then
    log_warn "Virtual environment already exists. Skipping creation."
else
    python3 -m venv .venv
    log_success "Virtual environment created"
fi

# Step 3: Activate virtual environment and install dependencies
log_info "Installing Python dependencies..."

source .venv/bin/activate

pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

log_success "Dependencies installed"

# Step 4: Start Docker services
log_info "Starting Docker services (PostgreSQL + pgAdmin)..."

docker-compose up -d

log_success "Docker services started"

# Step 5: Wait for PostgreSQL to be ready
log_info "Waiting for PostgreSQL to be ready..."

MAX_ATTEMPTS=30
ATTEMPT=0

until docker exec kaufman_cad_db pg_isready -U cad_user -d kaufman_cad &> /dev/null || [ $ATTEMPT -eq $MAX_ATTEMPTS ]; do
    ATTEMPT=$((ATTEMPT+1))
    echo -n "."
    sleep 1
done
echo ""

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    log_error "PostgreSQL failed to start within 30 seconds"
    exit 1
fi

log_success "PostgreSQL is ready"

# Step 6: Check if data needs to be loaded
log_info "Checking database state..."

RECORD_COUNT=$(docker exec kaufman_cad_db psql -U cad_user -d kaufman_cad -t -c "SELECT COUNT(*) FROM cad.appraisal_info;" 2>/dev/null | tr -d ' ' || echo "0")

if [ "$RECORD_COUNT" -gt "0" ]; then
    log_warn "Database already contains $RECORD_COUNT records in appraisal_info table"
    read -p "Do you want to reload data? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Skipping data load"
        SKIP_LOAD=true
    else
        log_info "Recreating database schema..."
        docker exec kaufman_cad_db psql -U cad_user -d kaufman_cad -f /docker-entrypoint-initdb.d/001_create_schema.sql
        SKIP_LOAD=false
    fi
else
    log_info "Database is empty, will load data"
    SKIP_LOAD=false
fi

# Step 7: Load data
if [ "$SKIP_LOAD" != "true" ]; then
    log_info "Loading CAD data into database..."
    log_info "This may take several minutes..."
    
    python3 scripts/load_data.py
    
    log_success "Data loading complete"
else
    log_info "Data loading skipped"
fi

# Step 8: Display summary
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "📊 Database Information:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  Database: kaufman_cad"
echo "  Username: cad_user"
echo "  Password: cad_password"
echo ""
echo "🌐 pgAdmin Web Interface:"
echo "  URL: http://localhost:5050"
echo "  Email: admin@admin.com"
echo "  Password: admin"
echo ""
echo "📝 Next Steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Open Jupyter notebooks: jupyter notebook"
echo "  3. Explore analysis/gateway_parks_analysis.ipynb"
echo ""
echo "🛑 To stop services: docker-compose down"
echo "📋 View logs: tail -f $LOG_FILE"
echo ""
log_success "Setup completed successfully at $(date)"
