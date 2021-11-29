from flask import Flask, jsonify
import os

app = Flask("Windmill")
app.config['SECRET_KEY'] = "helloImTheSecretBetYouCantCrackMeLalalalalalWazzupNoQueMuyHacker"
port = int(os.getenv('PORT', 8000))

@app.route('/')
def home() -> str:
    return "This is my quest, to follow that star. No matter how hopeles, no matter how far."

@app.route('/test')
def test() -> str:
    """Test Connection"""
    return "Connection Established"

@app.route('/config')
def config() -> str:
    return "Configuration Successful"

@app.route('/getCars')
def getCars():
    """Get Car Agents"""
    return ""


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)