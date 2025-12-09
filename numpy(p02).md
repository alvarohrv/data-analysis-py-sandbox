
# 🟦 **Matrices 2D en NumPy (ndarray)**
En NumPy, una **matriz 2D** es simplemente un `ndarray` con `ndim = 2`, es decir:
* Tiene **filas** y **columnas**
* Se representa como una lista de listas
* Es la base para trabajar algebra lineal básica

## 🔹1. Crear una matriz 2D

```python
import numpy as np

A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(A)
# [[1 2 3] [4 5 6]]
```
### 🔹 Propiedades importantes

```python
print(A.ndim)   # 2  # número de dimensiones
print(A.shape)  # (2, 3) # (filas, columnas)
print(A.size)   # 6 # total de elementos filas × columnas
print(A.dtype)  # int64 (depende del sistema) # tipo de dato
```

---

## 🟩 **2. Indexación y Slicing en matrices 2D**

### Acceder a un elemento:
<!--
A[fila][columna]
A[fila, columna]  # forma recomendada
 -->
```python
A[0, 1]  # → 2
```
**a. Acceder a una fila:**
```python
A[0]         # fila completa
A[0, :]      # equivalente
```
**b. Acceder a una columna:**
```python
A[:, 1]      # columna 1 → [2,5]
```
### Submatriz (slicing):
```python
A[0:2, 1:3]   # filas 0-1, columnas 1-2
```

---

## 🟧 3 **Operaciones con matrices**

### 🔸 1. Suma y Resta (elemento a elemento)

Solo funciona si las matrices tienen **misma forma**.

```python
A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
B = np.array([
    [10, 10, 10],
    [20, 20, 20]
])

print(A + B)
print(A - B)
```

---

### 🔸 2. Multiplicación por escalar

```python
2 * A
```
Opera elemento a elemento.
<!-- [1*2, 2*2, 3*2], [4*2, 5*2, 6*2] -->

---

### 🔸 3. Producto Hadamard (multiplicación elemento a elemento)

Importante: requiere **misma shape**.

```python
A * B
```

---

### 🔸 4. Producto Punto (matricial)

Usa:
```python
A.dot(B)
# o
A @ B
```
### 💡 **Regla de las dimensiones:**

```
A tiene forma (m × n)
B tiene forma (n × p)
--------------------------------
A @ B → matriz de forma (m × p)
```

```
El primer paso que debes comprobar antes de realizar la multiplicación matricial entre dos matrices A y B de NumPy es:
El número de columnas de A debe ser igual al número de filas de B. (Requisito de Compatibilidad Dimensional)
de tal forma que:
Si A es una matriz de dimensión m*n y B es una matriz de dimensión p*q, la multiplicación A*B solo es posible si: n = p
```

### 🟥 Ejemplo completo con matrices NO cuadradas

Supongamos:

`A` es (3×2)
`B` es (2×3)

```python
A = np.array([
    [1, 2],
    [3, 4],
    [5, 6]
])  # (3x2)

B = np.array([
    [7, 8, 9],
    [10,11,12]
]) # (2x3)

C = A @ B
print(C)
print(C.shape)

# [[ 27  30  33]
#  [ 61  68  75]
#  [ 95 106 117]]

# (3, 3)
```
💡 Funciona porque **las columnas de A = 2** y **las filas de B = 2**.

---

### 🛑 ¿Qué pasa si las formas NO son compatibles?

Ejemplo:

* A es (3×2)
* B es (4×3)

Si intentas:
```python
A @ B
```
Obtendrás error:
```
ValueError: shapes (3,2) and (4,3) not aligned
```
Porque:
```
2 ≠ 4
```
Importante ❗ Para multiplicar matrices, el **número de columnas de la primera** debe ser igual al **número de filas de la segunda**.

---

