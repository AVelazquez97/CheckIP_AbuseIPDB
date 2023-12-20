#!/bin/python3

import json
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Excepción específica para tratar los errores que arroje la API
class ApiException(Exception):
    def __init__(self, errors):
        super().__init__(errors)
        self.errors = errors

def get_api_data(ip_address, api_key):
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90',
        'verbose': True
    }

    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    # Parsear la respuesta JSON
    return json.loads(response.text)

def main():
    # Definir los parámetros
    ip_address = "190.134.121.102"
    api_key = "d99e5be0a9f432eac4211bcc4435ccc4fd47fcf97807b7e52cbe9eb5c731fa15b2e9862b7bdf4bcb"
    
    '''
    Se intenta realizar la Request HTTP a la API de AbuseIPDB y en caso de obtener una respuesta, se parsea y
    se muestra la información deseada.
    '''
    try:
        parsed_data = get_api_data(ip_address, api_key)

        if "errors" in parsed_data:
            errors = parsed_data.get("errors", [])
            
            raise ApiException(errors)  

        # Mostrar la response completa en formato json
        #print(json.dumps(parsed_data, sort_keys=True, indent=4))

        country_name = parsed_data["data"]["countryName"]
        country_code = parsed_data["data"]["countryCode"]
        is_whitelisted = parsed_data["data"]["isWhitelisted"]
        abuse_confidence_score = parsed_data["data"]["abuseConfidenceScore"]
        total_reports = parsed_data["data"]["totalReports"]
        isp = parsed_data["data"]["isp"]
        usage_type = parsed_data["data"]["usageType"]
        domain = parsed_data["data"]["domain"]
        hostnames = parsed_data["data"]["hostnames"]
        last_reported_at = parsed_data["data"]["lastReportedAt"]
        # reports = parsed_data["data"]["reports"]

    except ApiException as api_exception:
        for error in api_exception.errors:
            detail_error = error.get("detail")
            status = error.get("status")
            print(f"Error: {detail_error}")
            print(f"Código de estado: {status}")

    except KeyError as e:
        print(f"Error: La clave {e} no está presente en la respuesta JSON.")
    
    else:
        # Imprimir la información
        print(f"\nIP: {ip_address}")
        print(f" - País: {country_name}")
        print(f" - Código de País: {country_code}")
        print(f" - ¿Está en lista blanca?: {is_whitelisted}")
        print(f" - Porcentaje de abuso: {abuse_confidence_score}%")
        print(f" - Total de reportes: {total_reports}")
        print(f" - ISP: {isp}")
        print(f" - Tipo de uso: {usage_type}")
        print(f" - Dominio: {domain}")
        print(f" - Hostnames: {hostnames}")
        print(f" - Última vez reportada: {last_reported_at}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminando ejecución...\n')