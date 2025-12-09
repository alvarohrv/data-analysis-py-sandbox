# 🟦 **APUNTES DE NUMPY — NIVEL BASE A INTERMEDIO**

## 1. ¿Qué es NumPy y para qué sirve?

NumPy (“Numerical Python”) es una librería diseñada para:

* Trabajar con **vectores**, **matrices** y **arreglos n-dimensionales**.
* Hacer operaciones matemáticas muy rápidas gracias a código optimizado en C.
* Base de casi todo el ecosistema científico de Python (Pandas, Scikit-Learn, etc).

❗ **Pandas usa NumPy por debajo**, siempre.
Por eso, aunque instales Pandas, también tienes NumPy instalado — o se instala automáticamente.

### ¿Por qué no basta con Python puro?

* Las **listas** son lentas para cálculos numéricos.
* No permiten operaciones vectorizadas.
* Cada elemento puede ser de un tipo distinto.
* NumPy aprovecha optimizaciones de CPU y memoria.

---

## 🟩 2. Creación de arreglos (ndarrays)

```python
import numpy as np

a = np.array([2, 3, 7, 8, 5])
type(a) # numpy.ndarray
# a.dtype # dtype('int32')

```

### Propiedades importantes:

```python
a.dtype   # tipo de dato (int32, float64...)
a.size    # cantidad total de elementos
a.ndim    # número de dimensiones (1 para vector)
a.shape   # tupla con la forma (5,)  ← 5 elementos en 1D
```

### Características del ndarray

* Similar a una lista, pero:

  * Tiene **tipo homogéneo**.
  * Es **más rápido**.
  * Tiene **dimensión fija**.

---

## 🟦 3. Indexación y slicing

```python
a[0]       # primer elemento
a[-1]      # último elemento
a[1:4]     # elementos 1, 2, 3
a[::-1]    # arreglo invertido
```

---

## 🟥 4. Operaciones vectorizadas (gran ventaja de NumPy)

NumPy permite operar vectores **sin ciclos for**.

### Suma y resta de vectores

```python
u = np.array([0, 1])
v = np.array([1, 0])
z = u + v     # array([1, 1])
# z = np.add(u, v)
```

~~~py
arr1 = np.array([10, 11, 12, 13, 14, 15])
arr2 = np.array([20, 21, 22, 23, 24, 25])
arr3 = np.add(arr1, arr2)
print(arr3)
~~~
### Suma con escalar

```python
u = np.array([1, 3, -1, 2])
z = u + 1     # array([2, 4, 0, 3])
```

### The operation is equivalent to vector addition:
~~~py
# Plotting functions


import time 
import sys
import numpy as np 

import matplotlib.pyplot as plt

u = np.array([1, 0])
v = np.array([0, 1])
z = np.add(u, v)

def Plotvec1(u, z, v):
    
    ax = plt.axes() # to generate the full window axes
    ax.arrow(0, 0, *u, head_width=0.05, color='r', head_length=0.1)# Add an arrow to the  U Axes with arrow head width 0.05, color red and arrow head length 0.1
    plt.text(*(u + 0.1), 'u')#Adds the text u to the Axes 
    
    ax.arrow(0, 0, *v, head_width=0.05, color='b', head_length=0.1)# Add an arrow to the  v Axes with arrow head width 0.05, color red and arrow head length 0.1
    plt.text(*(v + 0.1), 'v')#Adds the text v to the Axes 
    
    ax.arrow(0, 0, *z, head_width=0.05, head_length=0.1)
    plt.text(*(z + 0.1), 'z')#Adds the text z to the Axes 
    plt.ylim(-2, 2)#set the ylim to bottom(-2), top(2)
    plt.xlim(-2, 2)#set the xlim to left(-2), right(2)


    Plotvec1(u, z, v)
    ~~~

### Multiplicación por escalar

```python
y = np.array([1, 3])
z = 2 * y     # array([2, 6])
```

---

## 🟧 5. Producto Hadamard (multiplicación elemento a elemento)

```python
u = np.array([1, 2])
v = np.array([3, 2])
z = u * v     # array([3, 4])
```

~~~py
arr1 = np.array([10, 20, 30, 40, 50, 60])
arr2 = np.array([2, 1, 2, 3, 4, 5])
arr3 = np.multiply(arr1, arr2)
print(arr3) # [ 20  20  60 120 200 300]

# c = np.divide(a, b)
~~~
---

## 🟪 6. Producto Punto (Dot Product)

```python
u = np.array([1, 2])
v = np.array([3, 2])

z = np.dot(u, v)  
# (1*3 + 2*2) = 7

u = np.array([-1, 1])
v = np.array([1, 1])

z = np.dot(u, v)  
# (-1 + (1)) = 0



```

### ¿Para qué se usa el producto punto?

* Ángulos entre vectores.
* Longitudes y proyecciones.
* Motores gráficos (3D).
* Redes neuronales y machine learning.
* Transformaciones lineales.

Es una **operación fundamental** en álgebra lineal.

---

## 🟨 7. Broadcasting

El *broadcasting* es cuando NumPy “expande” automáticamente las dimensiones necesarias para que dos arreglos puedan operar entre sí.

Ejemplo típico:

```python
a = np.array([1, 2, 3])
b = 2

a + b     # array([3, 4, 5])
```

Ejemplo más complejo:

```python
A = np.array([[1,2,3],
              [4,5,6]])

v = np.array([10, 20, 30])

A + v
```

NumPy replica `v` verticalmente para hacer la suma.

---

## 8. Funciones universales (ufuncs)

Son funciones optimizadas en C que operan **elemento a elemento**.

Ejemplos:

```python
a.mean()
a.max()
a.min()
np.sin(a)
```

### Otros muy usados

```python
np.sqrt(a)
np.exp(a)
np.log(a)
np.sum(a)
np.std(a)
```

---

## 🟩 9. Creación de arreglos útiles

### Rango lineal

```python
np.linspace(0, 1, 5)
# array([0., 0.25, 0.5, 0.75, 1.])
```

### Rango con paso fijo

```python
np.arange(0, 10, 2)
```

### Arreglo de ceros o unos

```python
np.zeros(5)
np.ones((2,3))
```

### Matrices identidad

```python
np.eye(3)
```

---

## 🟦 10. Reshape (cambiar forma del arreglo)

Muy útil en Machine Learning.

```python
a = np.array([1,2,3,4,5,6])
a.reshape(2,3)
```

---

## 🟣 11. ¿Qué tema matemático debería repasar para entender esto mejor?

Para manejar NumPy con soltura es útil repasar:

* **Álgebra lineal básica**

  * vectores y matrices
  * suma y resta
  * producto punto
  * magnitud de un vector
  * matriz identidad, transpuesta

* **Sistema de coordenadas**

  * representación gráfica de vectores
  * suma de vectores como desplazamientos

No necesitas nada avanzado; solo lo que se ve en los primeros capítulos de álgebra lineal.

---

## 🟧 12. ¿Por qué se explicó la suma de vectores en el plano cartesiano?

Porque visualmente ayuda a entender:

* Qué es un vector
* Qué significa sumarlos
* Cómo se comporta NumPy cuando suma `array`s

La suma `u + v = z` representa que si partes del origen:

📌 te mueves como `u`
📌 luego como `v`
📌 terminas en `z`

Es un concepto matemático importante en física, estadística y ML.

---

