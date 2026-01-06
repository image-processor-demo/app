from mangum import Mangum
from app.main import app

# Configure Mangum for Lambda with binary response support
handler = Mangum(app, lifespan="off")