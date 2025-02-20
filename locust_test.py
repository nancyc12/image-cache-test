from locust import HttpUser, task, between
import time

class LargeFileDownloadUser(HttpUser):
    wait_time = between(1, 2)  # Wait time between tasks in seconds

    @task
    def download_large_file(self):
        url = "/oem-share/sutton/bachman/sutton-workstation-2022-10-07/pc-sutton-bachman-focal-amd64-X00-20221004-139.iso"  # Replace with your file path
        start_time = time.time()
        
        with self.client.get(url, stream=True, timeout=120, catch_response=True) as response:
            if response.status_code == 200:
                file_size = 0
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1 MB chunks
                    file_size += len(chunk)  # Count total bytes downloaded

                duration = time.time() - start_time
                response.success()
                print(f"Downloaded {file_size / (1024 * 1024):.2f} MB in {duration:.2f} seconds")
            else:
                response.failure(f"Failed with status code {response.status_code}")
