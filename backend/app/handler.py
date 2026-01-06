from mangum import Mangum
from app.main import app

# Simple handler - let Mangum handle everything
handler = Mangum(app, lifespan="off")