from flask import Flask, jsonify

app = Flask("Reto")
app.config['SECRET_KEY'] = 2892877294823786928736844

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
