from locust import HttpUser, task, between
import time

class LargeFileDownloadUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def download_large_file(self):
        url = "/oem-share/sutton/bachman/sutton-workstation-2022-10-07/pc-sutton-bachman-focal-amd64-X00-20221004-139.iso"
        headers = {"Host": "tel-image-cache.canonical.com"}

        start_time = time.time()
        with self.client.get(url, headers=headers, stream=True, catch_response=True) as response:
            if response.status_code == 200:
                file_size = 0
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # Process 1MB chunks
                    file_size += len(chunk)  

                duration = time.time() - start_time
                response.success()
                print(f"Downloaded {file_size / (1024 * 1024):.2f} MB in {duration:.2f} seconds")
            else:
                response.failure(f"Failed with status {response.status_code}")
