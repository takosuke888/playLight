
import os
import uuid
import time
import hashlib
import hmac
import base64
import requests
import json
class SwitchBotAPI:

    def __init__(self):

        self.switchbot_hostname = 'https://api.switchbot.net/v1.1/devices'
        #self.switchbot_hostname = 'https://api.switch-bot.com/v1.1/devices'

        setting = open('switchbot_token.json', 'r')
        setting = json.load(setting)
    
        self.token = setting['token']
        self.secret = setting['secret']
        self.header = self.create_header()

        device_name = "ダイニング"
        self.bulb_device_id = self.get_deviceID_by_name(device_name)

        #self.generate_curl_bat()

    def create_header(self):
        nonce = uuid.uuid4()
        timestamp = int(round(time.time() * 1000))
        string_to_sign = f'{self.token}{timestamp}{nonce}'

        signature = base64.b64encode(
            hmac.new(
                self.secret.encode(), 
                msg=string_to_sign.encode(), 
                digestmod=hashlib.sha256
            ).digest()
        ).decode()

        #print(timestamp)

        return {
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'charset': 'utf8',
            't': str(timestamp),
            'sign': signature,
            'nonce': str(nonce)
        }

    def generate_curl_bat(self, output_file="switchbot_request.bat"):
        curl_command = (
            f'curl -X GET "{self.switchbot_hostname}" '
            f'-H "Authorization: {self.header["Authorization"]}" '
            f'-H "Content-Type: {self.header["Content-Type"]}" '
            f'-H "charset: {self.header["charset"]}" '
            f'-H "t: {self.header["t"]}" '
            f'-H "sign: {self.header["sign"]}" '
            f'-H "nonce: {self.header["nonce"]}"'
        )

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(f'@echo off\n{curl_command}\n')

        print(f"バッチファイル {output_file} を生成しました。")

    def get_devices(self):
        url = self.switchbot_hostname
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.json()}"

    def turn_on(self, device_id: str):
        url = f'{self.switchbot_hostname}/{device_id}/commands'
        payload = {
            'command': 'turnOn', 
            "parameter": 'default',
        }
        response = requests.post(url, headers=self.header, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.json()}"

    def turn_off(self, device_id: str):
        url = f'{self.switchbot_hostname}/{device_id}/commands'
        payload = {
            'command': 'turnOff', 
            "parameter": 'default',
        }
        response = requests.post(url, headers=self.header, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.json()}"

    def set_color(self, device_id: str, color: str):
        url = f'{self.switchbot_hostname}/{device_id}/commands'
        payload = {
            'command': 'setColor', 
            "parameter": color,
        }
        response = requests.post(url, headers=self.header, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.json()}"
        
    def set_cct(self, device_id: str, cct: int):
        url = f'{self.switchbot_hostname}/{device_id}/commands'
        payload = {
            'command': 'setColorTemperature', 
            "parameter": cct,
        }
        response = requests.post(url, headers=self.header, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.json()}"

    def get_deviceID_by_name(self, name: str):
        devices = self.get_devices()
        print(devices)
        if isinstance(devices, dict) and 'body' in devices and 'deviceList' in devices['body']:
            for device in devices['body']['deviceList']:
                if device['deviceName'] == name:
                    return device['deviceId']
        return None
    
    def get_device_status(self, deviceId: str):
        url = f'{self.switchbot_hostname}/{deviceId}/status'
        response = requests.get(url, headers=self.header)
        return response.json()

# 使用例
if __name__ == "__main__":
    api = SwitchBotAPI()

    devices = api.get_devices()
    print(devices)

    device_name = "ダイニング"
    device_id = api.get_deviceID_by_name(device_name)

    if device_id:
        print(api.get_device_status(device_id))
