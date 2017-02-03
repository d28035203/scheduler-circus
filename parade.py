#!/usr/bin/env python3
"""process-parade — toy CPU schedulers for OS lab (2017)."""

from __future__ import print_function


def fcfs(burst):
 """First Come First Served. Waiting time grows like lab queues."""
 n = len(burst)
 wait = [0] * n
 for i in range(1, n):
 wait[i] = wait[i - 1] + burst[i - 1]
 return wait


def sjf(burst):
 """Non-preemptive Shortest Job First."""
 order = sorted(range(len(burst)), key=lambda i: burst[i])
 wait = [0] * len(burst)
 t = 0
 for i in order:
 wait[i] = t
 t += burst[i]
 return wait


def avg(xs):
 return sum(xs) / float(len(xs)) if xs else 0.0


def demo():
 burst = [5, 3, 8, 6]
 print("burst times:", burst)
 w = fcfs(burst)
 print("FCFS wait:", w, "avg=%.2f" % avg(w))
 w = sjf(burst)
 print("SJF wait:", w, "avg=%.2f" % avg(w))


if __name__ == "__main__":
 demo()
