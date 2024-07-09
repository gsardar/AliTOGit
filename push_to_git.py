import os
import subprocess

def push_to_github(repo_url, local_dir):
    os.chdir(local_dir)
    
    # Initialize Git repository if needed
    if not os.path.exists(os.path.join(local_dir, ".git")):
        subprocess.run(["git", "init"], check=True)
        
    # Add files to staging area
    subprocess.run(["git", "add", "."], check=True)
    
    # Commit changes
    subprocess.run(["git", "commit", "-m", "Pushed files from Python"], check=True)
    
    # Set remote repository
    subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
    
    # Push to GitHub
    subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
    
    print("Files pushed to GitHub successfully!")

if __name__ == "__main__":
    repo_url = "https://github.com/gsardar/AliTOGit.git"
    local_dir = "C:\\Users\\Admin\\Desktop\\3.Projects\\Shopify\\AliTOGit\\gitRepo\\"
    push_to_github(repo_url, local_dir)
