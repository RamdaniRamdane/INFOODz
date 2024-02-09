from flask import url_for
from website import create_app 



rey = create_app()

if __name__ == "__main__":
    rey.run(debug=True, port=5001)
    
#5449000214911