# Scheduler Circus

CPU scheduling demos in Python: FCFS, non-preemptive SJF, and Round Robin.

## Run

```bash
python3 circus.py
python3 circus.py --quantum 3
```

## Metrics

For each algorithm the script prints per-process waiting time and turnaround time, plus averages.

Default workload:

| Process | Arrival | Burst |
|---------|---------|-------|
| P1 | 0 | 5 |
| P2 | 1 | 3 |
| P3 | 2 | 8 |
| P4 | 3 | 6 |

## License

MIT
