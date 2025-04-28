# Local Test Harness for Project 3 – UFO Sighting Analysis


## 0  Prerequisites

| Tool | Version | Install hint |
|------|---------|--------------|
| Docker Desktop / Docker Engine | 20.10+ | https://docs.docker.com/get-docker/ |
| Python | ≥ 3.8 | Already on macOS & most Linux distros |
| uv (pkg mgr) | latest | `python3 -m pip install --user uv` |
| Apptainer (optional) | 1.2+ | `brew install apptainer` \| cluster module |

---

## 1  Clone & install Python deps

```bash
git clone https://github.com/AmaanSajid/cis6930sp25-project3.git
cd cis6930sp25-project3

python3 -m pip install --user uv   # one-liner if not installed
python3 -m uv sync                 # creates .venv & installs deps
```


## 2  Start RabbitMQ + live publisher
```bash
docker compose up -d        # broker on 5672, UI on 15672
docker compose ps           # STATUS → "running (healthy)"
open http://localhost:15672 # login: guest / guest   (macOS)
```

- You should also see the publisher container streaming logs:
```bash
docker compose logs -f publisher
```

## 3  Run tests
```bash
python3 -m uv run python -m pytest -v
```

## 4  Stream & classify messages
```bash
python3 -m uv run python -m src.main \
        --consume --command localhost --port 5672
```
- Ctrl-C after ~30 s

## 5  Generate the four PDF reports
```bash
python3 -m uv run python -m src.main --report
```

## 6  Container build
```bash
apptainer build project3.sif apptainer.def
apptainer run project3.sif localhost 5672
# (Ctrl-C after a few messages)
```

## 7  Clean up
```bash
docker compose down         # stop broker + publisher
```

## Running Directly on DGX server
Verify

```bash
apptainer --version
```
Build your image
```bash
git clone https://github.com/AmaanSajid/cis6930sp25-project3.git
cd cis6930sp25-project3
apptainer build project3.sif apptainer.def
apptainer run project3.sif cpu002.cm.cluster 5672
```

Or, if you’re using the local test harness:

bash
```bash
apptainer run project3.sif localhost 5672
```

- All artefacts (CSV, PDFs, log) appear in output/, exactly like on your laptop.

