from app import app

import os
print(os.environ.get("SERVER"))
if __name__ == "__main__":
    app.run(debug=True)

