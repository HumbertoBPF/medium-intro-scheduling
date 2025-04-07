import heapq

from common.job import Job
from common.plotter import Plotter


class ShortestJobFirst(Plotter):
    def __init__(self):
        super().__init__()
        self.job_queue = []

    def add_job(self, job: Job):
        """
        Adds a job to the scheduler
        :param job: must be a tuple (execution_time, job_id, color)
        :return:
        """
        heapq.heappush(self.job_queue, (job.execution_time, job))

    def run(self):
        while len(self.job_queue) > 0:
            execution_time, running_job = heapq.heappop(self.job_queue)
            running_job.run(delta_t=running_job.execution_time)
            self._update_plot(delta_t=running_job.execution_time, plot_color=running_job.color, idle=False)
            self.t += execution_time

        self._plot_scheduling()


if __name__ == '__main__':
    scheduler = ShortestJobFirst()
    scheduler.add_job(Job("A", 30, 'red'))
    scheduler.add_job(Job("B", 5, 'blue'))
    scheduler.add_job(Job("C", 5, 'green'))
    scheduler.run()
