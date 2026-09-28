main run: `uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8080`

taskiq worker run: `taskiq worker worker:redis_list_queue_broker --workers 1`

TODO - use uuid like primary key instead of int and create full DM and we do not need waiting
id from db. Due to of this repositories should take DM entity instead of DTO`s 