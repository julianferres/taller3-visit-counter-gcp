from locust import HttpUser, task, between
from common.utils import *


class QuickstartUser(HttpUser):
    wait_time = between(10, 50)

    @task
    def home(self):
        page = "jobs"
        self.client.get(f"/webapp?page={page}")
        # get_resources(self.client, page)
        post_visit_and_get_counter(self.client, page)
