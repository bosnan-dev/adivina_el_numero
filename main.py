import streamlit as st
import random
import os
import pandas as pd
from PIL import Image
from db_connection import db_connection

# Configuración de la página
st.set_page_config(page_title="🎮 Adivina el Número", page_icon="🎯", layout="centered")
st.title("🤔 Juego Adivina el Número 🔢")
st.markdown("---")


# Logo-Imagen y enlaces
col1, col2, col3 = st.columns([6, 6, 6])
with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <a href='https://www.linkedin.com/in/bcordovag/' target='_blank' style='text-decoration: none; font-size: 20px; color: #0a66c2; font-weight: bold;'>🔗 Conecta conmigo en LinkedIn</a>
        </div>
    """, unsafe_allow_html=True)

    image = Image.open('./img/logo.png')
    st.image(image, caption="✍️📝Creado por Brayan Córdova 📝✍️ 👨‍💻 aka. Bosnan DEv 👨‍💻", width=250)

    st.markdown("""
        <div style='text-align: center; margin-top: 10px;'>
            <a href='https://github.com/bcordovag/adivina-el-numero' target='_blank' style='text-decoration: none; font-size: 20px; color: yellow; font-weight: bold;'>📥 Descarga el código fuente en GitHub 📥</a>
        </div>
    """, unsafe_allow_html=True)
st.markdown("---")

# Conexión a la base de datos
try:
    Conexion, conexion = db_connection()
    st.success("✅ Conexión exitosa a la base de datos")
except Exception as e:
    st.error(f"❌ Error al conectar con la base de datos: {e}")
    st.stop()
st.markdown("---")

# Muestra ranking de últimas partidas
st.subheader("📊 Ranking de los Últimos 5 Jugadores 📊")
try:
    conexion.execute("SELECT nombre_apellido, pais, intentos, resultado, played_at FROM juego1 ORDER BY id DESC LIMIT 5")
    resultados = conexion.fetchall()
    df_resultados = pd.DataFrame(resultados, columns=["Nombre y Apellido", "País", "Intentos", "Resultado", "Fecha y Hora"])
    st.dataframe(df_resultados, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"❌ Error al obtener los datos: {e}")
    st.stop()
st.markdown("---")

# Variables del juego
for key, default in {
    "nombre": "", "apellido": "", "pais": "",
    "nombre_guardado": False,
    "numero_random": random.randint(1, 5),
    "intentos": 0, "intentos_permitidos": 3,
    "juego_terminado": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Datos del jugador
st.subheader("👤 Ingresa los datos solicitados en minúsculas para comenzar:")
nombre_input = st.text_input("Nombre:", value=st.session_state.nombre)
apellido_input = st.text_input("Apellido:", value=st.session_state.apellido)
pais_input = st.text_input("País:", value=st.session_state.pais)

if st.button("💾 Guardar datos"):
    if nombre_input.strip() and apellido_input.strip() and pais_input.strip():
        st.session_state.update({
            "nombre": nombre_input.strip().lower(),
            "apellido": apellido_input.strip().lower(),
            "pais": pais_input.strip().lower(),
            "nombre_guardado": True,
            "numero_random": random.randint(1, 5),
            "intentos": 0,
            "intentos_permitidos": 3,
            "juego_terminado": False
        })
        st.success(f"🙌 ¡Bienvenido, {st.session_state.nombre} {st.session_state.apellido}! Estás jugando desde {st.session_state.pais}.")
    else:
        st.warning("⚠️ Debes llenar todos los campos antes de continuar.")

# Juego principal
if st.session_state.nombre_guardado:
    st.title("🎲 Adivina el Número 🎲")
    st.markdown(f"Intenta adivinar el número entre 1 y 5. \n\nTienes: {st.session_state.intentos_permitidos} intentos.")
    jugador = st.number_input("Ingresa tu número:", min_value=1, max_value=5, step=1)

    if st.button("🎯 Intentar") and not st.session_state.juego_terminado:
        if st.session_state.intentos_permitidos > 0:
            st.session_state.intentos += 1
            st.session_state.intentos_permitidos -= 1

            if jugador < st.session_state.numero_random:
                st.warning(f"🔼 El número es mayor.\nIntentos restantes: {st.session_state.intentos_permitidos}")
            elif jugador > st.session_state.numero_random:
                st.warning(f"🔽 El número es menor.\nIntentos restantes: {st.session_state.intentos_permitidos}")
            else:
                st.success(f"🎉 ¡Correcto! Lo lograste en {st.session_state.intentos} intentos.")
                st.session_state.juego_terminado = True
                try:
                    conexion.execute(
                        "INSERT INTO juego1 (nombre_apellido, pais, intentos, resultado) VALUES (%s, %s, %s, %s)",
                        (f"{st.session_state.nombre} {st.session_state.apellido}", st.session_state.pais, st.session_state.intentos, "Ganó")
                    )
                    Conexion.commit()
                except Exception as e:
                    st.error(f"❌ Error al guardar en la base de datos: {e}")

        if st.session_state.intentos_permitidos == 0 and jugador != st.session_state.numero_random:
            st.error(f"❌ ¡Has perdido! El número correcto era: {st.session_state.numero_random}")
            st.session_state.juego_terminado = True
            try:
                conexion.execute(
                    "INSERT INTO juego1 (nombre_apellido, pais, intentos, resultado) VALUES (%s, %s, %s, %s)",
                    (f"{st.session_state.nombre} {st.session_state.apellido}", st.session_state.pais, st.session_state.intentos, "Perdió")
                )
                Conexion.commit()
            except Exception as e:
                st.error(f"❌ Error al guardar en la base de datos: {e}")

    if st.session_state.juego_terminado:
        if st.button("🔄 Volver a jugar"):
            for key in ["nombre", "apellido", "pais", "nombre_guardado", "juego_terminado"]:
                st.session_state[key] = "" if isinstance(st.session_state[key], str) else False
            st.session_state.intentos_permitidos = 3
            st.session_state.intentos = 0
            st.session_state.numero_random = random.randint(1, 5)
            st.success("🌀 El juego ha sido reiniciado. Ingresa tus datos nuevamente para jugar.")
