import time
import requests
import json
import threading
from concurrent.futures import ThreadPoolExecutor

print(r""" 
--------------------------------------------
   __     __       ____ __    __            
  / /__ _/ /  ___ / / // /__ / /__  ___ ____
 / / _ `/ _ \/ -_) / _  / -_) / _ \/ -_) __/
/_/\_,_/_.__/\__/_/_//_/\__/_/ .__/\__/_/   
                            /_/             
--------------------------------------------                             """+"\n")


print("Welcome to LABELHELPER~\n")

username = input("Enter username: ")
token = input("Enter token: ")

while True:
    target_date = input("\nEnter the labeling date you need to query\n"
                         "Enter the date in the format YYYY-MM-DD for specific date labeling data,\n"
                         "YYYY-MM for monthly labeling data (supports monthly pass rate query),\n"
                         "or 'all' for global pass rate query\n")
    if target_date == "all":
        target_date = 2
    # Collections of labeled good, medium, and bad data IDs
    totalId = []
    gdId = []
    mdId = []
    bdId = []
    print("Initializing....\n")

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
        "token": str(token)}
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

    params2 = {
        "check_approve": "1"
    }

    params4 = {
        "check_approve": "2"
    }

    # Create a list of request objects
    requests_list = [
        Request(url, headers, cookies),
        Request(url, headers, cookies, params={"manual_level": "5"}),
        Request(url, headers, cookies, params={"manual_level": "3"}),
        Request(url, headers, cookies, params={"manual_level": "1"}),
        Request(url, headers, cookies, params={"check_approve": "1"}),
        Request(url, headers, cookies, params={"check_approve": "2"}),
    ]

    def send_requests(requests):
        for request in requests:
            request.send_request()

    # Create a thread pool
    executor = ThreadPoolExecutor(max_workers=20)

    # Submit the request tasks to the thread pool and execute them
    futures = executor.submit(send_requests, requests_list)

    # Wait for all requests to complete
    futures.result()

    # Close the thread pool
    executor.shutdown()

    # Access the response data
    response = requests_list[0].response
    responsegd = requests_list[1].response
    responsemd = requests_list[2].response
    responsebd = requests_list[3].response
    responsepass = requests_list[4].response
    responsefailed = requests_list[5].response

    # Check the connection status of the program
    if response.status_code == 200:
        print('Connected Successfully')
    else:
        print("Connection Failed, wait 10s")
        time.sleep(10)
    # Total labeled data
    json_data = response.json()
    data_list = json_data['data']

    # Labeled good data
    json_data_gd = responsegd.json()
    data_list_gd = json_data_gd['data']

    # Labeled medium data
    json_data_md = responsemd.json()
    data_list_md = json_data_md['data']

    # Labeled bad data
    json_data_bd = responsebd.json()
    data_list_bd = json_data_bd['data']

    # Passed data
    json_data_pass = responsepass.json()
    data_list_pass = json_data_pass["data"]

    # Failed data
    json_data_failed = responsefailed.json()
    data_list_failed = json_data_failed["data"]

    # Function to process total data
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
                labelCount += 1

    # Function to process good data
    def process_good_data(data_list_gd, target_date):
        global gd_count
        global gdId
        global gdSign
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
                gd_count += 1
                if "signature" in dict_gd:
                    labeledsign_gd = dict_gd["signature"]
                    gdSign.append(labeledsign_gd)
                else:
                    labeledsign_gd = dict_gd["id"]
                    gdSign.append(labeledsign_gd)

    # Function to process medium data
    def process_medium_data(data_list_md, target_date):
        global md_count
        global mdId
        global mdSign
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
                md_count += 1
                if "signature" in dict_md:
                    labeledsign_md = dict_md["signature"]
                    mdSign.append(labeledsign_md)
                else:
                    labeledsign_md = dict_md["id"]
                    mdSign.append(labeledsign_md)

    # Function to process bad data
    def process_bad_data(data_list_bd, target_date):
        global bd_count
        global bdId
        global bdSign
        bd_count = 0
        bdId = []
        bdSign = []
        for item in range(len(data_list_bd)):
            str_json_bd = json.dumps(data_list_bd[item], ensure_ascii=False)
            dict_bd = json.loads(str_json_bd)

            labeled_at_bd = dict_bd['labeled_at']
            labeledId_bd = dict_bd["id"]
            bdId.append(labeledId_bd)
            if str(target_date) in labeled_at_bd:
                bd_count += 1
                if "signature" in dict_bd:
                    labeledsign_bd = dict_bd["signature"]
                    bdSign.append(labeledsign_bd)
                else:
                    labeledsign_bd = dict_bd["id"]
                    bdSign.append(labeledsign_bd)

    # Function to process passed data
    def process_pass_data(data_list_pass, target_date):
        global pass_count
        global passId
        pass_count = 0
        passId = []
        if target_date != 2:
            datajudge = target_date.count("-")

        if target_date == 2 or datajudge <= 1:
            for item in range(len(data_list_pass)):
                str_json_pass = json.dumps(data_list_pass[item], ensure_ascii=False)
                dict_pass = json.loads(str_json_pass)
                labeled_at_pass = dict_pass['labeled_at']
                labeledId_pass = dict_pass["id"]
                passId.append(labeledId_pass)
                if str(target_date) in labeled_at_pass:
                    pass_count += 1
    def process_failed_data(data_list_failed, target_date):
        global failed_count
        global failedId
        failed_count = 0
        failedId = []
        if target_date !=2:
            datajudge=target_date.count("-")

        if target_date==2 or datajudge <=1:
            for item in range(len(data_list_failed)):
                str_json_failed = json.dumps(data_list_failed[item], ensure_ascii=False)
                dict_failed = json.loads(str_json_failed)
                labeled_at_failed = dict_failed['labeled_at']
                labeledId_failed = dict_failed["id"]
                failedId.append(labeledId_failed)
                if str(target_date) in labeled_at_failed:
                    failed_count = failed_count + 1




    # Create a thread pool
    t1 = threading.Thread(target=process_total_data, args=(data_list, target_date))
    t2 = threading.Thread(target=process_good_data, args=(data_list_gd, target_date))
    t3 = threading.Thread(target=process_medium_data, args=(data_list_md, target_date))
    t4 = threading.Thread(target=process_bad_data, args=(data_list_bd, target_date))
    t5 = threading.Thread(target=process_pass_data, args=(data_list_pass, target_date))
    t6 = threading.Thread(target=process_failed_data, args=(data_list_failed, target_date))

    # Start the threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    # Wait for all threads to complete
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    print("All processing threads finished...\n" + "Data Loading finished")
    print("Total Data:", labelCount)
    print(f"Bad Data:{bd_count}")
    print(f"Medium Data:{md_count}")
    print(f"Good Data: {gd_count}")

    if (pass_count!=0 and pass_count!=None)or (failed_count!=0 and failed_count!=None):
        print(f"pass data:{pass_count}")
        print(f"failed data:{failed_count}")
        pass_rate = ' {:.2%}'.format (pass_count / (pass_count + failed_count))
        print(f"pass rate:{pass_rate}")


    def specificSign():
        while True:
            while True:
                selectStatus = input(
                    "\nAssistant can list method names labeled as good, medium, or bad for you,\nInput 'g' to query the good data list,\nInput 'm' to query the medium data list,\nInput 'b' to query the bad data list,\nInput 'n' to not query\n")
                if selectStatus == "g":
                    for i, item in enumerate(gdSign):
                        print(f"{i + 1}.{item}")
                    break
                elif selectStatus == "m":
                    for i, item in enumerate(mdSign):
                        print(f"{i + 1}.{item}")
                    break
                elif selectStatus == "b":
                    for i, item in enumerate(bdSign):
                        print(f"{i + 1}.{item}")
                    break
                elif selectStatus == "n":
                    break
            breakSelect = input(
                "Do you confirm to continue querying the method name list of the day's labeled data? 'y' to continue, 'n' to go back\n")
            if breakSelect == "y":
                continue
            elif selectStatus == "n" or breakSelect == "n":
                break


    selectItem1 = input(
        "Do you need to continue querying? Continue with 'y', exit with 'n', view specific good, medium, bad data with 's'\n")
    if selectItem1 == "y":
        continue  # Note that this continue will restart the while loop no matter where it is placed
    elif selectItem1 == "n":
        break
    elif selectItem1 == "s":
        specificSign()

    selectItem2 = input("Do you need to continue querying? Continue with 'y', exit with 'n'\n")
    if selectItem2 == "y":
        continue
    elif selectItem2 == "n":
        break
