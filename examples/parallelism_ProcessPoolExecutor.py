from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import datetime
from time import sleep


class Timer:
    def __init__(self, message):
        self._message = message

    def __enter__(self):
        print(f'Started: {self._message}')
        self._start = datetime.datetime.now()
        return self

    def __exit__(self, *args):
        self._end = datetime.datetime.now()
        self._interval = self._end - self._start
        message = f"Finished ({self._interval.total_seconds():.2f} seconds)"
        print(message)


def score(param1, param2):
    sleep(2)
    return (param1, param2)


def main():
    parameters1 = [1, 2, 3, 4]
    parameters2 = ['a', 'b', 'c', 'd']

    num_cpus = multiprocessing.cpu_count()
    use_cpus = num_cpus - 1
    print(f"Available CPUs: {num_cpus}; Will Use: {use_cpus}")

    # Non-Parallel
    with Timer("Example - Non-Parallel (for loop)"):
        for i in range(0, len(parameters1)):
            print(score(parameters1[i], parameters2[i]))

    # Parallel
    with ProcessPoolExecutor(max_workers=use_cpus) as executor, Timer("Example - Parallel"):
        results = list(executor.map(score, parameters1, parameters2))
        print(results)


if __name__ == '__main__':
    main()
