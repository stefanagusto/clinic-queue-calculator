from dataclasses import dataclass
import heapq
from typing import List


@dataclass
class Doctor:
    """
    Represents a doctor with a fixed (average) consultation time in minutes.
    """
    avg_time: float


def estimated_wait_time(doctors: List[Doctor], position_in_queue: int) -> float:
    """
    Compute the patient's estimated waiting time (minutes) until they START being seen.

    Assumptions:
    - All doctors are available (idle) at t=0.
    - No doctor preference; each patient goes to whichever doctor frees first.
    - Consultation times are deterministic and equal to each doctor's avg_time.
    - position_in_queue is 1-based (1 means the next patient to enter a room).
    """
    if position_in_queue <= 0:
        raise ValueError("position_in_queue must be >= 1")
    if not doctors:
        raise ValueError("doctors list must not be empty")

    m = len(doctors)

    # If our patient is within the first m, they start immediately at t=0.
    if position_in_queue <= m:
        return 0.0

    # Min-heap of (next_free_time, doctor_index). All doctors start free at t=0.
    heap = [(0.0, idx) for idx in range(m)]
    heapq.heapify(heap)

    # Assign all patients AHEAD of the target.
    for _ in range(position_in_queue - 1):
        next_free, idx = heapq.heappop(heap)
        next_free += doctors[idx].avg_time  # occupy this doctor until this time
        heapq.heappush(heap, (next_free, idx))

    # The earliest next_free_time after assigning those patients is when our patient starts.
    return heap[0][0]


def read_int(prompt: str, min_value: int = None) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value is not None and value < min_value:
                print(f"Please enter an integer >= {min_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def read_float(prompt: str, min_value: float = None) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if min_value is not None and value < min_value:
                print(f"Please enter a number >= {min_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def main():
    print("=== Clinic Queue ETA Calculator ===")
    print("Assumptions: all doctors are idle at t=0, no doctor preference, deterministic avg times.\n")

    num_doctors = read_int("Number of doctors: ", min_value=1)
    doctors: List[Doctor] = []

    for i in range(1, num_doctors + 1):
        avg = read_float(f"Average consultation time for Doctor #{i} (minutes): ", min_value=0.0)
        doctors.append(Doctor(avg_time=avg))

    print("\nNOTE: Position in queue is 1-based (1 means the next patient to be seen).")
    pos = read_int("Enter YOUR position in the queue: ", min_value=1)

    eta = estimated_wait_time(doctors, pos)
    print(f"\nEstimated waiting time until you START: {eta:.2f} minutes")


if __name__ == "__main__":
    main()
