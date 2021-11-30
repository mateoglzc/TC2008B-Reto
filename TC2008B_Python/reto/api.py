from flask import Flask, jsonify, session, request
import model
import os

app = Flask("Windmill")
app.config['SECRET_KEY'] = "helloImTheSecretBetYouCantCrackMeLalalalalalWazzupNoQueMuyHacker"
port = int(os.getenv('PORT', 8000))

@app.route('/test', methods=["GET"])
def test() -> str:
    """Test Connection"""
    return "Connection Established"

@app.route('/config', methods=["POST"])
def config() -> str:
    """Recieve model configuration and create model"""
    numCars = int(request.form.get("numCars"))
    session["Model"] = model.CityModel(numCars)
    return "Configuration Successful"

@app.route('/getCars')
def getCars():
    """Get Car Agents"""
    model = session["Model"]
    return jsonify({"Items" : model.getCars()})

@app.route('/getTL')
def getTrafficLights():
    """Get Traffic Lights"""
    model = session["Model"]
    return jsonify({"Items" : model.getTrafficLights()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)