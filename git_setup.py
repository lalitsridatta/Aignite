"""Git setup script for the Judicial Court Process Explainer Bot."""

import subprocess
import os
import sys

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {str(e)}")
        return False

def setup_git_repo():
    """Set up Git repository and push to remote."""
    
    print("🚀 Setting up Git Repository for Judicial Court Process Explainer Bot")
    print("=" * 70)
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("Please install Git first: https://git-scm.com/downloads")
        return False
    
    # Initialize git repo if not already initialized
    if not os.path.exists(".git"):
        run_command("git init", "Initializing Git repository")
    
    # Add all files
    run_command("git add .", "Adding all files to Git")
    
    # Create initial commit
    commit_message = "feat: Add Judicial Court Process & Case Flow Explainer Bot - Award-winning AI system with RAG, safety constraints, and Streamlit interface"
    run_command(f'git commit -m "{commit_message}"', "Creating initial commit")
    
    # Check if remote exists
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("\n📝 No remote repository found.")
        print("To push to GitHub:")
        print("1. Create a new repository on GitHub")
        print("2. Run these commands:")
        print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git")
        print("   git branch -M main")
        print("   git push -u origin main")
    else:
        print(f"\n📡 Remote repository found:")
        print(result.stdout)
        
        # Try to push
        if run_command("git push", "Pushing to remote repository"):
            print("🎉 Successfully pushed to remote repository!")
        else:
            print("⚠️  Push failed. You may need to set up the remote or resolve conflicts.")
    
    print("\n" + "=" * 70)
    print("🏆 Git setup complete!")
    print("\n📂 Repository Contents:")
    print("   📄 Core System: app.py, simple_rag_pipeline.py, document_processor.py")
    print("   🛡️  Safety: safety_validator.py")
    print("   🧪 Testing: test_simple_rag.py, quota_checker.py")
    print("   📚 Docs: README.md, PROJECT_OVERVIEW.md")
    print("   📁 Data: documents/ folder with court PDFs")

def create_github_commands():
    """Create a file with GitHub setup commands."""
    
    github_commands = """# GitHub Setup Commands

## If you haven't created a GitHub repository yet:

1. Go to https://github.com/new
2. Create a new repository named "judicial-court-explainer"
3. Don't initialize with README (we already have files)

## Then run these commands:

```bash
git remote add origin https://github.com/YOUR_USERNAME/judicial-court-explainer.git
git branch -M main
git push -u origin main
```

## Repository Description for GitHub:

**Title:** Judicial Court Process & Case Flow Explainer Bot

**Description:** 
Award-winning AI-powered chatbot that explains court procedures and case lifecycles using RAG (Retrieval-Augmented Generation). Built with Gemini AI, Streamlit, and strict safety constraints to provide factual procedural information without legal advice.

**Tags:** 
ai, chatbot, legal-tech, rag, gemini, streamlit, court-procedures, legal-education, responsible-ai, hackathon

## Features to highlight:
- 🤖 RAG-powered document retrieval
- 🛡️ Safety-first design (no legal advice)
- 📚 Document-grounded responses
- 🎨 Clean Streamlit interface
- 🔍 Text-based search fallback
- 📊 Source attribution
- 🧪 Comprehensive testing suite
"""
    
    with open("GITHUB_SETUP.md", "w") as f:
        f.write(github_commands)
    
    print("📝 Created GITHUB_SETUP.md with detailed instructions")

def main():
    """Main function."""
    setup_git_repo()
    create_github_commands()
    
    print(f"\n🎯 Next Steps:")
    print("1. Check GITHUB_SETUP.md for GitHub repository setup")
    print("2. Run the application: python -m streamlit run app.py")
    print("3. Test with different API keys if needed")
    print("4. Share your award-winning AI system! 🏆")

if __name__ == "__main__":
    main()