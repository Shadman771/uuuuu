import json
import time
import psycopg2

from flask import Flask
from flask_cors import CORS, cross_origin
import requests
import re


# from numpy.distutils.fcompiler import none


# app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
#
#
# @app.route('/full_agent/create/<wallet>')
# @cross_origin()
def dso_login_auth(wallet, uuid):
    base_url = "https://uat-api.upay.systems/dham"

    url = base_url + str("/dso/app/v1/login/")
    payload = {
        "wallet_number": wallet,
        "device_uuid": uuid,
        "pin_number": "2580",
        "geo_location": {
            "lat": 190.000,
            "long": 35.00
        }
    }

    res = requests.post(url, json=payload)
    jsonResponse = res.json()
    # print(jsonResponse)
    return jsonResponse["message"], jsonResponse["data"]["access_token"]
    # print(jsonResponse)

    # if jsonResponse["status"] == "FIIO_AUTH_AS_200":
    #     return jsonResponse["message"]

    # response = requests.post(url, json=payload)
    # data = response.json()
    # print(data)
    # return response["message"]
    # print(message)


def create_agent(agent_wallet, Agent_Name, Shop_Name):
    message, token = dso_login_auth("01894841421", "d65m92sae2c60625463a731")
    print("token: ", token)

    url = "https://uat-api.upay.systems/dham/dso/app/v1/agent/onboard/"
    payload = {'wallet_number': agent_wallet,
               'agent_type': 'dao',
               'first_name': Agent_Name,
               'first_name_bn': 'টেস্ট-৫',
               'middle_name': 'shilon',
               'middle_name_bn': 'shilon',
               'last_name': 'Agent',
               'last_name_bn': 'A',
               'father_name': 'Test F',
               'father_name_bn': 'T F',
               'mother_name': 'Test M',
               'mother_name_bn': 'T M',
               'present_address': '{"address": "Road:1, House: 34, Gulshan-1", "city": "Dhaka", "country": "Bangladesh"}',
               'present_address_bn': '{"address": "Road:1, House: 34, Gulshan-1", "city": "Dhaka", "country": "Bangladesh"}',
               'permanent_address': '{"address": "Road:1, House: 34, Gulshan-1", "city": "Dhaka", "country": "Bangladesh"}',
               'permanent_address_bn': '{"address": "Road:1, House: 34, Gulshan-1", "city": "Dhaka", "country": "Bangladesh"}',
               'mobile_number': '01122332010',
               'alternative_mobile_number': '01122332002',
               'gender': '1',
               'dob': '1980-12-15',
               'nationality': 'Bangladeshi',
               'nationality_bn': 'BD',
               'occupation': 'Business',
               'occupation_bn': 'Business',
               'business_name': 'Telecom',
               'business_name_bn': 'Telecom',
               'ownership_type': 'Private',
               'business_address': 'adasdas',
               'business_address_bn': 'asdadad',
               'trade_licence_number': '39128748978916',
               'trade_licence_validity': '2025-07-03',
               'e_tin_number': '39128748978913',
               'shop_name': Shop_Name,
               'shop_name_bn': 'Ucb Cafeteria',
               'shop_location': '{"lat": "23.810335", "long": "90.412532"}',
               'geo_class': 'Suberb',
               'shop_type': 'Grocery',
               'shop_structure': 'Medium',
               'location_tag': '{"district":"dhaka", "thana":"dhaka", "union_municipal":"test"}',
               'district': 'dhaka',
               'thana': 'dhaka',
               'union_municipal': 'test',
               'nid_number': '741851999',
               'shop_location_type': 'Sample'}
    files = [
        ('nid_front', ('lolo.png', open('C:/Users/shadman.shilon/Downloads/lolo.png', 'rb'), 'image/png')),
        ('nid_back', ('lolo.png', open('C:/Users/shadman.shilon/Downloads/lolo.png', 'rb'), 'image/png')),
        ('tin', ('lolo.png', open('C:/Users/shadman.shilon/Downloads/lolo.png', 'rb'), 'image/png')),
        ('agent_photo', ('lolo.png', open('C:/Users/shadman.shilon/Downloads/lolo.png', 'rb'), 'image/png')),
        ('vat', ('lolo.png', open('C:/Users/shadman.shilon/Downloads/lolo.png', 'rb'), 'image/png')),
        ('signature', ('lolo.png', open('C:/Users/shadman.shilon/Downloads/lolo.png', 'rb'), 'image/png'))
    ]
    headers = {
        'Authorization': f'JWT {token}'
    }
    print(payload, headers)
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return response.json()


def get_agent_id(agent_wallet):
    database = "dham_db"

    conn = psycopg2.connect(
        # database=database, user='qaintegration', password='W#y7T_6Y5&eG', host='172.17.10.52', port='5432'
        database=database, user='qaintegration', password='W#y7T_6Y5&eG', host='172.17.10.52', port='5432'
    )

    curr = conn.cursor()

    custom_query = "SELECT id FROM agent_agent WHERE wallet_number = %s"
    curr.execute(custom_query, [agent_wallet])
    rows = curr.fetchall()
    conn.commit()

    conn.close()
    # if not rows:
    #     return none

    # result = ['0', '0']
    result = rows[0][0]

    return result


def dh_auth(dh_wallet):
    url = "https://uat-api.upay.systems/dham/auth_management/web/v1/login/"

    data = {
        "username": dh_wallet,
        "password": "dh123",
        "portal": "distributor"
    }

    res = requests.post(url, json=data)
    jsonResponse = res.json()
    if jsonResponse["code"] == "AMJ_RC200":
        return jsonResponse["token"]


def kyc_upload(agent_wallet):
    id = get_agent_id(agent_wallet)
    print(id)

    token = dh_auth("01190123456")
    print(token)

    url = "https://uat-api.upay.systems/dham/agent/web/v1/upload/kyc/"

    payload = {'agent_id': id,
               'agent_role': '1f920895-8208-40cb-af83-be3e119fd2af'}
    files = [
        ('agent_kyc', ('lolo.png', open('C:/Users/shadman.shilon/Downloads/lolo.png', 'rb'), 'image/png'))
    ]
    headers = {'Authorization': "dham " + str(token)}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return response.json()


def sales_auth():
    url = "https://uat-api.upay.systems/dham/auth_management/web/v1/login/"

    data = {
        "username": "01717888937",
        "password": "35ydt7pAHjZxqnqxiUjdwFfFXEdnNM4D",
        "portal": "sales_ops"
    }

    res = requests.post(url, json=data)
    jsonResponse = res.json()
    if jsonResponse["code"] == "AMJ_RC200":
        # print(jsonResponse["token"])
        # print(jsonResponse["message"]["en"])
        return jsonResponse["token"]


def kyc_approved(agent_wallet):
    print("STEP : 3 >> Agent KYC Approve by Sales Team")
    agent_id = get_agent_id(agent_wallet)
    # KYC APPROVE
    # ----------------------------------------------------------------------------------------------------------------
    sales_token = sales_auth()
    headers = {'Authorization': "dham " + str(sales_token)}
    kyc_approve_url = "https://uat-api.upay.systems/dham/agent/web/v1/kyc/approval/" + str(agent_id) + "/"

    kyc_approve_body = \
        {"approval_status": "Verified"
         }
    kyc_approve_response = requests.put(kyc_approve_url, headers=headers, json=kyc_approve_body)
    jsonResponse = kyc_approve_response.json()
    print(jsonResponse)
    if kyc_approve_response.ok:
        print(jsonResponse["message"] + " (KYC)")
        # print(">>Agent KYC Approved Successfully")
    else:
        print("AGENT KYC VERIFICATION FAILED")

    # # token = sales_auth()
    # agent_id = get_agent_id(agent_wallet)
    # token = sales_auth()
    #
    # url = "https://uat-api.upay.systems/dham/agent/web/v1/kyc/approval/" + str(agent_id) + "/"
    #
    # payload = json.dumps({
    #
    #     "approval_status": "Verified"
    #
    # })
    #
    # headers = {'Authorization': "dham " + str(token)}
    #
    # response = requests.request("PUT", url, headers=headers, data=payload)
    #
    # print(response.text)


def agent_approved(agent_wallet):
    agent_id = get_agent_id(agent_wallet)
    print("STEP : 3 >> Agent KYC Approve by Sales Team")

    # KYC APPROVE
    # ----------------------------------------------------------------------------------------------------------------
    sales_token = sales_auth()
    headers = {'Authorization': "dham " + str(sales_token)}
    agent_approve_url = "https://uat-api.upay.systems/dham/approval/web/v1/agent/action/"
    print("agent_id: ", agent_id)

    agent_approve_body = {"agent": agent_id,
                          "action_type": "approve",
                          "note": "this is note",
                          "agent_role": "dao"
                          }
    agent_approve_response = requests.post(agent_approve_url, headers=headers, json=agent_approve_body)
    print(agent_approve_response)
    jsonResponse = agent_approve_response.json()
    print(jsonResponse)
    return agent_approve_response.json()

    # if agent_approve_response.ok:
    #     print(jsonResponse).
    #     # print(">>Agent KYC Approved Successfully")
    # else:
    #     print("AGENT KYC VERIFICATION FAILED")


def get_otp(agent_wallet):
    database = "nhs_db"
    conn = psycopg2.connect(database=database, user='qaintegration', password='W#y7T_6Y5&eG', host='172.17.10.52',
                            port='5432')
    curr = conn.cursor()
    custom_query = "SELECT payload from nhs_notification_notificationevent where payload ->> 'to' = %s and ( payload " \
                   "->> 'notification_type' = '9' or payload ->> 'notification_type' = '10') ORDER BY created_at DESC" \
                   " LIMIT 1; "
    curr.execute(custom_query, [agent_wallet])
    rows = curr.fetchall()
    conn.commit()
    conn.close()
    print("rows ", rows)
    result = rows[0][0]["message"]

    # result = rows[0][0]["message"]
    try:
        y = re.findall(r"\d+", result)

        result = [otp for otp in y if len(otp) in [4, 6]][0]
        # print(result)
    except Exception as e:
        result = "No OTP/PIN Found"

    return result


if __name__ == "__main__":
    agent_wallet = input("Enter the agent wallet: ")
    Agent_Name = input("Enter the agent name: ")
    Shop_Name = input("Enter the shop name: ")

    # agent_wallet = "01199999600"
    #
    # Agent_Name = "Qa_agent_99"
    # Shop_Name = "Qa_agent_99_shop"

    message, access_token = dso_login_auth("01894841421", "d65m92sae2c60625463a731")
    print("token ==  " + str(access_token))
    print("message ==  " + str(message))
    print("\nDSO OK\n")
    agent = create_agent (agent_wallet, Agent_Name, Shop_Name)
    print("\nAGENT OK\n")

    x = dh_auth("01190123456")
    print(x)
    print("\nDH OK\n")

    kyc_upload(agent_wallet)
    print("\nKYC OK\n")

    sales = sales_auth()
    print("\nSALES OK\n")

    print(sales)

    time.sleep(1)
    kyc_approved(agent_wallet)
    print("\nKYC APPROVED OK\n")

    time.sleep(1)
    agent_approved(agent_wallet)
    print("\nAGENT APPROVED OK\n")

    time.sleep(3)
    w = get_otp(agent_wallet)
    print("\nOTP OK\n")

    print(w)
