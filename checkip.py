#!/usr/bin/python3
# Command checkip
# version 1.0
# by: Alexis Velázquez

import json
import sys
from requests import request
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_KEY = getenv('API_KEY')

class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

class APIRequestError(Exception):
    pass

class AbuseAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url='https://api.abuseipdb.com/api/v2/check'
        self.headers = {
            'Accept': 'application/json',
            'Key': self.api_key
        }

    def get_ip_info(self, ip_address):  
        querystring = {
            'ipAddress': ip_address,
            'maxAgeInDays': '90',
            'verbose': True  # Si se encuentra en True, se reciben el país y los reportes de la IP
        }

        response = request(method='GET', url=self.url, headers=self.headers, params=querystring)
        # Se parsea la respuesta JSON
        response_data = json.loads(response.text)
        
        # En caso de que se obtenga un error como respuesta de la API, se tira una excepción.
        if 'errors' in response_data:
            raise APIRequestError(response_data['errors'])
        
        return response_data['data']

def print_ip_info(ip_info):
        print(f'\n{Color.BOLD}{Color.GREEN}IP:{Color.END} {Color.YELLOW}{Color.BOLD}{ip_info['ipAddress']}{Color.END}')
        print(f'{Color.GREEN} - País:{Color.END} {Color.CYAN}{ip_info.get('countryName')}{Color.END}')
        print(f'{Color.GREEN} - Código de País: {Color.END} {Color.CYAN}{ip_info.get('countryCode')}{Color.END}')
        print(f'{Color.GREEN} - ¿Está en lista blanca?: {Color.END} {Color.CYAN}{ip_info.get('isWhitelisted')}{Color.END}')
        print(f'{Color.GREEN} - Porcentaje de abuso: {Color.END} {Color.CYAN}{ip_info.get('abuseConfidenceScore')}%{Color.END}')
        print(f'{Color.GREEN} - Total de reportes: {Color.END} {Color.CYAN}{ip_info.get('totalReports')}{Color.END}')
        print(f'{Color.GREEN} - ISP: {Color.END} {Color.CYAN}{ip_info.get('isp')}{Color.END}')
        print(f'{Color.GREEN} - Tipo de uso: {Color.END} {Color.CYAN}{ip_info.get('usageType')}{Color.END}')
        print(f'{Color.GREEN} - Dominio: {Color.END} {Color.CYAN}{ip_info.get('domain')}{Color.END}')
        print(f'{Color.GREEN} - Hostnames: {Color.END} {Color.CYAN}{ip_info.get('hostnames')}{Color.END}')
        print(f'{Color.GREEN} - Última vez reportada: {Color.END} {Color.CYAN}{ip_info.get('lastReportedAt')}{Color.END}\n')

def main():
    if len(sys.argv) != 2:
        print(f'\n{Color.GREEN}No has ingresado ninguna IP.{Color.END}')
        print(f'{Color.GREEN}Uso:{Color.END} {Color.CYAN}./checkip.py <ip_address>{Color.END}\n')
        sys.exit(1)
    
    # Se obtiene la dirección IP del argumento recibido por línea de comandos
    ip_address = sys.argv[1]

    '''
    Se intenta realizar la Request HTTP a la API de AbuseIPDB y en caso de obtener una respuesta, se parsea y
    se muestra la información deseada.
    '''
    try:
        endpoint = AbuseAPI(API_KEY)
        ip_info = endpoint.get_ip_info(ip_address)

        # Si no se obtuvo error de la API, se almacena el diccionario de claves recibido en 'data'
        print_ip_info(ip_info)
        
    except APIRequestError as error:
        for values in error.args[0]:
            print(f'\n{Color.RED}Error:{Color.END} {Color.YELLOW}{values['detail']}{Color.END}')
            print(f'{Color.RED}Código de estado:{Color.END} {Color.YELLOW}{values['status']}{Color.END}\n')

    except KeyError as e:
        print(f'\n{Color.RED}Error:{Color.END} {Color.YELLOW}La clave {e} no está presente en la respuesta JSON.{Color.END}')

    except Exception as e:
        print(f'\n{Color.RED}Error inesperado:{Color.END}: {Color.YELLOW}{e}{Color.END}')

    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminando ejecución...\n')
