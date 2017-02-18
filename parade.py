#!/usr/bin/env python3
"""process-parade — toy CPU schedulers for OS lab (2017)."""

from __future__ import print_function


def fcfs(burst):
 n = len(burst)
 wait = [0] * n
 for i in range(1, n):
 wait[i] = wait[i - 1] + burst[i - 1]
 return wait


def sjf(burst):
 order = sorted(range(len(burst)), key=lambda i: burst[i])
 wait = [0] * len(burst)
 t = 0
 for i in order:
 wait[i] = t
 t += burst[i]
 return wait


def round_robin(burst, quantum=2):
 """Classic RR. Quantum too small = context-switch festival."""
 n = len(burst)
 rem = list(burst)
 wait = [0] * n
 t = 0
 done = 0
 while done < n:
 progress = False
 for i in range(n):
 if rem[i] <= 0:
 continue
 progress = True
 slice_t = min(quantum, rem[i])
 rem[i] -= slice_t
 t += slice_t
 if rem[i] == 0:
 wait[i] = t - burst[i]
 done += 1
 if not progress:
 break
 return wait


def avg(xs):
 return sum(xs) / float(len(xs)) if xs else 0.0


def demo():
 burst = [5, 3, 8, 6]
 print("burst times:", burst)
 for name, w in [
 ("FCFS", fcfs(burst)),
 ("SJF ", sjf(burst)),
 ("RR2 ", round_robin(burst, 2)),
 ("RR4 ", round_robin(burst, 4)),
 ]:
 print("%s wait=%s avg=%.2f" % (name, w, avg(w)))


if __name__ == "__main__":
 demo()
