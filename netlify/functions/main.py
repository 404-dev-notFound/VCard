from mangum import Mangum
from main import app  # Your existing FastAPI app

handler = Mangum(app)
