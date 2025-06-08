from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio


from src.api.scheduler.tasks import update_cb_rates_task, update_tb_bitc_rates_task

scheduler = AsyncIOScheduler()


# def schedule_jobs():
#     print("Вызов schedule_jobs()")
#     def job_wrapper():
#         asyncio.create_task(update_cb_rates_task())
#
#     scheduler.add_job(
#         job_wrapper,
#         IntervalTrigger(hours=24),
#         id="update_rates_cb",
#         replace_existing=True
#     )
#
#     def job_wrapper_2():
#         print("перед Запуск update_tb_bitc_rates_task")
#         asyncio.create_task(update_tb_bitc_rates_task())
#         print("Запуск update_tb_bitc_rates_task")
#
#     scheduler.add_job(
#         job_wrapper_2,
#         IntervalTrigger(seconds=15), #  поменять на час
#         id="update_rates_tb_bt",
#         replace_existing=True
#     )

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

