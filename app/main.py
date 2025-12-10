import inject
import uvicorn
from fastapi import FastAPI
from max_core.application import setup_max_core
from app.bindings import AppBindings
from app.module import init_custom_module
from app.utils import load_config

# Load configuration and version info
config = load_config("app.conf")

# Configure dependency injection
inject.configure_once(AppBindings(config), allow_override=True)

# Create FastAPI app
app = FastAPI(
  title="your-app"
)

# Register max-core and other modules
setup_max_core(app, config)
init_custom_module(app)

# Entrypoint for running with Uvicorn
uvicorn.run(app, host="0.0.0.0", port=8006)