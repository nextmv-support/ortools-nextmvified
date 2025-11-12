 # OR-Tools + Nextmv: From Local Model to Cloud-Native Optimization

This repository demonstrates how to evolve a basic OR-Tools optimization model into a cloud-ready application using Nextmv. The examples show a small, local model (the Stigler diet problem), how to prepare it for Nextmv, and how to add lightweight experimentation and statistics.

## The Journey: Three Stages of Evolution

### 🏠 Stage 1: Basic Local OR-Tools Model (`starting-state/`)

A small OR-Tools implementation of the Stigler diet problem that runs locally.

Run locally:

```bash
cd starting-state/
pip install -r requirements.txt
python main.py
```

What the example includes:

- ✅ OR-Tools solver model (`starting-state/main.py`)
- ✅ Externalized input file: `starting-state/inputs/diet_data.json`
- ✅ Produces `solution.txt` (human-readable) and `statistics.json` (Nextmv-style statistics)

### ☁️ Stage 2: Run in Nextmv (`run_in_nextmv_state/`)

Changes made (example):

1. An `app.yaml` manifest that tells Nextmv how to run the model and handle inputs/outputs.

Example Nextmv commands (replace example app name and run ID as needed):

```bash
cd run_in_nextmv_state/
tar czf - diet.dat | nextmv app run -a ortools-example
nextmv app output -a ortools-example -r <runID>
```

What you unlock:

- ✅ Observability (logs, metrics)
- ✅ Collaboration and instance management
- ✅ Cloud execution and scaling

### 🧪 Stage 3: Full Experimentation Platform (`final_state/`)

Additional changes shown in `final_state/` include:

1. Statistics output compatible with Nextmv experimentation (JSON)
2. Configurable options in `app.yaml` so you can run parameter sweeps

Example:

```bash
cd final_state/
tar czf - diet.dat | nextmv app run -a ortools-example -o "limit_dairy=true"
nextmv app output -a ortools-example -r <runID>
```

What you unlock:

- ✅ Configuration testing and parameter sweeps
- ✅ Performance analytics and custom statistics
- ✅ Easy comparison between runs

## The Model: Stigler Diet

This is the Stigler diet problem — a classic optimization that minimizes the cost of a diet while meeting nutritional requirements.

- Objective: Minimize total cost
- Constraints: Meet minimum nutrition requirements (calories, protein, vitamins, etc.)
- The example can be extended with optional constraints (e.g. limit dairy) for experimentation

## Inputs and Outputs

- Input data (nutrients and food items) are stored in `starting-state/inputs/diet_data.json`.
- Running the example writes a human-readable summary to `solution.txt` (appended) and a JSON statistics file `statistics.json` (used by Nextmv) when available.

## Running the Examples

Prerequisites

- Python 3.8+ (examples use Python 3.11 in Nextmv runtimes)
- Install dependencies in the folder you want to run:

Local execution (starting-state):

```bash
cd starting-state/
pip install -r requirements.txt
python main.py
```

Notes:

- The example reads inputs from `starting-state/inputs/diet_data.json`.
- It appends a human-readable summary to `solution.txt` and writes `statistics.json` with Nextmv-style statistics when `nextmv` is available.
- If you don't have OR-Tools installed, install it with `pip install ortools` or use the provided `requirements.txt`.

## Deploy to Nextmv Cloud

```bash
python push.py
```

## The Power of This Approach

Small, well-placed changes (an app manifest and lightweight statistics) let you move from a local script to a cloud-native optimization application with observability, experiment tracking, and team-ready deployment.

---

For details on the implementation, see `starting-state/main.py` and `final_state/main.py`.
# Gurobipy + Nextmv: From Local Model to Cloud-Native Optimization

This repository demonstrates how to evolve a basic `gurobipy` optimization model into a fully-featured, cloud-native application using Nextmv. We'll take you through three stages of development, showing how minimal changes unlock powerful capabilities like observability, collaboration, instance management, version control, and experimentation.

## The Journey: Three Stages of Evolution

### 🏠 Stage 1: Basic Local Gurobipy Model (`starting-state/`)

A standard `gurobipy` diet optimization model that runs locally:

```bash
cd starting-state/
python main.py
```

**What you get:**

- ✅ Working optimization model
- ✅ Local execution
- ❌ No version control
- ❌ No collaboration features  
- ❌ No observability
- ❌ No experimentation

### ☁️ Stage 2: Run in Nextmv (`run_in_nextmv_state/`)

**Changes made:**

1. **Added `app.yaml` manifest** - Tells Nextmv how to run your model

```bash
cd run_in_nextmv_state/
tar czf - diet.dat | nextmv app run -a gurobipy-example 
nextmv app output -a gurobipy-example -r <insert runID here>
```

**What you unlock:**

- ✅ **Observability**: Detailed execution logs and metrics
- ✅ **Collaboration**: Share apps with team members
- ✅ **Instance Management**: Deploy and manage app versions
- ✅ **Version Control**: Track model changes over time
- ✅ **Cloud Execution**: Run on Nextmv's optimized infrastructure

### 🧪 Stage 3: Full Experimentation Platform (`final_state/`)

**Additional changes:**

1. **Added statistics output** - For experiment tracking and comparison
2. **Exposed options in `app.yaml`** - For model configuration

```bash
cd final_state/
tar czf - diet.dat | nextmv app run -a gurobipy-example -o "limit_dairy=true"
nextmv app output -a gurobipy-example -r <insert runID here>
```

**What you unlock:**

- ✅ **Configuration Testing**: Compare different solver configurations
- ✅ **Parameter Sweeps**: Test multiple scenarios automatically
- ✅ **Performance Analytics**: Track solution quality and runtime
- ✅ **Business Metrics**: Custom statistics for your domain

## The Model: Diet Optimization

This is a classic optimization problem that minimizes the cost of a diet while meeting nutritional requirements:

- **Objective**: Minimize total cost of food
- **Constraints**:
  - Meet minimum nutritional requirements (calories, protein, vitamins, etc.)
  - Stay within maximum volume limit
  - Optional: Limit dairy products (experimentation feature)

## Key Changes Explained

### The Minimal App Manifest (`app.yaml`)

```yaml
type: python
runtime: ghcr.io/nextmv-io/runtime/python:3.11
python:
  pip-requirements: requirements.txt
files:
  - main.py
configuration:
  content:
    format: "multi-file"
    multi-file:
      input:
        path: "."
      output:
        solutions: "."
        statistics: "statistics.json"
```

This tells Nextmv:

- Use the Python runtime
- Include your Python files
- How to handle input/output data

### Adding Experimentation Capabilities

1. **Statistics Output** (`main.py`):

```python
import nextmv

statistics = nextmv.Statistics(
    result=nextmv.ResultStatistics(
        duration=m.Runtime,
        value=m.ObjVal,
        custom={
            "nvars": m.NumVars,
            "ncons": m.NumConstrs,
        },
    ),
)
```

2.**Configurable Options** (`app.yaml`):

```yaml
configuration:
  options:
    items:
      - name: limit_dairy
        option_type: bool
        default: false
        ui:
          control_type: toggle
```

## Running the Examples

### Prerequisites

### Local Execution

```bash
pip install -r requirements.txt
python main.py

```

### Deploy to Nextmv Cloud

```bash
python push.py
```

## The Power of This Approach

With just one simple change (adding `app.yaml`), you transform a local script into a cloud-native optimization application with:

- **Zero infrastructure management**
- **Built-in experiment tracking**
- **Team collaboration features**
- **Automatic scaling**
- **Version control and rollback**
- **Performance monitoring**

This is the power of "Nextmvifying" your optimization models - minimal changes, maximum impact.
