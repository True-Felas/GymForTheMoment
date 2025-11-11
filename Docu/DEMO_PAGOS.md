# 🎯 Demostración del Sistema de Pagos

## Configuración Automática

El sistema de pagos está configurado para **generar automáticamente recibos de ejemplo** cuando accedes a la sección de pagos por primera vez. Esto facilita la demostración sin necesidad de configuración manual.

---

## 📋 ¿Qué se genera automáticamente?

Cuando abres la vista de pagos, el sistema genera automáticamente:

### Para TODOS los usuarios:

1. **Recibo del mes actual** (Noviembre 2025) - **PENDIENTE** ❌
2. **Recibo del mes anterior** (Octubre 2025) - **PAGADO** ✅ (solo admin y juan)
3. **Recibo de hace 2 meses** (Septiembre 2025) - **PAGADO** ✅ (todos)

Esto crea una **demostración visual inmediata** que muestra:

- ✅ Recibos pagados (con fecha de pago)
- ❌ Recibos pendientes (deuda actual)
- 📊 Usuarios morosos (tienen pagos pendientes)

---

## 🎬 Cómo Demostrar el Sistema

### 1️⃣ **Vista de Usuario Normal**

**Login**: `juan` / `gym2025`

1. Hacer clic en **"Mis Pagos"**
2. Verás automáticamente:

   - ✅ **2 recibos PAGADOS** (Septiembre y Octubre)
   - ❌ **1 recibo PENDIENTE** (Noviembre - 50€)
   - **Resumen**: 3 recibos totales | 1 pendiente | Deuda: 50.00€

3. **Para pagar un recibo pendiente**:
   - Clic en el botón **"Pagar"** del recibo de Noviembre
   - Aparece mensaje: "¡Pago registrado con éxito!"
   - El recibo se marca como PAGADO
   - La deuda desaparece

**Resultado visual**:

- Los recibos pagados aparecen con **borde verde** y icono **[OK]**
- Los pendientes con **borde rojo** y icono **[!]**

---

### 2️⃣ **Vista de Administrador**

**Login**: `admin` / `1234`

1. Hacer clic en **"Mis Pagos"**
2. Verás **3 pestañas** con información completa:

#### 📊 **Pestaña 1: Estadísticas**

```
┌─────────────────────────────────┐
│ Resumen General de Pagos        │
├─────────────────────────────────┤
│ Recibos Generados:      9       │
│ Pagos Realizados:       7       │
│ Pagos Pendientes:       2       │
│ Recaudado:         350.00€      │
│ Pendiente:         100.00€      │
└─────────────────────────────────┘
```

#### ⚠️ **Pestaña 2: Usuarios Morosos**

Muestra usuarios con pagos pendientes:

```
┌──────────────────────────────────────┐
│ [!] Usuario: sofia                   │
│     Pagos pendientes: 1              │
│     Deuda total: 50.00€              │
│     [Ver Detalles]                   │
└──────────────────────────────────────┘
```

Al hacer clic en **"Ver Detalles"**, muestra:

- Lista de recibos pendientes por mes
- Noviembre 2025: 50.00€

#### 📝 **Pestaña 3: Generar Recibos**

```
┌──────────────────────────────────────┐
│ Generación Automática de Recibos     │
│                                      │
│ Genera recibos mensuales para todos │
│ los usuarios.                        │
│ Cuota: 50€/mes                       │
│                                      │
│ Se generarán recibos de los últimos │
│ 3 meses para demostración.           │
│                                      │
│ Mes actual: Noviembre 2025           │
│                                      │
│ [Generar Recibos del Mes Actual]     │
└──────────────────────────────────────┘
```

Al hacer clic en **"Generar Recibos"**:

- Genera recibos para todos los usuarios
- Muestra: "[OK] Se generaron X recibos exitosamente"
- La vista se actualiza automáticamente

---

## 🔍 Escenarios de Demostración

### Escenario 1: Usuario con Deuda

1. Login como `sofia` / `fitlife`
2. Ir a "Mis Pagos"
3. Ver recibos pendientes claramente marcados en **ROJO**
4. Pagar el recibo de Noviembre
5. Ver confirmación visual
6. Actualizar vista: recibo ahora en **VERDE**

### Escenario 2: Administrador Gestionando Morosos

1. Login como `admin` / `1234`
2. Ir a "Mis Pagos" → Pestaña "Usuarios Morosos"
3. Ver que `sofia` aparece como morosa (antes de pagar)
4. Después de que sofia pague, la lista se actualiza
5. Si no hay morosos: "¡Excelente! No hay usuarios con pagos pendientes"

### Escenario 3: Generación de Recibos

1. Login como `admin`
2. Ir a "Mis Pagos" → Pestaña "Generar Recibos"
3. Clic en "Generar Recibos del Mes Actual"
4. Sistema genera recibos de los últimos 3 meses
5. Mensaje: "Se generaron X recibos exitosamente"
6. Ver estadísticas actualizadas

---

## 💡 Características Visuales

### Indicadores de Color

- 🟢 **Verde**: Recibo PAGADO
- 🔴 **Rojo**: Recibo PENDIENTE
- 🟡 **Amarillo**: Botón "Pagar" (acción requerida)

### Iconos

- **[OK]**: Pago completado
- **[!]**: Pago pendiente / Usuario moroso
- **[€]**: Dinero recaudado/pendiente
- **[R]**: Recibos generados

### Información Visible

Cada tarjeta de pago muestra:

- Mes y año
- Monto (50€)
- Estado (PAGADO/PENDIENTE)
- Fecha de pago (si está pagado)
- Botón "Pagar" (si está pendiente)

---

## 📈 Datos de Ejemplo Generados

Con 3 usuarios (admin, juan, sofia):

**Total de recibos**: 9 (3 usuarios × 3 meses)

**Distribución**:

- ✅ **7 pagos realizados** (Septiembre: 3, Octubre: 4)
- ❌ **2 pagos pendientes** (Noviembre: juan y sofia tienen pendiente)
- 💰 **Recaudado**: 350€ (7 × 50€)
- 📊 **Pendiente**: 100€ (2 × 50€)

**Usuarios morosos iniciales**: 2 (juan y sofia con Noviembre pendiente)

---

## 🎯 Puntos Clave para el Profesor

1. **Automatización Total**:

   - No requiere configuración manual
   - Los recibos se generan al abrir la vista
   - Datos de ejemplo listos para demostrar

2. **Interfaz Visual Clara**:

   - Colores distintivos (verde/rojo)
   - Información organizada
   - Fácil de entender de un vistazo

3. **Funcionalidad Completa**:

   - Generación de recibos ✅
   - Registro de pagos ✅
   - Listado de morosos ✅
   - Estadísticas en tiempo real ✅

4. **Casos de Uso Reales**:
   - Usuario normal: ver y pagar sus recibos
   - Administrador: gestión completa
   - Morosos: lista actualizada dinámicamente

---

## 🚀 Inicio Rápido para Demostración

```bash
# 1. Ejecutar la aplicación
python main.py

# 2. Login como usuario normal
Usuario: juan
Password: gym2025
→ Clic en "Mis Pagos"
→ Ver recibos y pagar pendiente

# 3. Login como administrador
Usuario: admin
Password: 1234
→ Clic en "Mis Pagos"
→ Explorar 3 pestañas
→ Generar recibos
→ Ver morosos
```

---

## ✨ Resumen

El sistema de pagos está **completamente funcional y auto-demostrable**:

- ✅ Se generan **datos de ejemplo automáticamente**
- ✅ **Interfaz visual clara** con colores y estados
- ✅ **3 perspectivas**: Usuario, Admin, Morosos
- ✅ **Funciones completas**: Generar, Pagar, Consultar
- ✅ **Estadísticas en tiempo real**
- ✅ **Validaciones y mensajes informativos**

**Todo listo para demostrar sin configuración adicional!** 🎉
