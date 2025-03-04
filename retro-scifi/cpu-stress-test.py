#!/usr/bin/env python3
"""
CPU Core Stress Tester - For testing Conky CPU visualizations
"""

import os
import time
import argparse
import multiprocessing
from multiprocessing import Process
import psutil


def stress_core(core_id, duration, intensity):
    """
    Stress a specific CPU core with the given intensity for the specified duration
    """
    # Assign this process to the specific core
    p = psutil.Process(os.getpid())
    p.cpu_affinity([core_id])

    print(f"Stressing Core {core_id} for {duration} seconds at {intensity}% intensity")

    end_time = time.time() + duration

    # Main stress loop
    while time.time() < end_time:
        # Work phase
        work_start = time.time()
        work_duration = (time.time() - work_start) + (intensity / 100.0)

        # Burn CPU cycles
        while (time.time() - work_start) < work_duration:
            # Intensive computation to stress the CPU
            x = 0
            for i in range(10000):
                x += i * i

        # Sleep phase (for lower intensities only)
        if intensity < 100:
            sleep_duration = (time.time() - work_start) * ((100 - intensity) / intensity)
            time.sleep(max(0, min(sleep_duration, 0.1)))  # Cap max sleep to avoid long pauses

    print(f"Core {core_id} stress test complete.")


def run_stress_pattern(pattern, duration=10, intensity=80):
    """
    Run a specific stress pattern on the CPU cores
    pattern options: 'all', 'alternating', 'even', 'odd', 'first-half', 'second-half',
                     or a comma-separated list of core numbers
    """
    # Get the number of cores
    core_count = multiprocessing.cpu_count()
    cores_to_stress = []

    if pattern == "all":
        cores_to_stress = list(range(core_count))
    elif pattern == "alternating":
        cores_to_stress = list(range(0, core_count, 2))
    elif pattern == "even":
        cores_to_stress = list(range(1, core_count, 2))
    elif pattern == "odd":
        cores_to_stress = list(range(0, core_count, 2))
    elif pattern == "first-half":
        cores_to_stress = list(range(core_count // 2))
    elif pattern == "second-half":
        cores_to_stress = list(range(core_count // 2, core_count))
    else:
        # Parse comma-separated list
        try:
            cores_to_stress = [int(core.strip()) for core in pattern.split(",")]
            # Ensure all core IDs are valid
            cores_to_stress = [c for c in cores_to_stress if 0 <= c < core_count]
        except ValueError:
            print(f"Error: Invalid core list format '{pattern}'. Using 'all' instead.")
            cores_to_stress = list(range(core_count))

    if not cores_to_stress:
        print("No cores selected for stress testing.")
        return

    print(f"Starting stress test on cores: {cores_to_stress}")
    print(f"Duration: {duration} seconds, Intensity: {intensity}%")

    # Start processes for each core
    processes = []
    for core in cores_to_stress:
        p = Process(target=stress_core, args=(core, duration, intensity))
        p.start()
        processes.append(p)

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("All stress tests completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CPU Core Stress Tester")
    parser.add_argument(
        "--pattern",
        "-p",
        default="all",
        help="Stress pattern: 'all', 'alternating', 'even', 'odd', 'first-half', 'second-half', or comma-separated list of core IDs",
    )
    parser.add_argument("--duration", "-d", type=int, default=10, help="Duration of stress test in seconds")
    parser.add_argument("--intensity", "-i", type=int, default=80, help="CPU load intensity (0-100%%)")

    args = parser.parse_args()

    run_stress_pattern(args.pattern, args.duration, args.intensity)
