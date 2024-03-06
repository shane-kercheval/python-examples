"""Example shows using exec (or anything) with timeout via signal.alarm."""
from textwrap import dedent
import signal
import time


def __timeout_handler(signum, frame):  # noqa
    raise TimeoutError()


def exec_timeout(code: str, namespace: dict | None = None, timeout: int = 5) -> object:
    """
    Execute code with a timeout. If the code takes longer than the timeout, a TimeoutError is
    raised.
    """
    signal.signal(signal.SIGALRM, __timeout_handler)
    signal.alarm(timeout)
    namespace = namespace or {}
    try:
        exec(code, namespace)
        return namespace
    finally:
        # Cancel the alarm
        signal.alarm(0)


def main():
    code_str = dedent("""
    import time
    print('sleeping 1.5 seconds...')
    time.sleep(1.5)
    my_result = 'done sleeping'
    """).strip()

    # Timeout of 2 seconds should complete successfully
    print(f"starting A with timeout of 2 seconds...")
    namespace = {}
    start = time.time()
    namespace = exec_timeout(code=code_str, namespace=namespace, timeout=2)
    end = time.time()
    assert namespace['my_result'] == 'done sleeping'
    print(f"Execution A completed in {end - start} seconds")

    # Timeout of 1 second should raise a TimeoutError
    print(f"starting B with timeout of 1 second...")
    namespace = {'my_result': 'should not be set'}
    start = time.time()
    try:
        _ = exec_timeout(code=code_str, namespace=namespace, timeout=1)
        assert False, "Execution B should have timed out"
    except TimeoutError:
        end = time.time()
        print(f"Execution B timed out after {end - start} seconds")
    assert namespace['my_result'] == 'should not be set'


if __name__ == '__main__':
    main()
