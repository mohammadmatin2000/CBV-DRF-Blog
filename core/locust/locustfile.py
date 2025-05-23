from locust import HttpUser, task, between

# ======================================================================================================================
class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        res = self.client.post("/accounts/api/v1/jwt/create/", json={
            "email": "matin20001313@gmail.com",
            "password": "n1387n2008n"
        })

        print("Status Code:", res.status_code)
        print("Response Text:", res.text)

        try:
            data = res.json()
            token = data.get("access")
            if token:
                self.client.headers = {"Authorization": f"Bearer {token}"}
            else:
                print("Access token not found in response:", data)
        except Exception as e:
            print("Failed to parse JSON:", e)
            print("Raw response:", res.text)

    @task
    def list_post(self):
        self.client.get("/api/v1/post/")

    @task
    def list_category(self):
        self.client.get("/api/v1/category/")
# ======================================================================================================================