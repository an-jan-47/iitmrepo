from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import csv

app = FastAPI()

# CORS: allow ANY origin (GET only is enough)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_FILE = "q-fastapi.csv"


def load_students():
    students = []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"]
            })
    return students


@app.get("/api")
def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    students = load_students()

    if class_:
        students = [s for s in students if s["class"] in class_]

    return {"students": students}
