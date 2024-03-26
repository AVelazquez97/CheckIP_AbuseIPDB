# Script que permite chequear detalles de una dirección IP, consultando la API de AbuseIPDB.

En primera instancia, se debe instalar dotenv para obtener variables de entorno del archivo **_.env_**. 
Para esto se puede utilizar el siguiente comando:

```
pip3 install python-dotenv
```

Una vez instalada la librería, se debe renombrar el archivo **_example.env_** por **_.env_** y cargar el auth token que 
proporciona AbuseIPDB para el uso de su API.

* **Es importante aclarar que para obtener un auth token es necesario crearse una cuenta en AbuseIPDB**

### Pasos adicionales para ejecutar script en Mac:

1. `pip3 install requests`

2. `pip3 uninstall urllib3`

3. `pip3 install 'urllib3<2.0'`
