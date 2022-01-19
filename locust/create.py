from locust import HttpUser, TaskSet, task, between
import time


class AuthorizedUser(TaskSet):
    def login(self):
        with self.client.post("/auth/login", data={"username":"Susan", "password":"Susan"}, catch_response=True) as response:
            if response.status_code < 300:
                response.success()


    # def logout(self):
    #     self.client.get("/auth/logout")

    def on_start(self):
        self.client.get("/index")
        self.login()

    # def on_stop(self):
    #     self.logout()

    @task
    def create(self):
        # time to think up the article(easy article), but it might take more
        time.sleep(15)
        self.client.post("/create_article", \
            data={"header":"The greates ARTICLE EVER!!", "body":"This article is just a test article. Sorry for the clickbait."})
        time.sleep(6)
        self.client.post("/user/Susan", data={"body":"I don't know, it might have been better to user JMeter or something"})

class AuthedUser(HttpUser):
    wait_time = between(2, 6)
    host = "http://localhost:8000"
    tasks = [AuthorizedUser]