from pathlib import Path

# ------------------------------------------------------------
# Base Directories (resolved from project root)
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]        # /app -> /project root
DATA_DIR = BASE_DIR / "data"

KEY_DIR = DATA_DIR / "keys"
CHAIN_DIR = DATA_DIR / "chain"                        # matches your actual structure
DB_DIR = DATA_DIR / "db"

# Ensure directories exist
KEY_DIR.mkdir(parents=True, exist_ok=True)
CHAIN_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# File Paths
# ------------------------------------------------------------

PRIVATE_KEY_FILE = KEY_DIR / "truetrace_priv.bin"
PUBLIC_KEY_FILE = KEY_DIR / "truetrace_pub.bin"       # matches your existing file
CHAIN_FILE = CHAIN_DIR / "event_chain.json"           # matches your actual file
EVENT_DB_FILE = DB_DIR / "truetrace.db"
