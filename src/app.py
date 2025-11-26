from fastapi import FastAPI

app = FastAPI()

@app.route('/autorization')
def authorization():
    pass

@app.route('/tests')
def knowledge_tests():
    pass