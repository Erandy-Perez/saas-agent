# ApexCore Technical Support Agent

Sistema inteligente de asistencia técnica y recuperación de información basado en RAG (Retrieval-Augmented Generation), diseñado para la documentación del SaaS ApexCore.

---

## Arquitectura del Sistema

La solución se encuentra desplegada sobre una infraestructura en la nube utilizando **Oracle Cloud Infrastructure (OCI)**. El sistema desacopla la lógica de procesamiento del backend de la interfaz visual del usuario.

* **Backend / Motor RAG:** Procesamiento de documentos PDF, fragmentación semántica con BGE-M3, indexación vectorial en memoria mediante FAISS y generación de respuestas con Google Gemini.
* **Frontend:** Interfaz web interactiva desarrollada en **Streamlit** con un diseño de interfaz minimalista y arquitectura de capas separadas.

---

## Estructura del Repositorio

```text
apexcore-saas/
│
├── agente.py          # Cerebro del RAG: carga el PDF, arma los embeddings, gestiona FAISS y los prompts del modelo
├── app.py             # Interfaz visual de usuario: maneja la app web con Streamlit y conecta el motor
├── frontend/
│   │   └── style.css  # Capa de presentación: todo el diseño visual, efectos de cristal y estilos
├── directorio/
│   │   └── Manual_ApexCore.pdf # Base de conocimiento oficial del SaaS que consulta el agente
├── requirements.txt   # Dependencias completas del proyecto listas para instalarse de un solo golpe
├── .env               # Archivo de configuración privada donde guardamos nuestra API key
└── .gitignore         # Archivos que ignoramos por seguridad y limpieza (.env, carpetas de caché)
```

---

## Guía de Instalación y Despliegue

Los siguientes pasos están diseñados para ejecutarse dentro de la terminal de tu servidor Linux en Oracle Cloud (OCI) a través de una conexión SSH. 

### 1. Acceso al Servidor y Clonación del Repositorio
Una vez que hayas ingresado a tu instancia mediante SSH, clona el repositorio en tu directorio de trabajo:
```bash
git clone [https://github.com/Erandy-Perez/saas-agent.git](https://github.com/Erandy-Perez/saas-agent.git)
cd saas-agent
```

### 2. Creación y Activación del Entorno Virtual
Para mantener el sistema limpio y evitar conflictos de versiones, aislamos las dependencias creando un entorno virtual de Python:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalación de Dependencias
Con el entorno virtual activo, instala todas las librerías necesarias ejecutando el archivo de requerimientos que ya viene en el repositorio:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configuración de Credenciales
El archivo `.env` ya viene incluido en la estructura base del proyecto. Ábrelo con tu editor de texto en la terminal para ingresar tu llave de acceso a la API de Gemini:
```bash
nano .env
```
*(Asegúrate de que quede estructurado como: `GEMINI_API_KEY=tu_api_key_aqui`, guarda los cambios y cierra el editor).*

### 5. Configuración de Red y Firewall (Puerto 8080)
Para que el servidor permita el tráfico web hacia nuestra aplicación, es necesario abrir el puerto 8080 en el firewall interno de Linux. Ejecuta los siguientes comandos:
```bash
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```
*Nota de infraestructura: Además de este paso, asegúrate de haber agregado una regla de entrada (Ingress Rule) para el puerto 8080 en la Security List de tu red virtual (VCN) desde la consola web de Oracle Cloud.*

### 6. Ejecución de la Aplicación
Finalmente, levanta el servidor de Streamlit forzando la salida por el puerto que acabamos de habilitar:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8080
```

Accede a la interfaz web desde tu navegador utilizando la IP pública de tu instancia y el puerto configurado:
`http://<IP_PUBLICA_OCI>:8080`
