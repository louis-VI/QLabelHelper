import sys
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QDateTimeEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QDateTime
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor


class QueryAssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("labelHelper")

        # Create username
        self.username_label = QLabel(self)
        self.username_label.setText("Account Name")
        self.username_label.setFixedWidth(68)
        self.username_label.move(30, 20)
        self.username_textbox = QLineEdit(self)
        self.username_textbox.move(120, 20)
        self.username_textbox.setFixedWidth(230)

        # Create token
        self.token_label = QLabel(self)
        self.token_label.setText("Token")
        self.token_label.setFixedWidth(68)
        self.token_label.move(30, 60)
        self.token_textbox = QLineEdit(self)
        self.token_textbox.setEchoMode(QLineEdit.Password)  # Hidden password
        self.token_textbox.move(120, 60)
        self.token_textbox.setFixedWidth(230)

        # Create date
        self.date_label = QLabel(self)
        self.date_label.setText("Select Date")
        self.date_label.setFixedWidth(68)
        self.date_label.move(30, 100)
        self.date_edit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.move(120, 100)
        self.date_edit.setFixedWidth(230)

        # Create submit button
        self.submit_button = QPushButton(self)
        self.submit_button.setText("Bascial Search")
        self.submit_button.move(30, 140)
        self.submit_button.clicked.connect(self.submit_credentials)

        # Create clear button
        self.clear_button = QPushButton(self)
        self.clear_button.setText("Reset")
        self.clear_button.move(250, 140)
        self.clear_button.clicked.connect(self.clear_credentials)

        # Create result textbox
        self.result_textbox = QTextEdit(self)
        self.result_textbox.move(30, 180)
        self.result_textbox.setFixedWidth(320)
        self.result_textbox.setFixedHeight(280)
        self.result_textbox.setReadOnly(True)

        # Create clear result button
        self.clear_result_button = QPushButton(self)
        self.clear_result_button.setText("Clear Result")
        self.clear_result_button.move(30, 475)
        self.clear_result_button.clicked.connect(self.clear_result)

        # Create exit button
        self.exit_button = QPushButton(self)
        self.exit_button.setText("Exit")
        self.exit_button.move(250, 475)
        self.exit_button.clicked.connect(self.close)

        # Set window size
        self.setGeometry(300, 300, 400, 520)


    def submit_credentials(self):
        username = self.username_textbox.text()
        token_password = self.token_textbox.text()
        target_date = self.date_edit.dateTime().toString("yyyy-MM-dd")


        # Write the code to fetch data here, using username, token_password, and target_date for the query

        class Request:
            def __init__(self, url, headers, cookies, params=None):
                self.url = url
                self.headers = headers
                self.cookies = cookies
                self.params = params
                self.response = None

            def send_request(self):
                self.response = requests.get(self.url, headers=self.headers, cookies=self.cookies, params=self.params)
        headers = {
            "authority": "codelabel.tencent.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "dnt": "1",
            "referer": "https://codelabel.tencent.com/securegate:codelabel/mine",
            "sec-ch-ua": "^\\^Not/A)Brand^^;v=^\\^99^^, ^\\^Microsoft",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "traceparent": "00-d9df1bcb8b19dface5e745938a6654e2-c957e725a2d55e7e-01",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
        }
        cookies = {
            "token": str(token_password)}
        url = "https://codelabel.tencent.com/api/function/label-by-self"
        params5 = {
            "manual_level": "5"
        }
        params3 = {
            "manual_level": "3"
        }
        params1 = {
            "manual_level": "1"
        }
        # Create request object list
        requests_list = [
            Request(url, headers, cookies),
            Request(url, headers, cookies, params={"manual_level": "5"}),
            Request(url, headers, cookies, params={"manual_level": "3"}),
            Request(url, headers, cookies, params={"manual_level": "1"})
        ]

        def send_requests(requests):
            for request in requests:
                request.send_request()

        # Create thread pool
        executor = ThreadPoolExecutor(max_workers=30)

        # Connect the request object list to the send_requests function
        futures = executor.submit(send_requests, requests_list)

        # wait for all requests to complete
        futures.result()

        # Close thread pool
        executor.shutdown()

        # Visit the response data
        response = requests_list[0].response
        responsegd = requests_list[1].response
        responsemd = requests_list[2].response
        responsebd = requests_list[3].response


        # Total label data
        json_data = response.json()
        # transformation
        data_list = json_data['data']

        # good label
        json_data_gd = responsegd.json()
        # transformation
        data_list_gd = json_data_gd['data']

        # medium label
        json_data_md = responsemd.json()
        # transformation
        data_list_md = json_data_md['data']

        # bad label
        json_data_bd = responsebd.json()
        # transformation
        data_list_bd = json_data_bd['data']

        def process_total_data(data_list, target_date):
            global labelCount
            global totalId
            labelCount = 0
            totalId = []
            for item in range(len(data_list)):
                str_json = json.dumps(data_list[item], ensure_ascii=False)
                dict = json.loads(str_json)
                labeled_at = dict['labeled_at']
                labeledId = dict["id"]
                totalId.append(labeledId)
                if str(target_date) in labeled_at:
                    labelCount = labelCount + 1

            # print("Total Data: ", labelCount)

            # Define a function to handle the logic of processing data labeled as 'good' in the loop traversal

        def process_good_data(data_list_gd, target_date):
            global gd_count
            global gdId

            gd_count = 0
            gdId = []
            gdSign = []
            for item in range(len(data_list_gd)):
                str_json_gd = json.dumps(data_list_gd[item], ensure_ascii=False)
                dict_gd = json.loads(str_json_gd)

                labeled_at_gd = dict_gd['labeled_at']
                labeledId_gd = dict_gd["id"]
                gdId.append(labeledId_gd)

                if str(target_date) in labeled_at_gd:
                    gd_count = gd_count + 1
                    # List of all method names labeled as good for the current day, there are some fields that do not have a signature, a judgment needs to be made

                    # Additional operations can be performed here on the results, such as saving or printing, etc.
                    # print("Good Data: ", gd_count)

                    # Define a function to handle the logic of data processing in the loop traversal

        def process_medium_data(data_list_md, target_date):
            global md_count
            global mdId

            md_count = 0
            mdId = []
            mdSign = []
            for item in range(len(data_list_md)):
                str_json_md = json.dumps(data_list_md[item], ensure_ascii=False)
                dict_md = json.loads(str_json_md)
                labeled_at_md = dict_md['labeled_at']
                labeledId_md = dict_md["id"]
                mdId.append(labeledId_md)
                if str(target_date) in labeled_at_md:
                    md_count = md_count + 1

            # Print the number of items labeled as 'medium': {md_count}

            # Define a function to handle the logic of processing data labeled as 'poor' in the loop traversal

        def process_bad_data(data_list_bd, target_date):
            global bd_count
            global bdId
            global bdSign
            bd_count = 0
            bdId = []
            for item in range(len(data_list_bd)):
                str_json_bd = json.dumps(data_list_bd[item], ensure_ascii=False)
                dict_bd = json.loads(str_json_bd)

                labeled_at_bd = dict_bd['labeled_at']
                labeledId_bd = dict_bd["id"]
                bdId.append(labeledId_bd)
                if str(target_date) in labeled_at_bd:
                    bd_count = bd_count + 1

            # Additional operations can be performed here on the results, such as saving or printing, etc.
            # print("Bad Data: ", bd_count)

            # Create four threads to handle different loops respectively

        t1 = threading.Thread(target=process_total_data, args=(data_list, target_date))
        t2 = threading.Thread(target=process_good_data, args=(data_list_gd, target_date))
        t3 = threading.Thread(target=process_medium_data, args=(data_list_md, target_date))
        t4 = threading.Thread(target=process_bad_data, args=(data_list_bd, target_date))

        # start the threads
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # wait for all threads to complete
        t1.join()
        t2.join()
        t3.join()
        t4.join()

        print("All processing threads finished...\n" + "Data Loaded finish")
        print("Total Data:", labelCount)



        forget_num = labelCount - gd_count - md_count - bd_count
        # Define a function to handle the logic of processing data labeled in the loop traversal
        data = "The number of labels you have labeled today is: " + str(labelCount) + "\n\n"
        data1 = "The number of labels marked as good is: " + str(gd_count) + "\n\n"
        data2 = "The number of labels marked as medium is: " + str(md_count) + "\n\n"
        data3 = "The number of labels marked as poor is: " + str(bd_count) + "\n\n"
        data4 = "The number of missed data entries is: " + str(forget_num) + "\n\n"

        full_data = data + data1 + data2 + data3 + data4
        self.result_textbox.setText(full_data)

        time.sleep(0.5)




    def clear_credentials(self):
        self.username_textbox.clear()
        self.token_textbox.clear()

    def clear_result(self):
        self.result_textbox.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QueryAssistantWindow()
    window.show()
    sys.exit(app.exec_())
