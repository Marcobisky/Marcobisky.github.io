import asyncio
import time

async def task1():
    print("Task 1: Starting")
    await asyncio.sleep(10)
    print("Task 1: Completed")
    
async def task2():
    print("Task 2: Starting")
    await asyncio.sleep(5)
    print("Task 2: Completed")
    
async def do_tasks_async():
    start = time.time()
    
    task1_start = asyncio.create_task(task1())
    task2_start = asyncio.create_task(task2())
    
    print("Arranged two tasks, waiting for complete ...")
    await task1_start
    await task2_start
    
    end = time.time()
    print(f"All tasks completed in {end - start:.1f} seconds")
    
if __name__ == "__main__":
    asyncio.run(do_tasks_async())