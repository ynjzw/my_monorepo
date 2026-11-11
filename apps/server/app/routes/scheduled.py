from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

app=APIRouter()
scheduler = AsyncIOScheduler()

def my_task():
    print(f"定时任务执行: {datetime.now()}")

def task2():
    print(f"任务2执行")

# 只负责“把任务添加到调度器”，不启动调度器
def register_jobs():
    trigger1 = CronTrigger(hour=16, minute=0, second=0)
    trigger2 = CronTrigger(hour=11, minute=0, second=0)
    scheduler.add_job(my_task, trigger1, id="my_task")
    scheduler.add_job(task2, trigger2, id="task2")

# 可选：提供一个手动查看任务状态的接口
@app.get("/jobs")
def list_jobs():
    return [{"id": job.id, "next_run": str(job.next_run_time)} for job in scheduler.get_jobs()]