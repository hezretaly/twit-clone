from locust import HttpUser, TaskSet, task, between



class AuthorizedUser(TaskSet):
    def login(self):
        # with self.client.post("/auth/login", data='username=Susan&password=Susan&submit=Sign+in', catch_response=True) as response:
        with self.client.post("/auth/login", data={"username":"Susan", "password":"Susan"}, catch_response=True) as response:
            if response.status_code < 300:
                print(response.raw)
                response.success()
            else:
                print("fuck")
                response.fail("no success")


    def logout(self):
        self.client.get("/auth/logout")

    def on_start(self):
        self.login()

    def on_stop(self):
        self.logout()

    @task
    def tweets(self):
        # have to login before visiting explore page
        self.client.get("/explore")

    @task
    def create(self):
        self.client.post("/create_article", data={"header":"The greates ARTICLE EVER!!", "body":"This article is just a test article. Sorry for the clickbait."})

    # # @task
    # # def tweet(self):
    # #     self.client.post()

    # @task
    # def articles(self):
    #     self.client.get("/articles")

    # @task
    # def article(self):
    #     self.client.get("/article/2")

    # @task
    # def sequence1(self):
    #     # with self.client.post("/create_article", data='header=The greates ARTICLE EVER!!&body=This article is just a test article. Sorry for the clickbait.', catch_response=True) as response:
    #     with self.client.post("/create_article", data='header=EVER&body=This', catch_response=True) as response:
    #         if response.status_code < 300:
    #             print(response.status_code, response.history)
    #             response.success()


class UnauthorizedUser(HttpUser):
    wait_time = between(4, 9)

    @task
    def hello_world(self):
        self.client.get("/index")

    # @task
    # def login(self):
    #     data_form = 'username=Susan&password=Susan'
    #     self.client.post("/auth/login", data=data_form)

    # @task
    # def articles(self):
    #     self.client.get("/articles")

class AuthedUser(HttpUser):
    wait_time = between(2, 5)
    # host = "http://localhost:8000"
    tasks = [AuthorizedUser]