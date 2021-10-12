import math
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
from common.utils import *


class UserTasks(TaskSet):
    @task
    def home(self):
        page = "about_legals"
        self.client.get(f"/webapp?page={page}")
        # get_resources(self.client, page)
        post_visit_and_get_counter(self.client, page)


class WebsiteUser(HttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]


class StepLoadShape(LoadTestShape):
    """
    A step load shape


    Keyword arguments:

        step_time -- Time between steps
        step_load -- User increase amount at each step
        spawn_rate -- Users to stop/start per second at every step
        time_limit -- Time limit in seconds

    """

    step_time = 30
    step_load = 10
    spawn_rate = 10
    time_limit = 300

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return current_step * self.step_load, self.spawn_rate
