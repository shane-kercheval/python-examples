import time
import asyncio


async def task(name, delay):
    print(f"Task {name} starting with a delay of {delay} seconds")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")
    return f"Result of task {name}"


async def main():
    # Creating multiple asynchronous tasks
    task1 = asyncio.create_task(task("One", 3))
    task2 = asyncio.create_task(task("Two", 2))
    task3 = asyncio.create_task(task("Three", 1))

    # Waiting for all tasks to complete
    results = await asyncio.gather(task1, task2, task3)
    print("\nAll tasks completed")
    for result in results:
        print(result)


# Run the main function
start = time.time()
asyncio.run(main())
end = time.time()
print(f"Total time: {end - start:.2f} seconds")
