---
name: Dates MVP - siempre confirmar plan antes de codear
description: En el proyecto Dates MVP el usuario exige que Claude proponga un plan y espere luz verde antes de hacer cambios de código
type: feedback
---

REGLA: En el proyecto Dates MVP (/home/dev2salogaash/Documentos/cloude/dates/), cada vez que el usuario pida un cambio, Claude debe PRIMERO explicar el plan (qué archivos, qué cambios, qué enfoque) y ESPERAR confirmación explícita ("va", "dale", "hazlo", "luz verde") antes de tocar código.

**Why:** El usuario lo pidió textualmente: "siempre que te pida un cambio me preguntas primero me dices cual sera el plan para ver si te doy luz verde o nel". Quiere controlar el alcance y evitar que Claude se lance solo.

**How to apply:** Ante cualquier petición de cambio en este proyecto → responder con plan + preguntar "¿le entro?". No usar Edit/Write hasta tener OK. Excepciones razonables: comandos de lectura, levantar servidores, lint/tests, y fixes triviales si el usuario ya dio OK general.
