from flask import Flask,request,jsonify
from main import gen_plot
import base64
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def main():
    data = request.json
    name = data["name"]
    data = data["data"]
    fig = gen_plot(data,name)
    buffer = BytesIO()
    fig.savefig(buffer,format="png",dpi=300)
    buffer.seek(0)
    data = base64.b64encode(buffer.read()).decode("utf-8")
    return f'<img src="data:image/png;base64,{data}"/>'
