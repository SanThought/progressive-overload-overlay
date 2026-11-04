# progressive-overload-overlay

Fuentes confiables y datos precisos dibujados sobre el espacio en blanco de un video
vertical (0:28, español) sobre carga progresiva en el gimnasio, con subtítulos en
inglés sincronizados y una intro/outro de 5 s. Proyecto hermano de
[ozempic-epigenetica-overlay](https://github.com/SanThought/ozempic-epigenetica-overlay).

## Qué es

El video fuente es un plano fijo de una persona hablando a cámara; el tercio superior
del cuadro es pared vacía. El proyecto dibuja ahí, en tiempo con el habla: 4 tarjetas
de datos con fuente (PROGRESSIVE OVERLOAD, THE 2-10% RULE, STRENGTH FAVORS HEAVY,
HYPERTROPHY: EITHER LOAD), una intro y un outro con las referencias completas.

## Pipeline (determinista por timecode)

1. `build.py` — genera las tarjetas PNG (Pillow, Space Grotesk + Inter, OFL),
   los subtítulos `subs.ass` y el filtergraph `graph.txt` (incluye un freeze-frame de 1.6 s al final del habla para que la última tarjeta se pueda leer); luego invoca ffmpeg:
   intro 5 s + video con overlays y subtítulos quemados + outro 5 s, concatenados.
2. `timeline.json` — mapa de escenas ↔ beats del habla y cómo se derivó el timing
   (faster-whisper `small`, `word_timestamps=True`, idioma `es`).
3. `sources.md` — las tres referencias con citas verbatim y URLs verificadas.

## Regla de sincronía

Cada tarjeta entra y sale sobre las frases que la nombran: THE 2-10% RULE aparece con
"controlo 10 kg en sentadilla"; STRENGTH LOVES HEAVY con "desarrollar un poco más de
fuerza"; HYPERTROPHY: ANY LOAD con "generar hipertrofia". Los subtítulos ingleses se
parten por frase sobre los timestamps de palabra, no por estimación.

## Archivos

- Render final: `final.mp4` (38.5 s, 474x850, 30 fps, ~5.3 MB).
- Las PNG de las tarjetas no se suben: las regenera el paso 1.
- El video fuente no se incluye (material privado de la conversación).
