from flask import Flask, request, jsonify, render_template # Flask se usa para crear la aplicación web. request se usa para acceder a los datos de la solicitud HTTP. jsonify Se usa para convertir un objeto Python en una respuesta JSON. render_template se usa para cargar y devolver un archivo HTML, Flask buscará ese archivo en una carpeta llamada templates dentro de tu proyecto.
import requests # importa el módulo requests que se usa para hacer peticiones HTTP a APIs externas.
from sqlalchemy import create_engine, Column, String, Float, Integer # create_engine Se usa para crear una conexión a la base de datos. Column se usa para definir las columnas de una tabla en la base de datos. String, Float, Integer se usan para especificar los tipos de datos de las columnas.
from sqlalchemy.orm import declarative_base, sessionmaker # declarative_base se usa para crear una clase base para declarar modelos de datos. sessionmaker es una clase de SQLAlchemy que genera fábricas de sesiones.
import os # os proporciona funciones para interactuar con el sistema operativo. En este caso, se utiliza para acceder a las variables de entorno.
from dotenv import load_dotenv

# Crear la app Flask
app = Flask(__name__) # crea una app web. __name__ es un atributo del objeto __main__ que es como el contenedor de todo lo que está sucediendo en tu programa principal. Si el archivo se ejecuta directamente el valor de __name__ será "__main__". Flask utiliza __name__ para determinar el directorio raíz de tu aplicación web.

# Configuración de la base de datos SQLite
DATABASE_URL = 'sqlite:///weather.db' # sqlite indica que el tipo de base de datos es SQLite. :/// esto significa que la base de datos se almacena en un archivo físico en el sistema de archivos local. weather.db es el nombre de la base de datos que se creará.
engine = create_engine(DATABASE_URL, echo=False) # create_engine es una función de SQLalchemy, construye el motor de la base de datos, es lo que establece y mantiene una conexión activa con la base de datos. echo=True hace que se impriman todas las consultas SQL que se ejecutan en la consola.
Base = declarative_base() # es parte de SQLAlchemy, crea una clase base declarativa que se utilizará para definir modelos de base de datos. Esta clase especial de SQLAlchemy actúa como un registro de todos los modelos de datos que defines. Has definido un modelo llamado WeatherQuery. En SQLAlchemy, el enfoque declarativo te permite definir tus tablas de base de datos como clases de Python, donde los atributos de la clase representan las columnas de la tabla. Al hacer esto, puedes interactuar con la base de datos utilizando objetos en lugar de tener que escribir SQL directamente.

# Modelo de la base de datos
class WeatherQuery(Base): # se crea una nueva clase que hereda de Base que es declarative_base().
    __tablename__ = 'weather_queries' # define el nombre de la tabla en la base de datos. estos '__' '__' indican que es una variable especial de Python. 
    id = Column(Integer, primary_key=True) # Column es una clase de SQLAlchemy que define una columna en la base de datos. Integer especifica que esta columna almacenará números enteros. primary_key=True indica a SQLAlchemy que la columna id debe ser la clave primaria de la tabla asociada a ese modelo. Se crea un índice único sobre la columna id en la base de datos. Esto acelera las consultas de búsqueda y recuperación de datos.
    city = Column(String, nullable=False) # define una columna llamada 'city'. String indica que almacenará texto. nullable=False significa que este campo no puede estar vacío (es obligatorio).
    temperature = Column(Float, nullable=False) # define una columna llamada 'temperature'. Float indica que almacenará números decimales.
    
Base.metadata.create_all(engine) # el constructor de tablas. metadata es un atributo de declarative_base, contiene detalles sobre la estructura de la base de datos, como los nombres de las tablas y columnas, la información necesaria para crear las tablas. create_all() este método se utiliza para crear todas las tablas definidas en los modelos de datos que han sido registrados en la metadata. engine es el objeto que representa la conexión a tu base de datos, sin esta conexión SQLAlchemy no sabría a qué base de datos enviar las sentencias SQL para crear las tablas.
Session = sessionmaker(bind=engine) # sessionmaker es una clase de SQLAlchemy que genera fábricas de sesiones. bind=engine le indica a sessionmaker que "enlace" la fábrica de sesiones al motor de la base de datos (engine), esto significa que las sesiones que se creen con esta fábrica estarán conectadas a tu base de datos SQLite.
session = Session() # al llamar a Session() como si fuera una función, se crea una nueva sesión de base de datos, esta sesión es la que te permitirá interactuar con la base de datos: insertar datos, consultar datos, modificar datos, etc.

@app.route('/') # '/' es la ruta raíz de tu aplicación, está diciendo que la función que sigue (en este caso, home()) debe ejecutarse cuando un usuario visite la ruta '/' de la aplicación web.
def home():
    return render_template('index.html') # usamos el comando return para devolver una respuesta al navegador que está solicitando esa ruta. En este caso, la respuesta será la página HTML que se genera con la función render_template().

# Endpoint para consultar el clima
@app.route('/weather', methods=['GET']) # @app.route() este decorador de Flask conecta una función a una ruta específica de tu aplicación web. '/weather' Es la ruta o endpoint de tu API, cuando un cliente haga una petición a /weather, se ejecutará la función que está debajo del decorador. methods=['GET'] especifica que este endpoint solo responderá a peticiones GET. GET es un método HTTP que se utiliza para solicitar datos, se pone en una lista porque pueden ser varios métodos.
def get_weather():
    city = request.args.get('city') # request es un objeto global de Flask que contiene información sobre la petición HTTP actual. .args es un diccionario que contiene los parámetros de la URL por ejemplo, si la URL es /weather?city=London, entonces request.args['city'] sería igual a 'London'. .get('city') Es un método seguro para obtener el valor del parámetro city, si el parámetro no existe, .get() devuelve None en lugar de generar un error.
    if not city:
        return jsonify({'error': 'city parameter is required'}), 400 # convierte diccionarios, listas, etc en una cadena en formato JSON, y lo convierte en un objeto de respuesta HTTP Flask, la cadena JSON se envía como cuerpo de la respuesta junto con los encabezados HTTP necesarios. En Flask el segundo argumento de return '400' es el código de estado HTTP de la respuesta. Que en este caso es 400 que es (Bad request).
    
    # Consumir la API externa (OpenWeatherMap)
    # api_key = "8bbba212313bdfcda0193f9f94c75169" # mi API key de OpenWeatherMap.
    load_dotenv() # carga las variables de entorno desde un archivo .env.
    api_key = os.getenv('API_KEY') # .getenv() obtiene el valor de la variable de entorno llamada "API_KEY" desde un archivo .env, Las variables de entorno son una forma de almacenar información sensible, como API Keys, sin tener que escribirlas directamente en el código.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial" # construcción de la URL para la petición a la API de OpenWeatherMap, la encuentras en su documentación. Se empieza a construir después del '?', cada parámetro se separa con '&'. q= nombre de la ciudad. appid= tu API key. units= determina cómo se mostrarán las mediciones del clima, 'metric' para Celsius (°C), 'imperial' para Fahrenheit (°F) y 'standard' para Kelvin(C), por defecto si no especificas 'units'.
    response = requests.get(url) # se utiliza la librería 'requests' para hacer una petición GET a la URL de la API de OpenWeatherMap, el resultado de la petición se guarda en la variable response.

    if response.status_code != 200: # .status_code este atributo del objeto response contiene el código de estado HTTP de la respuesta. Un código de estado 200 significa que la petición fue exitosa.
        return jsonify({'error': 'city not found.'}), 404 # convierte diccionarios, listas, etc en una cadena en formato JSON, y lo convierte en un objeto de respuesta HTTP Flask, la cadena JSON se envía como cuerpo de la respuesta junto con los encabezados HTTP necesarios. En Flask el segundo argumento de return '404' es el código de estado HTTP de la respuesta. Que en este caso es 404 que es (Not Found).

    data = response.json() # la API de OpenWeatherMap te devuelve los datos en formato JSON. .json() convierte ese texto JSON en un diccionario de Python que puedes usar fácilmente.
    temperature = data['main']['temp'] # navega por el diccionario 'data'. ['main'] accede a la clave 'main' que contiene otro diccionario. ['temp'] accede a la clave 'temp' dentro del diccionario 'main' y guarda su valor en la variable 'temperature'.

    # Guardar la consulta en la base de datos
    query = WeatherQuery(city=city, temperature=temperature) # aquí estás creando un nuevo objeto de la clase WeatherQuery, recuerda que esta clase es tu modelo de datos, que representa la estructura de la tabla weather_queries en tu base de datos. city=city, temperature=temperature con esto estás asignando los valores de las variables city y temperature (que obtuviste de la API de OpenWeatherMap) a los atributos correspondientes del objeto WeatherQuery. En este punto, tienes un objeto query que contiene la información de la consulta del clima, pero todavía no está guardado en la base de datos.
    session.add(query) # .add() este método agrega el objeto query a la sesión, indicando que quieres que se guarde en la base de datos. En este momento, el objeto query está en un estado "pendiente",  esperando a ser guardado de forma permanente en la base de datos.
    session.commit() # .commit() este método envía una sentencia SQL INSERT a la base de datos para insertar el objeto query en la tabla weather_queries.

    return jsonify({'city': city.title(), 'temperature': temperature}) # convierte diccionarios, listas, etc en una cadena en formato JSON, y lo convierte en un objeto de respuesta HTTP Flask, la cadena JSON se envía como cuerpo de la respuesta junto con los encabezados HTTP necesarios.

# Endpoint para listar todas las consultas guardadas
@app.route('/history', methods=['GET']) # indica que la función get_history() se ejecutará cuando se haga una petición GET a la ruta /history.
def get_history():
    queries = session.query(WeatherQuery).all() # 'session' es un objeto que representa la sesión de la base de datos, se utiliza para interactuar con la base de datos. .query() crea una consulta para obtener datos de la tabla WeatherQuery. WeatherQuery es el modelo que representa la tabla en la base de datos donde se almacenan las consultas. .all() ejecuta la consulta y devuelve una lista de todos los objetos WeatherQuery encontrados.
    return jsonify([{'city': q.city.title(), 'temperature': q.temperature} for q in queries]) # esto es una lista de comprensión. Sobre cada iteración de 'q' en 'queries' que es una lista de objetos que representan una consulta individual cada uno. Estos objetos tienen atributos, para acceder a los atributos de un objeto se usa '.' en este caso 'q.city' y 'q.temperature'. Esto crea otra lista de diccionarios a partir de esta.

if __name__ == '__main__': # cada archivo que contiene código se considera un módulo, cada módulo tiene un atributo especial llamado '__name__', el valor de '__name__' dentro de el mismo archivo se establece como '__main__', cuando importas el módulo en otro archivo el valor de '__name__' será el nombre del archivo sin '.py'. Por eso esta condición verifica si el código se está ejecutando como el programa principal o no.
    app.run(debug=True) # .run() es el método que inicia el servidor de desarrolo de Flask. debug=True activa el modo de depuración.

# https://openweathermap.org/current Documentación de OpenWeatherMap.

# 'data' ejemplo estructura de contenido JSON convertido en diccionario Python usando .json()
"""
data = {
    "coord": {
        "lon": -3.7026,
        "lat": 40.4165
    },
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 28.5,
        "feels_like": 27.8,
        "temp_min": 27.0,
        "temp_max": 30.0,
        "pressure": 1012,
        "humidity": 40
    },
    "visibility": 10000,
    "wind": {
        "speed": 3.6,
        "deg": 90
    },
    "clouds": {
        "all": 0
    },
    "dt": 1672531200,
    "sys": {
        "type": 1,
        "id": 6450,
        "country": "ES",
        "sunrise": 1672485600,
        "sunset": 1672528800
    },
    "timezone": 3600,
    "id": 3117735,
    "name": "Madrid",
    "cod": 200
}
"""

# 'queries' ejemplo estructura de lista de objetos donde cada objeto representa una consulta.
"""
queries = [
  WeatherQuery(city="Madrid", temperature=25), 
  WeatherQuery(city="London", temperature=15), 
  WeatherQuery(city="Paris", temperature=20)
]
"""