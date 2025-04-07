from typing import List

from common.job import Job
from common.plotter import Plotter

TIME_INTERRUPT = 1


class RoundRobinScheduler(Plotter):
    def __init__(self):
        super().__init__()
        self.jobs = []
        self.current_job_index = 0

    def _run_job(self):
        """
        This method runs the job with the shortest time to completion if the job queue is not empty. If there is no
        job to be run, it only updates the scheduling plot and the timer.
        :return:
        """
        if len(self.jobs) == 0:
            self._update_plot(delta_t=TIME_INTERRUPT, plot_color="white", idle=True)
            self.t += TIME_INTERRUPT
            return

        current_job, time_to_completion = self.jobs[self.current_job_index]

        # Time that the OS will spend to run the job
        delta_t = min(time_to_completion, TIME_INTERRUPT)

        current_job.run(delta_t=delta_t)

        self._update_plot(delta_t=delta_t, plot_color=current_job.color, idle=False)
        self.t += delta_t

        time_to_completion -= delta_t

        # If the job completed, remove it from the scheduler
        if time_to_completion <= 0:
            del self.jobs[self.current_job_index]
        # Otherwise, update its completion time
        else:
            self.jobs[self.current_job_index] = (current_job, time_to_completion)

        # Move to the next job
        self.current_job_index -= 1

        if self.current_job_index < 0:
            self.current_job_index = len(self.jobs) - 1

    def run_jobs(self, jobs: List[Job]):
        """
        This method simulates how the schedule executes the provided list of jobs.
        :param jobs: a list of jobs to be executed
        :return:
        """
        self.t = 0

        # Sorting the jobs decreasingly by arriving time ensures they are added in order to the scheduler
        jobs.sort(key=lambda job: -job.arriving_time)

        while len(jobs) > 0 or len(self.jobs) > 0:
            while len(jobs) > 0 and jobs[-1].arriving_time == self.t:
                # Incoming job: add it to the scheduler
                self.jobs.append((jobs[-1], jobs[-1].execution_time))
                jobs.pop()

                # Move the pointer to the end of the list such that incoming jobs get scheduled as soon as possible
                self.current_job_index = len(self.jobs) - 1

            self._run_job()

        self._plot_scheduling()


if __name__ == '__main__':
    scheduler = RoundRobinScheduler()
    job_a = Job(job_id="A", execution_time=30, color="red", arriving_time=0)
    job_b = Job(job_id="B", execution_time=5, color="blue", arriving_time=5)
    job_c = Job(job_id="C", execution_time=5, color="green", arriving_time=5)
    scheduler.run_jobs(jobs=[job_a, job_b, job_c])
