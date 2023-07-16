from flask import Blueprint, request, render_template

main = Blueprint("main", __name__)

from .. import models  # noqa
from ..tasks import add_together, block, process, add
from celery.result import AsyncResult

@main.route("/")
def index() -> str:
    return render_template("index.html")

@main.post("/add")
def start_add() -> dict[str, object]:
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = add_together.delay(a, b)
    return {"result_id": result.id}


@main.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
    
@main.post("/add")
def add() -> dict[str, object]:
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = add.delay(a, b)
    return {"result_id": result.id}
    
    
@main.post("/block")
def block() -> dict[str, object]:
    result = block.delay()
    return {"result_id": result.id}


@main.post("/process")
def process() -> dict[str, object]:
    result = process.delay(total=request.form.get("total", type=int))
    return {"result_id": result.id}