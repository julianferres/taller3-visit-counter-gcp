from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
from common.utils import *


class UserTasks(TaskSet):
    @task
    def home(self):
        page = "about"
        self.client.get(f"/webapp?page={page}")
        # get_resources(self.client, page)
        post_visit_and_get_counter(self.client, page)


class WebsiteUser(HttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.

    Keyword arguments:

        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage

        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages = [
        {"duration": 60, "users": 5, "spawn_rate": 10},
        {"duration": 100, "users": 25, "spawn_rate": 10},
        {"duration": 180, "users": 50, "spawn_rate": 10},
        {"duration": 220, "users": 15, "spawn_rate": 10},
        {"duration": 230, "users": 5, "spawn_rate": 10},
        {"duration": 240, "users": 1, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
