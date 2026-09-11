main run: `uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8080`

taskiq worker run: `taskiq worker worker:redis_list_queue_broker --workers 1`