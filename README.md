# Script que permite chequear detalles de una dirección IP, consultando la API de AbuseIPDB.

**ACLARACIÓN: Esta herramienta está enfocada en sistemas UNIX.**

En primera instancia, se debe instalar dotenv para obtener variables de entorno del archivo **_.env_**. 
Para esto se puede utilizar el siguiente comando:

```
pip3 install python-dotenv
```

Una vez instalada la librería, se debe renombrar el archivo **_example.env_** por **_.env_** y cargar el auth token que 
proporciona AbuseIPDB para el uso de su API.

* **Es importante aclarar que para obtener un auth token es necesario crearse una cuenta en AbuseIPDB**

- - -

### Configuraciones adicionales para ejecutar script en Mac:

1. `pip3 install requests`

2. `pip3 uninstall urllib3`

3. `pip3 install 'urllib3<2.0'`

- - -

### Ejecución de script:

Para la ejecución del script, es recomendado agregarlo al PATH del sistema operativo. Para esto, hay que seguir los 
siguientes pasos:

1. Ingresar a la terminal y ejecutar este comando: `echo $PATH` 

   Esto devolverá todas las rutas que se encuentran agregadas al path, cada una separada por dos puntos de la siguiente.

2. Copiar el script para cualquiera de las rutas de los directorios que estén en el path, por ejemplo:

   `cp checkip.py /usr/local/bin/checkip`

3. Copiar el archivo **_.env_** que contiene la API_KEY al mismo directorio que el script:

   `cp .env /usr/local/bin/`

4. Luego, darle permiso de ejecución:

   `chmod +x /usr/local/bin/checkip`

5. Por último, ejecutarlo con:

   `checkip IP` -> Donde IP se debe remplazar por la IP que se desee consultar la info.

