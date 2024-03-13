import re

import requests
import os
import time
import validators

POST_URL = "https://api2.online-convert.com/jobs"
SEND_TEMPLATE = {
    "input": [{
        "type": "remote",
        "source": ""
    }],
    "conversion": [{"target": "txt"}]}
DOCUMENT_ROOT = "."  # configure to where you want to store results
SETTINGS = "config.properties"


class DocumentControl:
    """
    Class used to download Regents exams, convert them from PDF to text, and write a formatted answer file.
    Uses www.api2convert.com to do the conversions.
    """

    def __init__(self, year: str, month: str, subject: str):
        """
        Given a year/month/subject to make a working directory, calling the convert methods with convert PDFs to text.
        """
        # Make a working directory
        self.working_dir = os.path.join(DOCUMENT_ROOT, year + "_" + month + "_" + subject)
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        # Get the conversion key from SETTINGS
        with open(SETTINGS, "r") as in_file:
            for line in in_file.readlines():
                if line.startswith("SECRET_KEY"):
                    self.secret_key = line.split("=")[1].strip()
        print(self.secret_key)
        if self.secret_key is None:
            raise Exception("Could not read the secret key for file conversion!")

    def get_conversion(self, uri: str, suffix: str, download_original: bool = True) -> str:
        """
        Given the URI of a PDF file on the internet, convert it to text.

        :param uri: The URI or URL path of a pdf file to convert
        :param suffix: Any suffix to add to the resulting file to add to the file name
        :param download_original: If to also download the file pointed to by the uri parameter
        :return str: The filepath of the converted file saved locally on success, else empty string
        """
        print("Processing " + uri)
        is_remote_file = validators.url(uri)

        # If to download the original as well
        if is_remote_file and download_original:
            self.__save_file(uri, suffix + ".pdf")

        # Convert the document to text, get back the path
        if is_remote_file:
            file_uri = self.__convert_pdf_remote_src(uri)
        else:
            file_uri = self.__convert_pdf_local_src(uri)

        print("Finished processing!")
        if file_uri != "":
            return self.__save_file(file_uri, suffix + ".txt")

        return ""

    @staticmethod
    def __check_response_errors(json_data: dict) -> bool:
        """
        Given a JSON response, print any errors, and return success state.

        :param json_data: A dictionary blob of json
        :return: A boolean, True if no errors, else False.
        """
        if len(json_data.get("errors", [])) > 0:
            print("ERROR returned!")
            for error in json_data["errors"]:
                print(error)
            return False
        if len(json_data.get("warnings", [])) > 0:
            print("WARNINGS returned!")
            for warn in json_data["errors"]:
                print(warn)
            return False
        return True

    def __digest_response(self, response) -> str:
        """
        Given a response to a file conversion, process it.
        """
        # Only continue if we got a successful response
        if response.status_code in [200, 201, 202]:
            # Check to see if we got any errors
            json_data = response.json()
            if not self.__check_response_errors(json_data):
                return ""
            job_id = json_data["id"]
            job_status = json_data["status"]["code"]
            if job_status not in ["downloading", "processing", "completed"]:
                print("Response status was not expected, got: " + job_status)
                print("More information: " + json_data["status"]["info"])
                return ""
            # They've started processing, grab the job ID to check it
            print("Processing started, waiting to download txt")
            # Wait for the processing to finish (maximum 30 seconds)
            for i in range(30):
                # Request the status
                response = requests.get(POST_URL + "/" + job_id, headers={"X-Oc-Api-Key": self.secret_key})
                if response.status_code != 200:
                    print("Got non-success status code: " + str(response.status_code))
                    print("Response body: " + str(response.content))
                    return ""
                else:
                    json_data = response.json()
                    print("Status: " + json_data["status"]["code"])
                    # If recognized as done, we're good
                    if json_data["status"]["code"] == "completed":
                        print("Job is done, download link: " + json_data["output"][0]["uri"])
                        return json_data["output"][0]["uri"]
                time.sleep(1)
        else:
            print("Returned a non success status: " + str(response.status_code))
            print("Content: " + str(response.content))
        return ""

    def __convert_pdf_remote_src(self, file_path: str) -> str:
        """
        Given a URI file path, run the conversion.

        :param file_path: A URI file path of the converted file
        """
        # Send the post request
        print("Converting: " + file_path)
        body = SEND_TEMPLATE.copy()
        body["input"][0]["source"] = file_path
        response = requests.post(POST_URL, json=body, headers={"X-Oc-Api-Key": self.secret_key})
        return self.__digest_response(response)

    def __convert_pdf_local_src(self, file_path: str) -> str:
        """
        Given a local file path, run the conversion.

        :param file_path: A URI file path of the converted file
        """
        # Send the post request with no input
        print("Converting: " + file_path)
        body = SEND_TEMPLATE.copy()
        body.pop("input")
        response = requests.post(POST_URL, json=body, headers={"X-Oc-Api-Key": self.secret_key})

        # Only continue if we got a successful response
        if response.status_code in [200, 201, 202]:
            # Check to see if we got any errors
            json_data = response.json()
            if not self.__check_response_errors(json_data):
                return ""
            job_id = json_data["id"]
            server = json_data["server"]
            post_url = server + "/upload-file/" + job_id
            response = requests.post(post_url, files={"file": open(file_path, "rb")},
                                     headers={"X-Oc-Api-Key": self.secret_key})
            if response.status_code in [200, 201, 202]:
                response = requests.get(POST_URL + "/" + job_id, headers={"X-Oc-Api-Key": self.secret_key})
                return self.__digest_response(response)
            else:
                print("Uploading of file returned non-success")
                return ""
        else:
            print("Returned a non success status: " + str(response.status_code))
            print("Content: " + str(response.content))
        return ""

    def __save_file(self, uri: str, suffix: str) -> str:
        """
        Given a URI, download the file to the working directory, with the suffix.

        :param uri: URI path to the file
        :param suffix: the suffix to add to the file
        :return: A string of the filename downloaded
        """

        def __do_action():
            request = requests.get(uri)
            if request.status_code in [200, 201, 200]:
                filename = self.working_dir + "/" + self.working_dir + "_" + suffix
                open(filename, "wb").write(request.content)
                print("File saved to " + filename)
                return filename
            print("Could not download file")
            return ""

        try:
            return __do_action()
        except requests.exceptions.ConnectionError:
            print("Could not save file, sleeping 5 seconds and retrying...")
            time.sleep(5)
            return __do_action()

    @staticmethod
    def reformat_answer_key(ans_key_file):
        """
        Given a text answer file converted from a PDF, find the answers and write a formatted answer file of just those
        Assumes 50 questions.
        """
        print("Reformatting the answer key")
        ans_formatted_txt_file = ans_key_file[:-4] + "_formatted.txt"
        with open(ans_key_file, "r") as infile:
            # seek through the file looking for a group of 50 lines with numbers 1-4 on them, but not all 1s
            solutions = list()
            for answer in re.finditer(r"([1-4](\r\n|\r|\n)){50}", infile.read()):
                if not re.match(r"(1(\r\n|\r|\n)){50}", answer.group()):
                    print("Found answer " + str(answer.group()))
                    solutions = [ans.strip() for ans in answer.group().split()]
            if len(solutions) > 0:
                with open(ans_formatted_txt_file, "w") as outfile:
                    question_number = 1
                    for ans in solutions:
                        outfile.write(str(question_number) + " " + ans + "\n")
                        question_number += 1
            else:
                print("Wasn't able to create the answer file!")


if __name__ == "__main__":
    # dc = DocumentControl("2024", "Jan", "chem")
    # exam_text_file = dc.get_conversion("https://www.nysedregents.org/Chemistry/124/chem12024-exam.pdf", "exam")
    # ans_text_file = dc.get_conversion("https://www.nysedregents.org/Chemistry/124/chem12024-sk.pdf", "ans")
    # dc.reformat_answer_key(os.path.join(dc.working_dir, dc.working_dir + "_ans.txt"))
    pass
