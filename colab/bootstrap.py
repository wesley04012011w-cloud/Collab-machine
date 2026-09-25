import os, subprocess, sys, time

ROOT=os.path.dirname(__file__)

def run(*args):
    subprocess.run(args, check=True)

run("apt-get","update","-qq")
run("apt-get","install","-y","-qq","zstd","curl")
run(sys.executable,"-m","pip","install","-q","fastapi","uvicorn","httpx")

if subprocess.run(["bash","-lc","command -v ollama"],capture_output=True).returncode != 0:
    run("bash","-lc","curl -fsSL https://ollama.com/install.sh | sh")

env={**os.environ,"OLLAMA_HOST":"127.0.0.1:11434"}
subprocess.Popen(["ollama","serve"],env=env)
time.sleep(3)

agent_env={**os.environ,"OLLAMA_URL":"http://127.0.0.1:11434",
           "OLLAMA_STUDIO_TOKEN":os.environ.get("OLLAMA_STUDIO_TOKEN","change-this-token")}
subprocess.Popen([sys.executable,"-m","uvicorn","agent:app","--host","0.0.0.0","--port","8787"],
                 cwd=ROOT,env=agent_env)

print("Collab Machine agent running on port 8787.")
print("Set OLLAMA_STUDIO_TOKEN to a strong secret before exposing the port.")
