"""Bootstrap Ollama inside a managed Colab runtime."""
import os
import subprocess
import time

def main() -> None:
    subprocess.run("apt-get update -qq && apt-get install -y -qq zstd curl", shell=True, check=True)
    subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
    env = os.environ.copy()
    env["OLLAMA_HOST"] = "127.0.0.1:11434"
    subprocess.Popen(["ollama", "serve"], env=env)
    time.sleep(2)
    print("Ollama bootstrap complete.")

if __name__ == "__main__":
    main()
