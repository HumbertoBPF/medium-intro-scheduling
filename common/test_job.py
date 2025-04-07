import uuid

import pytest

from common.job import Job


@pytest.mark.parametrize("execution_time, arriving_time, io_requests, error", [
    (30, 10, [(5, 15), (30, 40)], "Invalid lower bound: 5"),
    (30, 10, [(15, 25), (35, 45)], "Invalid upper bound: 45"),
    (30, 10, [(15, 25), (30, 30)], "Invalid interval: (30, 30)"),
    (30, 10, [(15, 25), (35, 30)], "Invalid interval: (35, 30)"),
    (30, 10, [(15, 25), (20, 30)], "Overlapping I/O requests: (15, 25) and (20, 30)"),
    (-1, 10, [(15, 25), (20, 30)], "The execution time of a job must be positive"),
    (0, 10, [(15, 25), (20, 30)], "The execution time of a job must be positive"),
    (30, -1, [(15, 25), (20, 30)], "The arriving time of a job must be non-negative"),
])
def test_job_constructor_validations(execution_time, arriving_time, io_requests, error):
    """Validations of Job class attributes"""
    with pytest.raises(AttributeError) as e:
        Job(
            job_id=str(uuid.uuid4()),
            execution_time=execution_time,
            color="red",
            arriving_time=arriving_time,
            io_requests=io_requests,
        )
    assert str(e.value) == error


@pytest.mark.parametrize("execution_time, arriving_time, io_requests, expected_io_requests", [
    (30, 10, [(15, 20), (32, 37), (23, 28)], [(15, 20), (23, 28), (32, 37)]),
    (30, 0, [(5, 15), (27, 29), (20, 23)], [(5, 15), (20, 23), (27, 29)]),
    (30, 5, [], []),
])
def test_job_constructor(execution_time, arriving_time, io_requests, expected_io_requests):
    """Successful initialization of a JobSTCFWithIO instance"""
    random_uuid = str(uuid.uuid4())

    job = Job(
        job_id=random_uuid,
        execution_time=execution_time,
        color="red",
        arriving_time=arriving_time,
        io_requests=io_requests,
    )

    assert job.job_id == random_uuid
    assert job.execution_time == execution_time
    assert job.arriving_time == arriving_time
    assert job.color == "red"
    assert job.io_requests == expected_io_requests
