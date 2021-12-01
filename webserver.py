from quart import Quart

app = Quart("webserver")

@app.route("/")
async def home():
    return "Hi!"
