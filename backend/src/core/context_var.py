import contextvars

task_uuid_var = contextvars.ContextVar("task_uuid", default="")
