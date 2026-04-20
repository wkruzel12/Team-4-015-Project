"""Application entry point for the Bistro Burnett web app."""

import os

from bistro_burnett_web.app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), debug=True)
