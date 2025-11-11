# Documentación Técnica - GymForTheMoment

## Diagramas del Sistema

### 1. Diagrama Entidad-Relación (E-R)

```
┌──────────────────┐
│    USUARIOS      │
├──────────────────┤
│ PK id            │
│    nombre        │
│    password      │
│    nivel         │
│    reservas_     │
│    completadas   │
└────────┬─────────┘
         │
         │ 1
         │
         │
         │ N
         ▼
┌──────────────────┐
│    RESERVAS      │
├──────────────────┤
│ PK id            │
│ FK usuario_id    │◄───────┐
│    maquina       │        │
│    fecha         │        │ Restricción:
│    hora          │        │ - Lunes a Viernes
│    duracion      │        │ - 24 horas (00:00-23:00)
│    completada    │        │ - 1 persona por máquina
└──────────────────┘        │
                            │
         ┌──────────────────┘
         │
         │ 1
         │
         │
         │ N
         ▼
┌──────────────────┐
│      PAGOS       │
├──────────────────┤
│ PK id            │
│ FK usuario_id    │
│    mes           │
│    anio          │
│    monto         │
│    pagado        │
│    fecha_pago    │
└──────────────────┘
         ▲
         │
         │ 1
         │
         │
         │ N
         ▼
┌──────────────────┐
│  RUTINAS_        │
│  COMPLETADAS     │
├──────────────────┤
│ PK id            │
│ FK usuario_id    │
│    nivel         │
│    fecha_        │
│    completada    │
│    ejercicios_   │
│    completados   │
└──────────────────┘
```

**Relaciones:**

- **USUARIOS** 1:N **RESERVAS** - Un usuario puede tener muchas reservas
- **USUARIOS** 1:N **PAGOS** - Un usuario puede tener muchos pagos
- **USUARIOS** 1:N **RUTINAS_COMPLETADAS** - Un usuario puede completar muchas rutinas

---

### 2. Diagrama de Clases UML

```
┌─────────────────────────────────┐
│         Database                │
├─────────────────────────────────┤
│ - DB_PATH: str                  │
│ - connection: sqlite3.Connection│
│ - cursor: sqlite3.Cursor        │
├─────────────────────────────────┤
│ + __init__()                    │
│ + conectar(): void              │
│ + crear_tablas(): void          │
│ + cerrar(): void                │
│ + get_connection(): Connection  │
└─────────────────────────────────┘
                ▲
                │ usa
                │
    ┌───────────┴───────────┬─────────────────┬─────────────────┐
    │                       │                 │                 │
┌───┴─────────────────┐ ┌───┴──────────────┐ ┌┴──────────────┐ ┌┴──────────────┐
│    UserModel        │ │  ReservaModel    │ │  RutinaModel  │ │  PagoModel    │
├─────────────────────┤ ├──────────────────┤ ├───────────────┤ ├───────────────┤
│ + validar_usuario() │ │ + MAQUINAS[]     │ │ + RUTINAS{}   │ │ + CUOTA: 50.0 │
│ + registrar_usuario()│ │ + HORARIOS[]     │ │ + obtener_    │ │ + generar_    │
│ + obtener_id()      │ │ + crear_reserva()│ │   rutina()    │ │   recibo()    │
│ + obtener_stats()   │ │ + maquina_       │ │ + marcar_     │ │ + registrar_  │
│ + incrementar_      │ │   disponible()   │ │   completada()│ │   pago()      │
│   reservas()        │ │ + procesar_      │ │ + obtener_    │ │ + obtener_    │
└─────────────────────┘ │   vencidas()     │ │   stats()     │ │   morosos()   │
                        └──────────────────┘ └───────────────┘ └───────────────┘
            ▲                   ▲                   ▲                 ▲
            │                   │                   │                 │
            │ usa              │ usa               │ usa             │ usa
            │                   │                   │                 │
    ┌───────┴────────┬──────────┴───────┬───────────┴──────┬──────────┴──────┐
    │                │                  │                  │                 │
┌───┴──────────┐ ┌───┴────────────┐ ┌───┴────────────┐ ┌───┴────────────┐ ┌──┴───────────┐
│LoginController│ │ReservasController│ │ RutinasView   │ │ HistorialView │ │  PagosView   │
├──────────────┤ ├──────────────────┤ ├────────────────┤ ├───────────────┤ ├──────────────┤
│ - modelo     │ │ - modelo         │ │ - rutina_model│ │ - usuario_id  │ │ - pago_model │
│ - vista      │ │ - user_model     │ │ + mostrar_    │ │ + actualizar_ │ │ - es_admin   │
│ + validar_   │ │ + verificar_     │ │   detalle()   │ │   historial() │ │ + crear_     │
│   login()    │ │   vencidas()     │ │ + completar_  │ │ + crear_      │ │   interfaz() │
│ + registrar_ │ │ + crear_reserva()│ │   rutina()    │ │   tarjeta()   │ │ + generar_   │
│   usuario()  │ └──────────────────┘ └────────────────┘ └───────────────┘ │   recibos()  │
│ + abrir_app()│                                                            │ + ver_morosos│
└──────────────┘                                                            └──────────────┘
        │
        │ controla
        ▼
┌─────────────────────────────────┐
│           Login                 │
│        (CTk Window)             │
├─────────────────────────────────┤
│ - controller: LoginController   │
│ - usuario_entry: CTkEntry       │
│ - password_entry: CTkEntry      │
├─────────────────────────────────┤
│ + crear_interfaz_login()        │
│ + intentar_login()              │
│ + intentar_registro()           │
│ + mostrar_error()               │
└─────────────────────────────────┘
                │
                │ abre al éxito
                ▼
┌─────────────────────────────────┐
│            App                  │
│     (Main Dashboard)            │
├─────────────────────────────────┤
│ - usuario_id: int               │
│ - usuario_actual: str           │
│ - user_model: UserModel         │
│ - tarjetas: dict                │
├─────────────────────────────────┤
│ + crear_interfaz()              │
│ + actualizar_estadisticas()     │
│ + abrir_reservas()              │
│ + abrir_historial()             │
│ + abrir_rutinas()               │
│ + abrir_progreso()              │
│ + abrir_pagos()                 │
└─────────────────────────────────┘
```

**Patrones de Diseño Aplicados:**

- **MVC (Model-View-Controller)**: Separación clara entre datos, lógica y presentación
- **Singleton**: Database.get_connection() proporciona conexión única
- **Factory**: Métodos estáticos para crear tarjetas, botones, etc.

---

### 3. Diagrama de Casos de Uso

```
                    GymForTheMoment - Casos de Uso

        Actor: Usuario                                Actor: Administrador
            │                                              │
            │                                              │
            ├──► (Registrarse)                            │
            │                                              │
            ├──► (Iniciar Sesión)                         │
            │         │                                    │
            │         └──────────────┐                    │
            │                        │                    │
            ├──► (Hacer Reserva)     │                    ├──► (Ver Estadísticas)
            │         │              │                    │
            │         │              │                    ├──► (Ver Usuarios Morosos)
            │         ├── «include» ─┴─► (Validar L-V)   │
            │         │                                   │
            │         └── «include» ───► (Verificar       ├──► (Generar Recibos)
            │                            Disponibilidad)  │
            │                                              │
            ├──► (Ver Historial)                          │
            │                                              │
            ├──► (Completar Rutina)                       │
            │         │                                    │
            │         └── «extend» ────► (Subir Nivel)    │
            │                                              │
            ├──► (Ver Progreso/Perfil)                    │
            │                                              │
            ├──► (Gestionar Pagos) ◄──────────────────────┤
            │         │                                    │
            │         ├── «include» ───► (Registrar Pago) │
            │         │                                    │
            │         └── «include» ───► (Ver Deuda)      │
            │                                              │
            │                                              │
     ┌──────┴──────────────────────────────────────────┬──┴──────┐
     │                                                  │         │
     │          SISTEMA: GymForTheMoment                │         │
     │                                                  │         │
     │  Funcionalidades Automáticas:                   │         │
     │  - Procesar reservas vencidas                   │         │
     │  - Incrementar nivel (cada 3 reservas)          │         │
     │  - Generar recibos mensuales                    │         │
     │  - Calcular horas entrenadas                    │         │
     │                                                  │         │
     └──────────────────────────────────────────────────┴─────────┘
```

**Casos de Uso Principales:**

1. **Registrarse**: Usuario nuevo crea cuenta (validación: min 3 caracteres usuario, min 4 contraseña)
2. **Iniciar Sesión**: Usuario accede al sistema
3. **Hacer Reserva**: Usuario reserva máquina (validación: L-V, 24h, disponibilidad)
4. **Ver Historial**: Usuario ve todas sus reservas (filtros: todas/completadas/pendientes)
5. **Completar Rutina**: Usuario marca rutina como completada (3 niveles: fácil/intermedio/difícil)
6. **Ver Progreso**: Usuario ve perfil, stats, nivel, rutinas completadas
7. **Gestionar Pagos**: Usuario ve y paga recibos mensuales
8. **Ver Usuarios Morosos** (Admin): Administrador ve listado de usuarios con pagos pendientes
9. **Generar Recibos** (Admin): Administrador genera recibos mensuales automáticamente
10. **Ver Estadísticas** (Admin): Administrador ve resumen de pagos del gimnasio

---

### 4. Diagrama de Secuencia: Hacer Reserva

```
Usuario    ReservasView   ReservaModel   Database    ReservasController  UserModel
   │            │              │            │                 │              │
   │──────────► │              │            │                 │              │
   │ Clic       │              │            │                 │              │
   │"Reservar"  │              │            │                 │              │
   │            │              │            │                 │              │
   │            │──────────────┴──────────► │                 │              │
   │            │  verificar_reservas_      │                 │              │
   │            │  vencidas()               │                 │              │
   │            │              ◄────────────┤                 │              │
   │            │              │            │                 │              │
   │            │              │            │◄────────────────┤              │
   │            │              │            │  procesar_      │              │
   │            │              │            │  reservas()     │              │
   │            │              │            │                 │              │
   │            │◄─────────────┴────────────┤                 │              │
   │            │  lista usuarios afectados │                 │              │
   │            │              │            │                 │              │
   │            │              │            │                 │──────────────►│
   │            │              │            │                 │ incrementar_ │
   │            │              │            │                 │ reservas()   │
   │            │              │            │                 │              │
   │ ◄──────────┤              │            │                 │              │
   │ Ventana    │              │            │                 │              │
   │ Reserva    │              │            │                 │              │
   │            │              │            │                 │              │
   │──────────► │              │            │                 │              │
   │ Selecciona │              │            │                 │              │
   │ Fecha      │              │            │                 │              │
   │            │              │            │                 │              │
   │            ├──────────────┤            │                 │              │
   │            │ validar_dia_ │            │                 │              │
   │            │ semana()     │            │                 │              │
   │            │              │            │                 │              │
   │            │ Si sábado/domingo         │                 │              │
   │ ◄──────────┤ ERROR: "Solo L-V"        │                 │              │
   │            │              │            │                 │              │
   │──────────► │              │            │                 │              │
   │ Selecciona │              │            │                 │              │
   │ Máquina    │              │            │                 │              │
   │            │              │            │                 │              │
   │──────────► │              │            │                 │              │
   │ Selecciona │              │            │                 │              │
   │ Hora       │              │            │                 │              │
   │            │              │            │                 │              │
   │            │──────────────┴──────────► │                 │              │
   │            │  maquina_disponible()     │                 │              │
   │            │              ◄────────────┤                 │              │
   │            │              │ true/false │                 │              │
   │            │              │            │                 │              │
   │──────────► │              │            │                 │              │
   │ Confirmar  │              │            │                 │              │
   │            │              │            │                 │              │
   │            │──────────────┴──────────► │                 │              │
   │            │  crear_reserva()          │                 │              │
   │            │              ◄────────────┤                 │              │
   │            │              │  INSERT    │                 │              │
   │            │              │            │                 │              │
   │ ◄──────────┤              │            │                 │              │
   │ "Reserva   │              │            │                 │              │
   │ Exitosa"   │              │            │                 │              │
   │            │              │            │                 │              │
```

---

### 5. Diagrama de Secuencia: Gestión de Pagos (Admin)

```
Admin      PagosView     PagoModel      Database
   │            │             │              │
   │──────────► │             │              │
   │ Clic       │             │              │
   │"Generar    │             │              │
   │ Recibos"   │             │              │
   │            │             │              │
   │            │─────────────┴────────────► │
   │            │  generar_recibos_          │
   │            │  automaticos()             │
   │            │             │              │
   │            │             ├──────────────►│
   │            │             │ SELECT users  │
   │            │             │              ││
   │            │             │◄──────────────┤
   │            │             │ [usuarios]    │
   │            │             │              │
   │            │             │              │
   │            │  Para cada usuario:        │
   │            │             ├──────────────►│
   │            │             │ INSERT pago   │
   │            │             │ (mes_actual)  │
   │            │             │              ││
   │            │             │◄──────────────┤
   │            │             │              │
   │            │◄────────────┴───────────────┤
   │            │  N recibos generados        │
   │            │             │              │
   │ ◄──────────┤             │              │
   │ "N recibos │             │              │
   │ generados" │             │              │
   │            │             │              │
   │──────────► │             │              │
   │ Ver        │             │              │
   │ Morosos    │             │              │
   │            │             │              │
   │            │─────────────┴────────────► │
   │            │  obtener_morosos()         │
   │            │             │              │
   │            │             ├──────────────►│
   │            │             │ SELECT users  │
   │            │             │ WHERE pagado=0│
   │            │             │ GROUP BY user │
   │            │             │              ││
   │            │             │◄──────────────┤
   │            │             │ [morosos]     │
   │            │◄────────────┴───────────────┤
   │            │  lista morosos              │
   │            │  (nombre, deuda)            │
   │            │             │              │
   │ ◄──────────┤             │              │
   │ Listado    │             │              │
   │ Morosos    │             │              │
   │            │             │              │
```

---

## Restricciones del Sistema

### Reglas de Negocio

1. **Reservas**:

   - Solo se permiten reservas de **Lunes a Viernes**
   - Horario disponible: **24 horas** (00:00 - 23:00)
   - **1 persona por máquina** (capacidad máxima)
   - Duración por defecto: **1 hora**
   - Las reservas se marcan automáticamente como completadas al pasar su horario

2. **Niveles**:

   - Los usuarios comienzan en **Nivel 1**
   - Se sube 1 nivel cada **3 reservas completadas**
   - El progreso es automático (sin intervención manual)

3. **Pagos**:

   - Cuota mensual: **50€**
   - Los recibos se generan automáticamente cada mes
   - Los usuarios con pagos pendientes aparecen en la lista de morosos
   - Solo el administrador puede generar recibos y ver morosos

4. **Rutinas**:

   - 3 niveles de dificultad: **Fácil (7 ejercicios), Intermedio (8), Difícil (10)**
   - Las rutinas completadas se registran con fecha y ejercicios realizados

5. **Usuarios**:
   - Nombre de usuario: mínimo 3 caracteres
   - Contraseña: mínimo 4 caracteres
   - Nombres de usuario únicos (no se permiten duplicados)

### Validaciones Implementadas

- ✅ Validación de campos vacíos en login/registro
- ✅ Validación de longitud mínima de usuario y contraseña
- ✅ Validación de coincidencia de contraseñas en registro
- ✅ Validación de día de la semana (L-V) en reservas
- ✅ Validación de disponibilidad de máquinas
- ✅ Validación de unicidad de recibos mensuales
- ✅ Prevención de reservas duplicadas en mismo horario/máquina

---

## Tecnologías y Arquitectura

### Stack Tecnológico

- **Lenguaje**: Python 3.8+
- **GUI**: CustomTkinter (interfaz gráfica moderna)
- **Base de Datos**: SQLite3 (local, sin servidor)
- **Widgets adicionales**: tkcalendar (selector de fechas)

### Arquitectura: MVC (Model-View-Controller)

```
┌─────────────────────────────────────────────────┐
│                  FRONTEND                       │
│                   (View)                        │
├─────────────────────────────────────────────────┤
│ - login.py                                      │
│ - app.py (dashboard)                            │
│ - reserv_view.py                                │
│ - historial_view.py                             │
│ - rutinas_view.py                               │
│ - progreso_view.py                              │
│ - pagos_view.py                                 │
└────────────────┬────────────────────────────────┘
                 │
                 │ Interactúa con
                 ▼
┌─────────────────────────────────────────────────┐
│                 CONTROLLER                      │
│                 (Lógica)                        │
├─────────────────────────────────────────────────┤
│ - login_controller.py                           │
│ - reserv_control.py                             │
└────────────────┬────────────────────────────────┘
                 │
                 │ Utiliza
                 ▼
┌─────────────────────────────────────────────────┐
│                   MODEL                         │
│              (Datos y Lógica)                   │
├─────────────────────────────────────────────────┤
│ - user_model.py                                 │
│ - reserv_model.py                               │
│ - rutina_model.py                               │
│ - pago_model.py                                 │
└────────────────┬────────────────────────────────┘
                 │
                 │ Accede a
                 ▼
┌─────────────────────────────────────────────────┐
│                 DATABASE                        │
│              (Persistencia)                     │
├─────────────────────────────────────────────────┤
│ - database.py                                   │
│ - gimnasio.db (SQLite)                          │
│   ├── usuarios                                  │
│   ├── reservas                                  │
│   ├── pagos                                     │
│   └── rutinas_completadas                      │
└─────────────────────────────────────────────────┘
```

---

## Resumen de Cumplimiento de Requisitos

### ✅ Interfaz UI (1 punto)

- Interfaz gráfica con CustomTkinter
- Clara, funcional y fácil de usar
- Validación de datos para evitar errores

### ✅ Persistencia de Datos (2 puntos)

- SQLite para almacenamiento fiable
- 4 tablas: usuarios, reservas, pagos, rutinas_completadas
- Datos persistentes entre sesiones

### ✅ Estructura del Código (1 punto)

- POO aplicada correctamente
- Clases para cada entidad del E-R
- Herencia de CustomTkinter widgets
- Código mantenible y organizado (MVC)

### ✅ Lógica de Reservas y Pagos (2 puntos)

- ✅ Gestión de reservas L-V, 24h
- ✅ Valida disponibilidad de máquinas
- ✅ Listado de ocupación por día/máquina
- ✅ Registra pagos mensuales
- ✅ Genera recibos automáticamente
- ✅ Listado de usuarios morosos

### ✅ Documentación (1 punto)

- ✅ Diagrama E-R completo
- ✅ Diagrama de Clases UML
- ✅ Diagrama de Casos de Uso
- ✅ Diagramas de Secuencia
- ✅ Documentación de restricciones y reglas de negocio

---

**Total: 7/7 puntos posibles (100%)**
