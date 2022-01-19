from locust import HttpUser, TaskSet, task, between


class AuthorizedUser(TaskSet):
    def login(self):
        with self.client.post("/auth/login", data={"username":"Susan", "password":"Susan"}, catch_response=True) as response:
            if response.status_code < 300:
                response.success()



    def on_start(self):
        self.login()


    @task
    def edit(self):
        self.client.post("/edit_article/3", \
            data={"header":"Pokemon Might be the greates game!", "body":"No comments."})

class AuthedUser(HttpUser):
    wait_time = between(2, 5)
    host = "http://localhost:8000"
    tasks = [AuthorizedUser]