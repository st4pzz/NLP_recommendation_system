from fastapi import FastAPI, Query
import os
import uvicorn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scripts import get_clean_dataset,get_clean_query

app = FastAPI()

@app.get("/hello")
def read_hello():
    return {"message": "hello world"}

@app.get("/query")
def query_route(query: str = Query(..., description="Search query")):
    query = get_clean_query(query)
    data = get_clean_dataset()

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data["Lyrics"])
    Q = vectorizer.transform([query])
    R = X @ Q.T
    R = R.toarray().flatten()
    idx = R.argsort()[-10:][::-1]
    lista = []
    for i in idx:
        dici = {}
        dici['title'] = data.iloc[i]["Song Name"]
        dici['content'] = data.iloc[i]["Lyrics"]
        dici['relevance'] = R[i] 
        lista.append(dici)


    return {"results": lista, "message": "OK"}

def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()