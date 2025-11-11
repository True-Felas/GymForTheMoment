# GymForTheMoment 🏋️

Aplicación de gestión de gimnasio desarrollada en Python con CustomTkinter.

## 🌟 Características Principales

### Sistema de Reservas

- 🏋️ Reserva de máquinas individuales (12 máquinas disponibles)
- 📅 Calendario interactivo para seleccionar fechas
- ⏰ 24 horarios disponibles (00:00 - 23:00)
- 🗓️ Restricción de reservas: **solo de Lunes a Viernes**
- 🔴 Indicadores visuales de disponibilidad (Disponible/Ocupada)
- ✅ Procesamiento automático de reservas completadas

### Sistema de Pagos

- 💳 Cuota mensual de 50€ por usuario
- 📊 Generación automática de recibos mensuales
- 💰 Registro de pagos por parte del usuario
- 📋 **Listado de usuarios morosos** (pagos pendientes)
- 🔍 Comparación de recibos vs pagos realizados
- 👤 Vista de administrador para gestión completa

### Sistema de Niveles

- 🏆 Niveles automáticos basados en reservas completadas
- 📈 Sube 1 nivel cada 3 reservas completadas
- 📊 Barra de progreso visual
- 🎯 Mensajes motivacionales

### Rutinas de Entrenamiento

- 🌱 **Nivel Fácil**: 7 ejercicios, 30-45 min (Principiantes)
- 🔥 **Nivel Intermedio**: 8 ejercicios, 45-60 min (Con experiencia)
- ⚡ **Nivel Avanzado**: 10 ejercicios, 60-90 min (Atletas)
- 📋 Detalles de cada ejercicio (series, repeticiones, descanso)
- ✅ Seguimiento de rutinas completadas

### Perfil y Progreso

- 👤 Perfil personalizado con avatar
- 📊 Estadísticas completas de entrenamiento
- 💪 Historial de rutinas por nivel
- 🏆 Visualización de progreso hacia siguiente nivel
- ⏱️ Contador de horas entrenadas

### Historial

- 📜 Registro completo de todas las reservas
- 🔍 Filtros (Todas/Completadas/Pendientes)
- 📊 Resumen de estadísticas
- 📅 Información detallada de cada reserva

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **CustomTkinter** - Interfaz gráfica moderna
- **SQLite3** - Base de datos local
- **tkcalendar** - Widget de calendario

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/True-Felas/GymForTheMoment.git
cd GymForTheMoment
```

2. Instala las dependencias:

```bash
pip install customtkinter tkcalendar
```

3. Ejecuta la aplicación:

```bash
python main.py
```

## 🧪 Pruebas

Ejecuta el script de pruebas para verificar la funcionalidad:

```bash
python test_database.py
```

## 👥 Usuarios de Prueba

| Usuario | Contraseña |
| ------- | ---------- |
| admin   | 1234       |
| juan    | gym2025    |
| sofia   | fitlife    |

## 📂 Estructura del Proyecto

```
GymForTheMoment/
├── Backend/
│   ├── Controller/
│   │   ├── login_controller.py
│   │   └── reserv_control.py
│   ├── DataBase/
│   │   └── database.py
│   └── Model/
│       ├── reserv_model.py
│       ├── rutina_model.py
│       └── user_model.py
├── Frontend/
│   └── View/
│       ├── app.py
│       ├── historial_view.py
│       ├── login.py
│       ├── progreso_view.py
│       ├── reserv_view.py
│       └── rutinas_view.py
├── gimnasio.db
├── main.py
├── test_database.py
├── CAMBIOS_IMPLEMENTADOS.md
├── NUEVAS_FUNCIONALIDADES.md
└── README.md
```

## 🗃️ Base de Datos

La aplicación utiliza SQLite con 3 tablas principales:

### `usuarios`

- Información de usuarios
- Nivel y progreso
- Contador de reservas completadas

### `reservas`

- Reservas de máquinas
- Estado (completada/pendiente)
- Fecha, hora y duración

### `pagos`

- Recibos mensuales de usuarios
- Estado de pago (pagado/pendiente)
- Fecha de pago registrada
- Monto de la cuota (50€)

## 🎯 Funcionalidades Destacadas

### Automatización

- ✅ Procesamiento automático de reservas vencidas
- 📈 Actualización automática de niveles
- ⏱️ Cálculo automático de horas entrenadas

### Interfaz Intuitiva

- 🎨 Diseño moderno con CustomTkinter
- 🔍 Navegación clara y sencilla
- 📱 Ventanas responsivas

### Seguimiento Completo

- 📊 Estadísticas en tiempo real
- 📜 Historial detallado
- 🏆 Progreso visual

## 📖 Documentación Adicional

- [CAMBIOS_IMPLEMENTADOS.md](CAMBIOS_IMPLEMENTADOS.md) - Cambios iniciales (SQLite, máquinas, niveles)
- [NUEVAS_FUNCIONALIDADES.md](NUEVAS_FUNCIONALIDADES.md) - Funcionalidades recientes (historial, rutinas, perfil)
- [DOCUMENTACION_DIAGRAMAS.md](DOCUMENTACION_DIAGRAMAS.md) - **Diagramas completos del sistema** (E-R, Clases UML, Casos de Uso, Secuencia)

## 🤝 Contribuciones

Este es un proyecto de aprendizaje. Las sugerencias y mejoras son bienvenidas.

## 📝 Licencia

Proyecto educativo desarrollado para aprendizaje de Python y desarrollo de interfaces gráficas.

## ✨ Autor

Desarrollado por **True-Felas** como proyecto de aprendizaje.

---

¡Disfruta tu entrenamiento! 💪🏋️
