import subprocess
import sys
import urllib.request
import time

def run_command(command, check=True):
    """Run a shell command and handle errors."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        sys.exit(1)
    return result

def check_url(url, retries=5, delay=5):
    """Check if a URL is accessible."""
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                if response.status == 200:
                    print(f"Application is accessible at {url}")
                    return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{retries}: Waiting for {url}... ({str(e)})")
            time.sleep(delay)
    print(f"Failed to access {url} after {retries} attempts")
    return False

def main():
    print("Starting local setup for React app...")
    
    # Build React app
    print("Installing dependencies and building React app...")
    run_command("npm install")
    run_command("npm run build")
    
    # Build Docker image
    print("Building Docker image...")
    run_command("docker build -t react-app:latest .")
    
    # Run Docker container
    print("Running Docker container...")
    run_command("docker run -d -p 8080:80 --name react-app-container react-app:latest")
    
    # Verify application is running
    print("Verifying application...")
    if check_url("http://localhost:8080"):
        print("Local setup completed successfully!")
    else:
        print("Local setup failed. Please check the container logs.")
        run_command("docker logs react-app-container", check=False)
        sys.exit(1)

if __name__ == "__main__":
    main()