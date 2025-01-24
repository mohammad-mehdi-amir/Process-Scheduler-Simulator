import heapq
import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = None

class Scheduler:
    def __init__(self, context_switch_time=0):
        self.context_switch_time = context_switch_time
        self.time = 0
        self.gantt_chart = []

    def calculate_metrics(self, processes):
        for process in processes:
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            process.response_time = process.response_time if process.response_time is not None else process.waiting_time

    def display_results(self, processes,lable):
        print("PID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\tResponse")
        for process in sorted(processes, key=lambda x: x.pid):
            print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time}\t{process.completion_time}\t{process.turnaround_time}\t{process.waiting_time}\t{process.response_time}")

        self.plot_gantt_chart(lable)

    def plot_gantt_chart(self,lable):
        plt.figure(figsize=(10, 5))
        for process_id, start_time, end_time in self.gantt_chart:
            plt.barh(1, end_time - start_time, left=start_time, edgecolor='black')
            plt.text((start_time + end_time) / 2, 1, f"P{process_id}", ha='center', va='center')

        plt.xlabel("Time")
        plt.yticks([])
        plt.title(f"Gantt Chart, {lable}")
        plt.show()

    def fcfs(self, processes):
        processes.sort(key=lambda x: x.arrival_time)
        self.time = 0

        for process in processes:
            if self.time < process.arrival_time:
                self.time = process.arrival_time

            if self.gantt_chart and self.time != self.gantt_chart[-1][2]:
                self.time += self.context_switch_time

            self.gantt_chart.append((process.pid, self.time, self.time + process.burst_time))
            process.completion_time = self.time + process.burst_time
            self.time += process.burst_time

        self.calculate_metrics(processes)

    def sjf(self, processes):
        processes.sort(key=lambda x: x.arrival_time)
        ready_queue = []
        self.time = 0
        completed = 0

        while completed < len(processes):
            for process in processes:
                if process.arrival_time <= self.time and process not in ready_queue and process.completion_time == 0:
                    heapq.heappush(ready_queue, (process.burst_time, process))

            if ready_queue:
                burst_time, process = heapq.heappop(ready_queue)
                if self.gantt_chart and self.time != self.gantt_chart[-1][2]:
                    self.time += self.context_switch_time

                self.gantt_chart.append((process.pid, self.time, self.time + process.burst_time))
                process.completion_time = self.time + process.burst_time
                self.time += process.burst_time
                completed += 1
            else:
                self.time += 1

        self.calculate_metrics(processes)

    def round_robin(self, processes, time_quantum):
        ready_queue = []
        self.time = 0

        for process in processes:
            process.remaining_time = process.burst_time

        while processes or ready_queue:
            while processes and processes[0].arrival_time <= self.time:
                ready_queue.append(processes.pop(0))

            if ready_queue:
                process = ready_queue.pop(0)
                if process.response_time is None:
                    process.response_time = self.time - process.arrival_time

                exec_time = min(process.remaining_time, time_quantum)
                self.gantt_chart.append((process.pid, self.time, self.time + exec_time))
                process.remaining_time -= exec_time
                self.time += exec_time

                if process.remaining_time > 0:
                    ready_queue.append(process)
                else:
                    process.completion_time = self.time
            else:
                self.time += 1

        self.calculate_metrics(processes)


process_list = [
    Process(1, 0, 8),
    Process(2, 1, 4),
    Process(3, 2, 9),
    Process(4, 3, 5)
]

scheduler = Scheduler(context_switch_time=0)

print("FCFS Scheduling")
scheduler.fcfs(process_list.copy())
scheduler.display_results(process_list,'FCFS')

print("\nSJF Scheduling")
scheduler.sjf(process_list.copy())
scheduler.display_results(process_list,'SJF')

print("\nRound Robin Scheduling")
scheduler.round_robin(process_list.copy(), time_quantum=4)
scheduler.display_results(process_list,'round robin')
