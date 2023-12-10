from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    post_codes = [
        "W1T-7HA",
        "SY7 9AA ",
        "DA6 8HD",
        "CM132QQ",
        "SW7 4AA",
        "EH14 4BB",
        "KY4 9EW",
        "FY5 3JB",
        "DE11 8AX",
        "OL8 4AE",
        "SL6 9JR",
        "SP6 2NJ",
        "INVALID1",
        "INVALID2",
        "INVALID3",
    ]
    strict = [True, False]

    @task
    def validate(self):
        headers = {"X-Correlation-Id": "abc"}
        params = {
            "post_code": random.choice(self.post_codes),
            "strict": random.choice(self.strict)
        }
        self.client.post("/v1/validate", json=params, headers=headers)