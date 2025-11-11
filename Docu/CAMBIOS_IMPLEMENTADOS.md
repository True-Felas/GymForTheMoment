# Cambios Implementados en la Aplicación de Gimnasio

## Resumen de Cambios

Se han implementado tres mejoras principales en la aplicación:

### 1. ✅ Migración de MySQL a SQLite

**Cambios realizados:**

- Reemplazado `mysql.connector` por `sqlite3` (librería nativa de Python)
- Base de datos ahora se almacena en el archivo `gimnasio.db` en la raíz del proyecto
- No requiere instalación de MySQL/XAMPP
- Sintaxis SQL adaptada a SQLite:
  - `AUTO_INCREMENT` → `AUTOINCREMENT`
  - `VARCHAR`, `INT`, `BOOLEAN` → tipos de SQLite apropiados
  - Placeholders `%s` → `?`

**Archivos modificados:**

- `Backend/DataBase/database.py`
- `Backend/Model/user_model.py`
- `Backend/Model/reserv_model.py`

**Beneficios:**

- Base de datos local portable
- No requiere servidor MySQL
- Ideal para aprendizaje y desarrollo

---

### 2. ✅ Sistema de Reservas de Máquinas (Individual)

**Cambios realizados:**

- Las reservas ahora son para **máquinas de gimnasio** en lugar de clases grupales
- Cada máquina solo puede ser reservada por **una persona** a la vez
- Lista de máquinas disponibles:
  - Cinta de Correr 1 y 2
  - Bicicleta Estática 1 y 2
  - Elíptica 1 y 2
  - Remo 1
  - Press de Banca
  - Prensa de Piernas
  - Máquina de Poleas
  - Rack de Sentadillas
  - Banco de Abdominales

**Cambios en la base de datos:**

- Tabla `reservas`: campo `clase` renombrado a `maquina`
- Campo `asistio` renombrado a `completada`

**Cambios en la interfaz:**

- Vista de reservas muestra máquinas en lugar de clases
- Indicadores visuales:
  - 🟢 Verde: Máquina disponible
  - 🔴 Rojo: Máquina ocupada

**Archivos modificados:**

- `Backend/Model/reserv_model.py`
- `Frontend/View/reserv_view.py`
- `Frontend/View/app.py`

---

### 3. ✅ Sistema de Niveles Automático

**Cambios realizados:**

- Los usuarios suben de nivel automáticamente cada **3 reservas completadas**
- Nuevo campo en tabla `usuarios`: `reservas_completadas`
- Las reservas se marcan como completadas automáticamente cuando pasa su horario

**Lógica implementada:**

1. Al abrir la ventana de reservas, se verifica si hay reservas vencidas
2. Las reservas vencidas se marcan como completadas automáticamente
3. Por cada reserva completada, se incrementa el contador del usuario
4. Cada 3 reservas completadas → sube 1 nivel

**Ejemplo:**

- Nivel 1 → 3 reservas completadas → Nivel 2
- Nivel 2 → 6 reservas completadas → Nivel 3
- Y así sucesivamente...

**Archivos modificados:**

- `Backend/DataBase/database.py` (nuevo campo)
- `Backend/Model/user_model.py` (método `incrementar_reservas_completadas`)
- `Backend/Model/reserv_model.py` (método `procesar_reservas_vencidas`)
- `Backend/Controller/reserv_control.py` (método `verificar_y_procesar_reservas_vencidas`)
- `Frontend/View/app.py` (integración en la vista)

---

## Cómo Probar los Cambios

### 1. Ejecutar el script de pruebas

```bash
python test_database.py
```

Este script verifica:

- Creación de base de datos SQLite
- Usuarios de ejemplo
- Creación de reservas
- Verificación de disponibilidad de máquinas
- Sistema de niveles

### 2. Ejecutar la aplicación

```bash
python main.py
```

**Credenciales de prueba:**

- Usuario: `admin` / Contraseña: `1234`
- Usuario: `juan` / Contraseña: `gym2025`
- Usuario: `sofia` / Contraseña: `fitlife`

### 3. Probar funcionalidades

1. **Reservar una máquina:**

   - Hacer login
   - Clic en "Reservar Máquina"
   - Seleccionar fecha, máquina y horario
   - Confirmar reserva

2. **Verificar disponibilidad:**

   - Hacer login con otro usuario
   - Intentar reservar la misma máquina/horario
   - Debería aparecer como "OCUPADA" (🔴)

3. **Verificar sistema de niveles:**
   - Crear 3 reservas con fechas/horas pasadas
   - Abrir la ventana de reservas (ejecuta verificación automática)
   - Ver que el nivel sube automáticamente

---

## Estructura de la Base de Datos

### Tabla: usuarios

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nivel INTEGER DEFAULT 1,
    reservas_completadas INTEGER DEFAULT 0
)
```

### Tabla: reservas

```sql
CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    maquina TEXT NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    duracion INTEGER DEFAULT 1,
    completada INTEGER DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
)
```

---

## Archivos Nuevos

- `test_database.py` - Script de pruebas para verificar funcionamiento
- `gimnasio.db` - Base de datos SQLite (se crea automáticamente)
- `CAMBIOS_IMPLEMENTADOS.md` - Esta documentación

---

## Notas Importantes

1. **Compatibilidad:** El proyecto ya no requiere MySQL. Solo necesitas Python con las librerías estándar.

2. **Base de datos:** El archivo `gimnasio.db` se crea automáticamente la primera vez que ejecutas la aplicación.

3. **Sistema de niveles:** Es automático. No requiere intervención manual. Solo asegúrate de que las fechas/horas de las reservas sean pasadas para que se marquen como completadas.

4. **Capacidad de máquinas:** Actualmente configurado a 1 persona por máquina. Si deseas cambiarlo, modifica `CAPACIDAD_POR_MAQUINA` en `Backend/Model/reserv_model.py`.

---

## Pendientes / Mejoras Futuras

- [ ] Agregar notificaciones cuando un usuario sube de nivel
- [ ] Implementar un cron job o tarea programada para verificar reservas vencidas periódicamente
- [ ] Agregar historial de niveles alcanzados
- [ ] Implementar sistema de recompensas por nivel
- [ ] Agregar vista de "Mis Reservas" con estado de cada una

---

¡Todos los cambios han sido implementados exitosamente! 🎉
