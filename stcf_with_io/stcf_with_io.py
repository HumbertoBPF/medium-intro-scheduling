import heapq
from typing import List

from common.job import Job
from common.plotter import Plotter

TIME_INTERRUPT = 1


class ShortestTimeToCompletionFirstWithIO(Plotter):
    def __init__(self):
        # This property stores jobs that will be scheduled in a future moment
        super().__init__()
        self.incoming_jobs = []

        # This property stores jobs that are taken into account by the scheduler
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

        # Update the execution time (which will represent here the remaining time until total completion)
        running_job.execution_time -= delta_t

        # Put the job back to the queue if it has not completed yet
        if remaining_time > 0:
            heapq.heappush(self.job_queue, (remaining_time, running_job))
        # If the job completed, check if there is a pending I/O request
        elif len(running_job.io_requests) > 0:
            # Time that the I/O request will take
            io_request_time = running_job.io_requests[0][1] - running_job.io_requests[0][0]

            # Decrement the execution time of the job by the time taken by the I/O operation
            running_job.execution_time -= io_request_time

            # Remove the I/O operation from the I/O request queue
            running_job.io_requests.popleft()

            # The job must be scheduled again when the I/O operation completes
            running_job.arriving_time = io_request_time + self.t
            self.incoming_jobs.append(running_job)

    def run_jobs(self, jobs: List[Job]):
        """
        This method simulates how the schedule executes the provided list of jobs.
        :param jobs: a list of jobs to be executed
        :return:
        """
        self.t = 0

        # Sorting the jobs decreasingly by arriving time ensures they are added in order to the scheduler
        jobs.sort(key=lambda job: -job.arriving_time)

        self.incoming_jobs = jobs

        while len(self.incoming_jobs) > 0 or len(self.job_queue) > 0:
            while len(self.incoming_jobs) > 0 and self.incoming_jobs[-1].arriving_time == self.t:
                incoming_job = self.incoming_jobs[-1]

                execution_time = incoming_job.execution_time

                # If there is a pending I/O request, compute the completion time of the sub-job
                if len(incoming_job.io_requests) > 0:
                    execution_time = incoming_job.io_requests[0][0] - incoming_job.arriving_time

                heapq.heappush(self.job_queue, (execution_time, incoming_job))
                self.incoming_jobs.pop()

            self._run_shortest_time_to_completion_job()

        self._plot_scheduling()


if __name__ == '__main__':
    scheduler = ShortestTimeToCompletionFirstWithIO()
    job_a = Job(job_id="A", execution_time=10, color="red", arriving_time=0, io_requests=[(4, 6), (8, 10)])
    job_b = Job(job_id="B", execution_time=5, color="blue", arriving_time=0, io_requests=[])
    job_c = Job(job_id="B", execution_time=5, color="green", arriving_time=0, io_requests=[])
    scheduler.run_jobs(jobs=[job_a, job_b, job_c])
