import queue

from common.job import Job
from common.plotter import Plotter


class FirstInFirstOutScheduler(Plotter):
    def __init__(self):
        super().__init__()
        self.job_queue = queue.Queue()

    def add_job(self, job: Job):
        self.job_queue.put(job)

    def run(self):
        while not self.job_queue.empty():
            running_job = self.job_queue.get()
            running_job.run(delta_t=running_job.execution_time)
            self._update_plot(delta_t=running_job.execution_time, plot_color=running_job.color, idle=False)
            self.t += running_job.execution_time

        self._plot_scheduling()


if __name__ == '__main__':
    scheduler = FirstInFirstOutScheduler()
    scheduler.add_job(Job("A", 30, 'red'))
    scheduler.add_job(Job("B", 5, 'blue'))
    scheduler.add_job(Job("C", 5, 'green'))
    scheduler.run()
