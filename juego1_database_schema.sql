CREATE TABLE juego1 (
     id SERIAL PRIMARY KEY,                         -- Identificador único para cada registro
     nombre_apellido TEXT,                          -- Nombre completo del jugador
     pais TEXT,                                     -- pais del jugador
     intentos INT NOT NULL,                         -- Número de intentos realizados
     resultado TEXT NOT NULL,                       -- Resultado del juego ('Ganó' o 'Perdió')
     played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Fecha y hora del intento
);

SELECT * FROM juego1;                               -- Query para ver los datos de la tabla.

DELETE FROM juego1 WHERE id = 1;                    -- Eliminar registro por ID
