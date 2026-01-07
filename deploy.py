"""Deployment script for the Judicial Court Process Explainer Bot."""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False


def setup_documents():
    """Setup documents from hackiee folder."""
    print("📁 Setting up documents...")
    try:
        subprocess.check_call([sys.executable, "setup_documents.py"])
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Automatic document setup failed")
        print("Please manually copy PDF files to the 'documents' folder")
        return False


def run_tests():
    """Run system tests."""
    print("🧪 Running system tests...")
    try:
        result = subprocess.run([sys.executable, "test_system.py"], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False


def launch_application():
    """Launch the Streamlit application."""
    print("🚀 Launching Judicial Court Process Explainer Bot...")
    try:
        subprocess.check_call(["streamlit", "run", "app.py"])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch application: {e}")
        print("Try running manually: streamlit run app.py")
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")


def main():
    """Main deployment function."""
    print("🏛️  Judicial Court Process & Case Flow Explainer Bot")
    print("=" * 60)
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Install requirements
    if not install_requirements():
        return
    
    # Step 3: Setup documents
    setup_documents()
    
    # Step 4: Run tests (optional, continue even if tests fail)
    print("\n" + "=" * 60)
    test_passed = run_tests()
    if not test_passed:
        print("⚠️  Some tests failed, but continuing with deployment...")
    
    # Step 5: Launch application
    print("\n" + "=" * 60)
    print("🎯 Deployment complete! Launching application...")
    print("\nOnce the application starts:")
    print("1. The system will automatically use the configured Gemini API key")
    print("2. Documents will be processed and indexed")
    print("3. You can start asking questions about court procedures")
    print("\n" + "=" * 60)
    
    launch_application()


if __name__ == "__main__":
    main()