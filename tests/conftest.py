import pytest
import time
from pathlib import Path

# Dictionary to store timing per file
file_times = {}
file_start_times = {}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    """Track timing for each test file."""
    file_path = str(Path(item.fspath).name)
    
    # Start timing if this is the first test in the file
    if file_path not in file_start_times:
        file_start_times[file_path] = time.time()
    
    yield
    
    # If this is the last test in the file (nextitem is None or different file)
    if nextitem is None or str(Path(nextitem.fspath).name) != file_path:
        elapsed = time.time() - file_start_times[file_path]
        file_times[file_path] = elapsed

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Display per-file timing summary."""
    terminalreporter.write_sep("=", "test file durations")
    
    # Sort by duration (longest first)
    sorted_files = sorted(file_times.items(), key=lambda x: x[1], reverse=True)
    
    total_time = sum(file_times.values())
    
    for file_name, duration in sorted_files:
        terminalreporter.write_line(f"{duration:>8.4f}s  {file_name}")
    
    terminalreporter.write_sep("-", f"total: {total_time:.4f}s")