import math
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
    wait_time = constant(1)
    tasks = [UserTasks]


class DoubleWave(LoadTestShape):
    """
    A shape to immitate some specific user behaviour. In this example, midday
    and evening meal times. First peak of users appear at time_limit/3 and
    second peak appears at 2*time_limit/3

    Settings:
        min_users -- minimum users
        peak_one_users -- users in first peak
        peak_two_users -- users in second peak
        time_limit -- total length of test
    """

    min_users = 10
    peak_one_users = 40
    peak_two_users = 40
    time_limit = 600

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = (
                (self.peak_one_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                + (self.peak_two_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                + self.min_users
            )
            return round(user_count), round(user_count)
        else:
            return None
