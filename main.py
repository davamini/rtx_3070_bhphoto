from bs4 import BeautifulSoup
import requests as rq
from twilio.rest import Client
import datetime
import time
import os
import json

current_dir = os.path.dirname(os.path.realpath(__file__))
json_conf_path = os.path.join(current_dir, 'config.json')

json_conf_file = open(json_conf_path, )
conf_data = json.load(json_conf_file)
json_conf_file.close()

twilio_sid = conf_data['twilio']['sid']
twilio_authtoken = conf_data['twilio']['authtoken']


twilio_client = Client(twilio_sid, twilio_authtoken)

url_lst = ["https://www.bhphotovideo.com/c/product/1602755-REG/asus_dualrtx30708g_geforce_rtx_3070_8g.html",
		   "https://www.bhphotovideo.com/c/product/1600127-REG/zotac_zt_a30700h_10p_gaming_geforce_rtx_3070.html",
		   "https://www.bhphotovideo.com/c/product/1598689-REG/gigabyte_gv_n3070gaming_oc_8gd_geforce_rtx_3070_gaming.html/DFF/d10-v21-t1-x1077130/SID/103810X1560435X64606e72562e38ec2460bb8c6854831b",
		   "https://www.bhphotovideo.com/c/product/1599833-REG/gigabyte_gv_n3070eagle_8gd_geforce_rtx_3070_eagle.html/DFF/d10-v21-t1-x1077131/SID/103810X1560435X567d650128124a675584ee8dd2ab630a",
		   "https://www.bhphotovideo.com/c/product/1602756-REG/asus_strixrtx3070o8_rog_strix_geforce_rtx.html/DFF/d10-v21-t1-x1078311/SID/103810X1560435X7a0bcf4b76d10568265f2c5e71546520"
		  ]

not_available_lst = ["New Item - Coming Soon", "More on the Way"]


def no_replicants(lst):

	replicants = []
	for i in lst:
		count = 0
		for j in lst:
			if j == i:
				count += 1
		if count > 1:
			replicants.append(i)

	return replicants


def send_msg(msg):

	print(msg)
	twilio_client.messages.create(
		            to=conf_data["twilio"]["recipient_number"],
		            from_=conf_data["twilio"]["from_number"],
		            body=msg,
		        )

def get_availability_text(url):

	content = rq.get(url).text
	soup = BeautifulSoup(content, 'lxml')
	text = soup.find("span", {"data-selenium": "stockStatus"}).text

	return text


def main(url_lst):

	while True:

		try:

			for url in url_lst:
				text = get_availability_text(url)
				
				if text not in not_available_lst:
					msg = f"RTX_3070 Buy at: {url}"
					send_msg(msg)
					
					return

				else:
					now = datetime.datetime.now()
					print(f"No change: {now}")

				time.sleep(10)

		except rq.exceptions.ConnectionError as e:
			print(f"Error: {e}\n\nSleeping for 60 seconds")
			time.sleep(60)


if __name__ == "__main__":

	reps = no_replicants(url_lst)

	if len(reps) > 0:
		raise Exception(f"{reps}")

	main(url_lst)
