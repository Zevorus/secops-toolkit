import os
import shutil
from pathlib import Path
from typing import Optional, List
from dotenv import set_key, find_dotenv

# Directory structure:
# ~/.secops-toolkit/
# ├── .env (Current active profile)
# └── profiles/
#     ├── main_profile.env
#     ├── other_profile.env
#     └── ...

GLOBAL_CONFIG_DIR = Path.home() / ".secops-toolkit"
PROFILES_DIR = GLOBAL_CONFIG_DIR / "profiles"
ACTIVE_CONFIG_FILE = GLOBAL_CONFIG_DIR / ".env"

def ensure_dirs():
    """Ensure profiles and global config directories exist."""
    if not PROFILES_DIR.exists():
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)

def get_profile_path(profile_name: str) -> Path:
    """Returns the path to a specific profile .env file."""
    if not profile_name.endswith(".env"):
        profile_name = f"{profile_name}.env"
    return PROFILES_DIR / profile_name

def save_config(configs: dict[str, str], profile_name: str = "main_profile") -> str:
    """Saves multiple configuration keys to a specific profile file."""
    ensure_dirs()
    profile_path = get_profile_path(profile_name)
    
    # Ensure file exists
    if not profile_path.exists():
        profile_path.touch()
            
    for key, value in configs.items():
        set_key(str(profile_path), key, str(value))
        
    return str(profile_path)

def activate_profile(profile_name: str) -> bool:
    """Copies a profile file to the main global .env location."""
    profile_path = get_profile_path(profile_name)
    if not profile_path.exists():
        return False
    
    ensure_dirs()
    shutil.copy(profile_path, ACTIVE_CONFIG_FILE)
    return True

def list_profiles() -> List[str]:
    """Returns a list of available profile names."""
    if not PROFILES_DIR.exists():
        return []
    # Return stem (filename without extension)
    return [f.stem for f in PROFILES_DIR.glob("*.env")]

def get_global_config_path() -> Optional[str]:
    """Returns the main global active config path if it exists."""
    if ACTIVE_CONFIG_FILE.exists():
        return str(ACTIVE_CONFIG_FILE)
    return None
