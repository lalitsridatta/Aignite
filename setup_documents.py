"""Utility script to copy court documents from hackiee folder to documents folder."""

import os
import shutil
from pathlib import Path


def copy_documents_from_hackiee():
    """Copy PDF documents from hackiee folder on desktop to documents folder."""
    
    # Define source and destination paths
    desktop_path = Path.home() / "Desktop"
    hackiee_path = desktop_path / "hackiee"
    documents_path = Path("documents")
    
    print(f"Looking for documents in: {hackiee_path}")
    
    # Check if hackiee folder exists
    if not hackiee_path.exists():
        print(f"❌ Hackiee folder not found at: {hackiee_path}")
        print("Please ensure the hackiee folder exists on your Desktop")
        return False
    
    # Create documents folder if it doesn't exist
    documents_path.mkdir(exist_ok=True)
    
    # Find all PDF files in hackiee folder (including subfolders)
    pdf_files = list(hackiee_path.rglob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in hackiee folder")
        return False
    
    print(f"Found {len(pdf_files)} PDF files:")
    
    # Copy each PDF file
    copied_count = 0
    for pdf_file in pdf_files:
        try:
            destination = documents_path / pdf_file.name
            
            # Avoid overwriting existing files
            if destination.exists():
                print(f"⚠️  Skipping {pdf_file.name} (already exists)")
                continue
            
            shutil.copy2(pdf_file, destination)
            print(f"✅ Copied: {pdf_file.name}")
            copied_count += 1
            
        except Exception as e:
            print(f"❌ Error copying {pdf_file.name}: {str(e)}")
    
    print(f"\n📊 Successfully copied {copied_count} PDF files to documents folder")
    return copied_count > 0


if __name__ == "__main__":
    print("🔄 Setting up court documents...")
    success = copy_documents_from_hackiee()
    
    if success:
        print("\n✅ Document setup complete!")
        print("You can now run the application with: streamlit run app.py")
    else:
        print("\n❌ Document setup failed!")
        print("Please manually copy your PDF files to the 'documents' folder")