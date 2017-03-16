#!/usr/bin/env python3
"""scheduler-circus — FCFS, SJF, Round Robin CPU scheduling demos."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Process:
    name: str
    arrival: int
    burst: int


@dataclass
class Done:
    name: str
    waiting: int
    turnaround: int


def fcfs(procs: List[Process]) -> List[Done]:
    ordered = sorted(procs, key=lambda p: (p.arrival, p.name))
    t = 0
    out: List[Done] = []
    for p in ordered:
        if t < p.arrival:
            t = p.arrival
        wait = t - p.arrival
        t += p.burst
        out.append(Done(p.name, wait, wait + p.burst))
    return out


def sjf(procs: List[Process]) -> List[Done]:
    remaining = procs[:]
    t = 0
    out: List[Done] = []
    while remaining:
        ready = [p for p in remaining if p.arrival <= t]
        if not ready:
            t = min(p.arrival for p in remaining)
            continue
        p = min(ready, key=lambda x: (x.burst, x.arrival, x.name))
        remaining.remove(p)
        wait = t - p.arrival
        t += p.burst
        out.append(Done(p.name, wait, wait + p.burst))
    return out


def round_robin(procs: List[Process], quantum: int) -> List[Done]:
    from collections import deque

    jobs = {p.name: {"arrival": p.arrival, "left": p.burst, "burst": p.burst} for p in procs}
    q = deque()
    t = 0
    arrived = set()
    done: dict[str, Done] = {}

    def enqueue_arrivals():
        for p in procs:
            if p.name not in arrived and p.arrival <= t:
                q.append(p.name)
                arrived.add(p.name)

    enqueue_arrivals()
    if not q:
        t = min(p.arrival for p in procs)
        enqueue_arrivals()

    while len(done) < len(procs):
        if not q:
            t = min(p.arrival for p in procs if p.name not in done and p.name not in arrived)
            enqueue_arrivals()
            continue
        name = q.popleft()
        job = jobs[name]
        run = min(quantum, job["left"])
        t += run
        job["left"] -= run
        enqueue_arrivals()
        if job["left"] == 0:
            turnaround = t - job["arrival"]
            waiting = turnaround - job["burst"]
            done[name] = Done(name, waiting, turnaround)
        else:
            q.append(name)
    return [done[p.name] for p in procs]


def report(title: str, results: List[Done]) -> None:
    print(f"\n== {title} ==")
    print(f"{'proc':<8} {'wait':>6} {'tat':>6}")
    for r in results:
        print(f"{r.name:<8} {r.waiting:6d} {r.turnaround:6d}")
    avg_w = sum(r.waiting for r in results) / len(results)
    avg_t = sum(r.turnaround for r in results) / len(results)
    print(f"{'avg':<8} {avg_w:6.2f} {avg_t:6.2f}")


DEFAULT = [
    Process("P1", 0, 5),
    Process("P2", 1, 3),
    Process("P3", 2, 8),
    Process("P4", 3, 6),
]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--quantum", type=int, default=2)
    args = p.parse_args()
    print("processes:", [(x.name, x.arrival, x.burst) for x in DEFAULT])
    report("FCFS", fcfs(DEFAULT))
    report("SJF (non-preemptive)", sjf(DEFAULT))
    report(f"Round Robin q={args.quantum}", round_robin(DEFAULT, args.quantum))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
