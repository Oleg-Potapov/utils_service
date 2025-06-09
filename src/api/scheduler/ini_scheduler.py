from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


from src.api.scheduler.tasks import update_cb_rates_task, update_tb_bitc_rates_task

scheduler = AsyncIOScheduler()


def schedule_jobs():
    print("Вызов schedule_jobs()")

    scheduler.add_job(
        update_cb_rates_task,
        IntervalTrigger(hours=24),
        id="update_rates_cb",
        replace_existing=True
    )

    scheduler.add_job(
        update_tb_bitc_rates_task,
        IntervalTrigger(hours=1),
        id="update_rates_tb_bt",
        replace_existing=True
    )

