from src import create_app

app = create_app()

@app.route("/hello/user/<username>")
def say_hello(username):
    return f"Hello {username}"



if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0", port=5000)