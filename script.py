import logging
import requests
import os


# Configure logging to a file
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Get versions from Selenium nested folders
def get_file_content_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                # print(f"File: {file_path}")
                # print("Content:")
                # print(content)
                # print("-" * 30)
                logging.info(f"{file_path} {content}")


# url = "https://www.openai.com"
# response = requests.get(url)

# # Example usage
# def do_something():
#     logging.debug("This is a debug message")
#     logging.info("This is an info message")
#     logging.warning("This is a warning message")
#     logging.error("This is an error message")
#     logging.critical("This is a critical message")

if __name__ == "__main__":
    get_file_content_in_folder('./selenium')
