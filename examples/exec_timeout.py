"""Example shows using exec (or anything) with timeout via signal.alarm."""
from textwrap import dedent
import signal
import time


def timeout_handler(signum, frame):
    raise TimeoutError


def execute_with_timeout(code, timeout):
    signal.signal(signal.SIGALRM, timeout_handler)  # Set the timeout handler
    signal.alarm(timeout)  # Set the alarm for the specified timeout

    result = None
    try:
        result = exec(code)  # Execute the code
    except TimeoutError:
        print("Execution timed out!")
    finally:
        signal.alarm(0)  # Cancel the alarm

    return result


def main():
    code_str = dedent("""
    print('starting function')
    time.sleep(1.5)
    """).strip()

    try:
        print("starting A...")
        start = time.time()
        _ = execute_with_timeout(code_str, timeout=2)
        end = time.time()
        print(f"Execution A completed in {end - start} seconds")
        print("starting B...")
        start = time.time()
        _ = execute_with_timeout(code_str, timeout=1)
        end = time.time()
        print(f"Execution B completed in {end - start} seconds")
        # Process the result if execution completes successfully
    except TimeoutError:
        end = time.time()
        print(f"Execution timed out after {end - start} seconds")
        # Handle the timeout appropriately
    except Exception as e:
        print(f"A different error occurred: {e}")
        # Handle other potential errors


if __name__ == '__main__':
    main()
