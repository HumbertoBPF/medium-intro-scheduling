import heapq

from common.job import Job
from common.plotter import Plotter

TIME_INTERRUPT = 1


class ShortestTimeToCompletionFirst(Plotter):
    def __init__(self):
        super().__init__()
        self.job_queue = []

    def _run_shortest_time_to_completion_job(self):
        """
        This method runs the job with the shortest time to completion if the job queue is not empty. If there is no
        job to be run, it only updates the scheduling plot and the timer.
        :return:
        """
        # Check if there is work to be done
        idle = len(self.job_queue) == 0

        if idle:
            self._update_plot(delta_t=TIME_INTERRUPT, plot_color="white", idle=True)
            self.t += TIME_INTERRUPT
            return

        # Get the job with the lowest time to completion
        time_to_completion, running_job = heapq.heappop(self.job_queue)

        # Time that the OS will spend to run the job
        delta_t = min(time_to_completion, TIME_INTERRUPT)

        running_job.run(delta_t=delta_t)

        self._update_plot(delta_t=delta_t, plot_color=running_job.color, idle=False)

        self.t += delta_t
        remaining_time = time_to_completion - delta_t

        # Put the job back to the queue if it has not completed yet
        if remaining_time > 0:
            heapq.heappush(self.job_queue, (remaining_time, running_job))

    def run_jobs(self, jobs: list[Job]):
        """
        This method simulates how the schedule executes the provided list of jobs.
        :param jobs: a list of jobs to be executed
        :return:
        """
        self.t = 0

        # Sorting the jobs decreasingly by arriving time ensures they are added in order to the scheduler
        jobs.sort(key=lambda job: -job.arriving_time)

        while len(jobs) > 0 or len(self.job_queue) > 0:
            while len(jobs) > 0 and jobs[-1].arriving_time == self.t:
                heapq.heappush(self.job_queue, (jobs[-1].execution_time, jobs[-1]))
                jobs.pop()

            self._run_shortest_time_to_completion_job()

        self._plot_scheduling()


if __name__ == '__main__':
    scheduler = ShortestTimeToCompletionFirst()
    job_a = Job(job_id="A", execution_time=30, color="red", arriving_time=0)
    job_b = Job(job_id="B", execution_time=5, color="blue", arriving_time=5)
    job_c = Job(job_id="C", execution_time=5, color="green", arriving_time=5)
    scheduler.run_jobs(jobs=[job_a, job_b, job_c])
