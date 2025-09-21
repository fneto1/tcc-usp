#!/bin/bash
# Setup script for 48h Academic Experiment
# Creates environment and installs dependencies

echo "🎓 Setting up 48h Academic Saga Experiment"
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed"
    exit 1
fi

echo "✓ Prerequisites check passed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Create Docker network
echo "🐳 Setting up Docker network..."
docker network create saga-test-network 2>/dev/null || echo "✓ Network already exists"

# Make scripts executable
echo "🔧 Setting up script permissions..."
chmod +x *.py
chmod +x *.sh

# Test Docker connectivity
echo "🧪 Testing Docker setup..."
docker run --rm hello-world > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Docker test successful"
else
    echo "❌ Docker test failed"
    exit 1
fi

# Verify Saga services are built
echo "🔍 Checking Saga service builds..."

if [ -d "../saga-orquestrado" ]; then
    echo "✓ Orchestrated saga directory found"
else
    echo "❌ Orchestrated saga directory not found"
    exit 1
fi

if [ -d "../saga-coreografado" ]; then
    echo "✓ Choreographed saga directory found"
else
    echo "❌ Choreographed saga directory not found"
    exit 1
fi

# Create results directory
mkdir -p results
echo "✓ Results directory created"

echo ""
echo "🎯 Setup Complete!"
echo "=========================================="
echo "To run the complete experiment:"
echo "  python3 run_complete_experiment.py"
echo ""
echo "To run individual pattern tests:"
echo "  python3 academic_test_suite_48h.py orchestrated http://localhost:3000"
echo "  python3 academic_test_suite_48h.py choreographed http://localhost:3000"
echo ""
echo "To run statistical analysis:"
echo "  python3 statistical_analysis.py results_orch.json results_choreo.json"
echo "=========================================="