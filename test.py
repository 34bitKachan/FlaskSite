from flask import Flask, make_response

app = Flask(__name__)

@app.route('/custom_response')
def custom_response():
    response = make_response("Это пользовательский ответ", 200)
    response.headers["X-Custom-Header"] = "MyHeaderValue"
    response.headers["Pidor"] = "You"

    response.set_cookie("test_cookie", "test_value", max_age=60)
    return response

if __name__ == '__main__':
    app.run(debug=True)