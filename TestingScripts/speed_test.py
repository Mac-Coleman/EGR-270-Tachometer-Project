import time

t1 = time.time_ns()
t2 = time.time_ns()

print("Time elapsed: " + str(t2 - t1) + " ns")
print("              " + str((t2-t1) / 1000) + " μs")
