"""Bistro Burnett Web Prototype

Date: April 2026
Authors: Team 4-015
Purpose:
    Start the Flask web server for the Bistro Burnett ordering prototype.
    Input: browser requests sent to the Flask server.
    Output: rendered HTML pages served to the browser.
"""

import os

from bistro_burnett_web.app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), debug=True)
