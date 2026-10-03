# Process Dynamics and Control

Source code for the [Process Dynamics and Control Course](https://apmonitor.com/pdc). The archive is organized by learning module from the [course schedule](https://apmonitor.com/pdc/index.php/Main/CourseSchedule) with source code by Topic, Quiz, Assignment, and Temperature Control Lab activity. The [get_source.py](get_source.py) Python program retrieves the lastest version of the source code from each page listed in [pages.csv](pages.csv).

![PDC Course Overview](https://apmonitor.com/pdc/uploads/Main/pdc_overview.png)

## Set up the Python environment

The examples use Python packages listed in [requirements.txt](requirements.txt). Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first, then run the following commands from the repository directory. Python 3.9 is recommended for this environment.

### Linux and macOS

```bash
uv venv --python 3.9 .venv
uv pip install -r requirements.txt
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
uv venv --python 3.9 .venv
uv pip install -r requirements.txt
.venv\Scripts\Activate.ps1
```

In Command Prompt, activate with `.venv\Scripts\activate.bat` instead. If PowerShell blocks activation scripts, use Command Prompt or follow Microsoft's [PowerShell execution policy instructions](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies).

To leave the virtual environment, run `deactivate` in the terminal. Re-run the activation command whenever you open a new terminal to work on the project.
