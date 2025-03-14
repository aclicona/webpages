# Proyecto Django + Vue + Nuxt 3

Este proyecto utiliza Django como backend y Vue.js (dashboard), con Nuxt 3 como frontend.

## Requisitos previos

- Git
- Python 3.12
- Node.js 22
- PostgreSQL

## Instalación y configuración

### Backend (Django)

#### 1. Instalar Python 3.12

**En Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

**En macOS (usando Homebrew):**
```bash
brew update
brew install python@3.12
```

**En Windows:**
- Descarga el instalador desde [python.org](https://www.python.org/downloads/release/python-3120/)
- Ejecuta el instalador y asegúrate de marcar la opción "Add Python to PATH"

#### 2. Crear un entorno virtual

```bash
python3.12 -m venv venv
```

#### 3. Activar el entorno virtual

**En Linux/macOS:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

#### 4. Clonar el repositorio

```bash
git clone https://github.com/aclicona/web-pages-backend.git webpage
cd webpage
```

#### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

#### 6. Instalar y configurar PostgreSQL

**En Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**En macOS (usando Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**En Windows:**
- Descarga e instala PostgreSQL desde [postgresql.org](https://www.postgresql.org/download/windows/)

#### 7. Crear una base de datos PostgreSQL

```bash
sudo -u postgres psql
```

En la consola de PostgreSQL, ejecuta:
```sql
CREATE DATABASE nombre_db;
CREATE USER nombre_usuario WITH PASSWORD 'contraseña';
ALTER ROLE nombre_usuario SET client_encoding TO 'utf8';
ALTER ROLE nombre_usuario SET default_transaction_isolation TO 'read committed';
ALTER ROLE nombre_usuario SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE nombre_db TO nombre_usuario;
\q
```

#### 8. Configurar las variables de entorno (opcional)

Crea un archivo `.env` en la raíz del proyecto:
```
DEBUG=True
SECRET_KEY="tu_clave_secreta"
DATABASE_URL=postgres://nombre_usuario:contraseña@localhost:5432/nombre_db
DEVELOPMENT=1
```

#### 9. Aplicar las migraciones

```bash
python manage.py migrate
```

#### 10. Crear un superusuario (opcional)

```bash
python manage.py createsuperuser
```

#### 11. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

El backend de Django estará disponible en: http://127.0.0.1:8000/

### Frontend (Vue.js + Nuxt 3)

#### 1. Instalar Node.js 22

**En Ubuntu/Debian (usando NVM):**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22
```

**En macOS (usando Homebrew):**
```bash
brew update
brew install node@22
```

**En Windows:**
- Descarga el instalador desde [nodejs.org](https://nodejs.org/)

#### 2. Clonar el repositorio del frontend

Desde la raíz del proyecto principal:

```bash
git clone https://github.com/aclicona/web-pages-frontend.git frontend
cd frontend
```

#### 3. Instalar las dependencias

```bash
npm install
```

#### 4. Iniciar el servidor de desarrollo

```bash
npm run dev
```

El frontend estará disponible en: http://localhost:3000/

## Estructura del proyecto

```
proyecto/
├── venv/                  # Entorno virtual de Python
├── manage.py              # Script de Django
├── backend/               # Configuración principal de Django
├── dashboard/             # Aplicación de dashboard bajo Vue que renderiza Django
├── frontend/              # Proyecto Nuxt 3
│   ├── node_modules/      
│   ├── pages/             # Páginas de Nuxt
│   ├── components/        # Componentes de Vue
│   ├── nuxt.config.js     # Configuración de Nuxt
│   └── package.json       # Dependencias de Node.js
└── README.md              # Este archivo
```

## Comandos útiles

### Django

- Crear migraciones: `python manage.py makemigrations`
- Aplicar migraciones: `python manage.py migrate`
- Crear superusuario: `python manage.py createsuperuser`
- Recolectar archivos estáticos: `python manage.py collectstatic`
- Ejecutar tests: `python manage.py test`

### Nuxt/Vue

- Ejecutar en modo desarrollo: `npm run dev`
- Construir para producción: `npm run build`
- Iniciar en modo producción: `npm run start`
- Ejecutar linter: `npm run lint`

## Despliegue

### Backend (Django)

Para desplegar el backend en producción, considera:
- Gunicorn como servidor WSGI
- Nginx como proxy inverso
- Configuración adecuada de variables de entorno
- Deshabilitar DEBUG en producción

### Frontend (Nuxt)

Para desplegar el frontend en producción:
- Construir con `npm run build`
- Servir con Nginx o un servicio de hosting estático

## Contribuir

1. Haz fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un nuevo Pull Request

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)