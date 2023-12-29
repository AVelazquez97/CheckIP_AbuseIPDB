#!/usr/bin/python3
# Command checkip
# version 1.0
# by: Alexis Velázquez

import json
import requests
import sys

API_KEY = "d99e5be0a9f432eac4211bcc4435ccc4fd47fcf97807b7e52cbe9eb5c731fa15b2e9862b7bdf4bcb"

# Excepción específica para tratar los errores que arroje la API
class ApiException(Exception):
    def __init__(self, errors):
        super().__init__(errors)
        self.errors = errors

def get_api_data(ip_address):
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90',
        'verbose': True #Si se encuentra en True, se reciben el país y los reportes de la IP
    }

    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    # Parsear la respuesta JSON
    return json.loads(response.text)

def main():
    # Definir los parámetros
    #ip_address = "190.134.121.102"

    if len(sys.argv) != 2:
        print("Uso: ./checkip.py <ip_address>")
        sys.exit(1)
    
    # Se obtiene la dirección IP del argumento de línea de comandos
    ip_address = sys.argv[1]

    '''
    Se intenta realizar la Request HTTP a la API de AbuseIPDB y en caso de obtener una respuesta, se parsea y
    se muestra la información deseada.
    '''
    try:
        parsed_data = get_api_data(ip_address)

        # En caso de que se obtenga un error como respuesta de la API, se tira una excepción.
        if "errors" in parsed_data:
            errors = parsed_data.get("errors", [])
            raise ApiException(errors)  

        # Es posible mostrar la response completa en formato json de esta forma
        # print(json.dumps(parsed_data, sort_keys=True, indent=4))

        # Si no se obtuvo error de la API, se almacena el diccionario de claves recibido en "data"
        data = parsed_data.get("data")

        country_name = data.get("countryName")
        country_code = data.get("countryCode")
        is_whitelisted = data.get("isWhitelisted")
        abuse_confidence_score = data.get("abuseConfidenceScore")
        total_reports = data.get("totalReports")
        isp = data.get("isp")
        usage_type = data.get("usageType")
        domain = data.get("domain")
        hostnames = data.get("hostnames")
        last_reported_at = data.get("lastReportedAt")
        #reports = data.get("reports")

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
        #print(f" - Reportes: {reports}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminando ejecución...\n')
