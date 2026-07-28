# ApexCore Technical Support Agent

Proyecto desarrollado para Alura y ONE como parte del Challenge AlurAgente.

Acceso público a la aplicación: http://140.84.190.205:8080

Sistema inteligente de asistencia técnica y recuperación de información basado en Retrieval Augmented Generation, diseñado para la documentación del SaaS ApexCore.

## Arquitectura del Sistema

La solución se encuentra desplegada sobre una infraestructura en la nube utilizando Oracle Cloud Infrastructure. El sistema desacopla la lógica de procesamiento del backend de la interfaz visual del usuario.

Backend / Motor RAG: Procesamiento de documentos PDF, fragmentación semántica con BGE M3, indexación vectorial en memoria mediante FAISS y generación de respuestas con Google Gemini.

Frontend: Interfaz web interactiva desarrollada en Streamlit con un diseño de interfaz minimalista y arquitectura de capas separadas.

## Evidencias OCI y Ejemplos de Uso

Para las evidencias de uso de Oracle Cloud, el repositorio incluye el archivo Despliegue_Agente_RAG_ApexCore.pdf y capturas de pantalla que demuestran el correcto funcionamiento del proyecto, la configuración de red y las reglas de seguridad en la plataforma.

Ejemplos de preguntas y respuestas del agente:

Pregunta: Como se configura un nuevo usuario administrador en la plataforma.
Respuesta: El agente extraerá la ruta exacta del panel de control basándose en el manual oficial.

Pregunta: Cuales son los pasos para generar el reporte mensual.
Respuesta: El sistema listará las instrucciones precisas para la exportación de datos.

## Estructura del Repositorio

```text
saas-agent/
agente.py : Cerebro del RAG, carga el PDF, arma los embeddings y gestiona FAISS
app.py : Interfaz visual de usuario, maneja la app web con Streamlit
frontend/style.css : Capa de presentación, diseño visual y estilos
directorio/Manual_ApexCore.pdf : Base de conocimiento oficial del SaaS
requirements.txt : Dependencias completas del proyecto
.env : Archivo de configuración para claves de acceso
Despliegue_Agente_RAG_ApexCore.pdf : Documento de evidencia técnica
```

## Guía de Instalación y Despliegue

Los siguientes pasos están diseñados para ejecutarse dentro de la terminal de un servidor Linux en Oracle Cloud a través de una conexión SSH.

### 1. Acceso al Servidor y Clonación del Repositorio

Una vez dentro de la instancia mediante SSH, se debe clonar el repositorio en el directorio de trabajo:

```bash
git clone [https://github.com/Erandy-Perez/saas-agent.git](https://github.com/Erandy-Perez/saas-agent.git)
cd saas-agent
```

### 2. Creación y Activación del Entorno Virtual

Para mantener el sistema limpio y evitar conflictos de versiones, se aíslan las dependencias creando un entorno virtual de Python:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalación de Dependencias

Con el entorno virtual activo, se instalan todas las librerías necesarias ejecutando el archivo de requerimientos incluido en el repositorio:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configuración de Credenciales

El archivo .env se encuentra en la estructura base del proyecto. Se requiere abrirlo con un editor de texto en la terminal para ingresar la llave de acceso a la API de Gemini:

```bash
nano .env
```

Se debe asegurar que la estructura quede definida como GEMINI_API_KEY=clave_aqui en el interior. Posteriormente, se guardan los cambios y se cierra el editor.

### 5. Configuración de Red y Firewall

Para permitir el tráfico web hacia la aplicación, es necesario abrir el puerto 8080 en el firewall interno de Linux ejecutando los siguientes comandos:

```bash
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

Nota de infraestructura: Además de la configuración del sistema operativo, es mandatorio agregar una regla de entrada para el puerto 8080 en la lista de seguridad de la red virtual desde la consola web de Oracle Cloud.

### 6. Ejecución de la Aplicación

Finalmente, se levanta el servidor de Streamlit. Para asegurar que el servicio se mantenga activo de forma permanente en segundo plano, incluso al cerrar la sesión SSH, se ejecuta el siguiente comando:

```bash
nohup streamlit run app.py --server.address 0.0.0.0 --server.port 8080 > streamlit.log 2>&1 &
```

Una vez ejecutado, el sistema estará disponible permanentemente a través del navegador ingresando la dirección IP pública de la instancia y el puerto configurado: http://140.84.190.205:8080
