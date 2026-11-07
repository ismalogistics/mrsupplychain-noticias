# Guía visual del portal de Noticias · Mr. Supply Chain® México

Reglas para que cada publicación (briefs, tendencias, especiales) se vea igual que el diseño aprobado por Isma el 6 nov 2026.
**Toda tarea que publique en este repo debe leer y cumplir esta guía antes de hacer commit.**

## 1. Lo que cada brief debe traer (data/briefs/*.json y data/latest.json)

- `es`, `en` y `pt` llevan, además de `titular`, `bloques` y `scm`, el campo **`esencial`**: una lista de **exactamente 3 frases cortas**
  (máximo ~25 palabras cada una, con cifra concreta) que resumen el brief para quien sólo tiene 30 segundos:
  1. qué pasó (el dato principal), 2. por qué, 3. qué hacer o vigilar en supply chain.
  Mismas cifras en los tres idiomas. Se muestra como **"Lo esencial en 30 segundos"** debajo del titular (portada y página del brief).
  Si falta, el sitio usa la primera oración de cada bloque, que suele ser demasiado larga: no lo dejes vacío.
- `titular`: una sola frase de máximo ~20 palabras. No metas tres cifras en el titular; las demás van en `esencial`.
- Cada bloque (`bloques[].x`): 2 a 5 oraciones. El sitio los parte en párrafos de 2 oraciones; no escribas párrafos de 8 oraciones.
- `scm` con varios pasos: escríbelo como `Intro: 1) paso; 2) paso; 3) paso.` y el sitio lo muestra como lista numerada.

## 2. Tendencias, lectura y redes

- `data/tendencias.json`: el `id` de cada tarjeta decide su ilustración. Usa uno de:
  `semis`, `electricidad`, `laboral`, `puertos`, `energia`, `software`, `retail`; para otras industrias usa un id descriptivo
  (`autotransporte`, `aereo`, `mineria`, `automotriz`, `farma`, `agro`…): el sitio elige la ilustración por palabras del nombre y el titular.
  `x` = 2 o 3 frases (se recorta con "Leer más"); `scm` = una acción concreta.
- `lectura.temas[].tema`: nombre corto del frente ("Peso y tasas", "Energía y fletes", "Insumos e inventario", "Demanda y comercio",
  "Metales y electrónica"…). La ilustración sale de ese nombre.
- `data/redes.json` lo genera `scripts/feeds.py` (GitHub Action): guarda `img` cuando el medio publica foto. No lo edites a mano.

## 3. Componentes del diseño (no los quites ni los dupliques)

| Pieza | Dónde vive |
|---|---|
| Ilustraciones propias (portada por horario y región, industrias, temas) | `art.js` (`NXArt`) |
| Selector de región Global / LATAM / México con explicación | `index.html` (`.nx-tabwrap`, `.nx-tabinfo`) |
| "Lo esencial en 30 segundos" | `news.js` (`esencial()`), `scripts/build_static.py` (`esencial_html`) |
| Lectura de gráficos: recuadro grande "Qué significa para supply chain" | `news.js` (`interp()`) |
| Barra fija al bajar + botón "Arriba" | `ui.js` (se carga en portada, briefs, archivo y especiales) |
| Tarjeta promocional (especial, newsletter) | clases `.nx-promo` / `.nx-nl` en `news.css` |

- Fotos: sólo ilustraciones propias (`art.js`) o la foto que el propio medio publica en su feed. Nunca fotos de personas públicas ni imágenes de bancos sin licencia.
- Colores: azul `#1e4f9c` (acento), navy `#0b1f47`, Global `#1e5fa8`, LATAM `#1f8a5b`, México `#a83246`.
- Letra: títulos en serif; todo el texto de lectura en sans (`var(--sans)`), interlineado 1.6–1.75.
- Si cambias `news.css`, `news.js`, `art.js` o `ui.js`, sube su `?v=` en `index.html`, `scripts/build_static.py` y en el `build.py` de cada especial.

## 4. Especiales (`especiales/<slug>/`)

Todo especial nuevo debe:
- Cargar `../../news.css`, `../../static.js` y `../../ui.js` (barra fija y botón arriba) con la misma versión que la portada.
- Tener un índice `<nav class="ex-toc">` con anclas a sus secciones (la barra fija lo copia). No lo hagas `position: sticky`.
- Abrir con **"Lo esencial en 30 segundos"** (`<aside class="nx-ess">` con 3 frases) y, si hay resultado o análisis largo,
  mostrar el primer párrafo y el resto dentro de `<details class="nx-moreblk">` ("Leer el resultado completo").
- Usar texto sans en la prosa y párrafos de 2 oraciones (en el especial de elecciones: `blk_cortos()` de `build.py`).
- En la portada, anunciarse con la tarjeta `.nx-promo` (imagen + etiqueta + título + una línea + botón), no con estilos en línea.
  En el especial de elecciones, el resumen va en `RESULTADOS['esencial']` (3 frases L(es, en, pt)).

## 5. Revisión antes del push

1. `python scripts/build_static.py` (y el `build.py` del especial si lo tocaste).
2. Abre la portada, un brief y el especial con Playwright a 1280 y 390 px: sin errores de consola, sin desborde horizontal,
   y verifica que se vean la portada ilustrada, "Lo esencial en 30 segundos" y el selector de región.
