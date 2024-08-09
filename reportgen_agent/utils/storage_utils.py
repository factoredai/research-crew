# TODO: This is far from the best approach, we should build a frontend 
# for the LangGraph checkpoints and rely on them. This was create for easy
# debugging in our initial state as we can just open local files directly.

import os
import json
from datetime import datetime
from typing import Tuple, Dict, Any

from reportgen_agent.core.state import ReportGenState


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'app_history')
)
os.makedirs(BASE_DIR, exist_ok=True)

def create_run_directory(base_dir: str = BASE_DIR) -> Tuple[str, str]:
    """Create a directory for the current run with a timestamp.

    Parameters
    ----------
    base_dir : str, optional
        The base directory where the run directory will be created.
        Defaults to BASE_DIR.

    Returns
    -------
    Tuple[str, str]
        A tuple containing the path to the created run directory and the 
        timestamp.

    """   
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(base_dir, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    return run_dir, timestamp

def save_state(state: ReportGenState, run_dir: str, step_name: str) -> None:
    """Save the state to a JSON file in the specific step's directory.

    Parameters
    ----------
    state : Dict[str, Any]
        The state to be saved.
    run_dir : str
        The directory of the current run.
    step_name : str
        The name of the current step.
    """
    state_dir = os.path.join(run_dir, step_name)
    os.makedirs(state_dir, exist_ok=True)
    state_file = os.path.join(state_dir, 'state.json')
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(e)

def save_webpage(content: str, run_dir: str, url: str, step_name: str) -> None:
    """Save the webpage content to an HTML file in the specific step's directory.

    Parameters
    ----------
    content : str
        The content of the webpage to be saved.
    run_dir : str
        The directory of the current run.
    url : str
        The URL of the webpage.
    step_name : str
        The name of the current step.

    Notes
    -----
    This function saves the webpage content as an HTML file and logs the action to TinyDB.
    The URL is sanitized to create a valid filename.
    """    
    sanitized_url = url.replace("http://", "").replace("https://", "").replace("/", "_")
    state_dir = os.path.join(run_dir, step_name)
    os.makedirs(state_dir, exist_ok=True)
    html_file = os.path.join(state_dir, f"{sanitized_url}.html")
    with open(html_file, 'w') as f:
        f.write(content)
    
