"""Entry point: python run.py or gunicorn run:app."""
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402

env = os.environ.get("FLASK_ENV") or os.environ.get("ENVIRONMENT") or "production"
app = create_app(env)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=(env == "development"), host="0.0.0.0", port=port)
