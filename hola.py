import streamlit as st


# Configuración de la página
st.set_page_config(page_title="Agenda de Contactos", layout="wide")

# Títulos principales
st.markdown("# :green[AGENDA DE GERARDO]")
st.header("Agenda exclusiva de Gera ")

st.markdown("## :green[Descripción de las opciones disponibles]")
st.markdown("""
 - **Opción 1**: Muestra solo los nombres de los contactos registrados.
 - **Opción 2**: Permite seleccionar un contacto y ver su teléfono, correo, dirección y red social.
 - **Opción 3**: Muestra toda la información detallada de todos los contactos
 - **Opción 4**: Te permite agregar personas y datos a la agenda
 - **Opción 5**: Eliminar contactos → Te permite eliminar personas que estan en la agenda
""")

opcion = st.text_input("introduce la opcion que deseas usar:")
st.divider() # Línea separadora


if "agenda" not in st.session_state:
    st.session_state.agenda = [
        ["Juan Pérez"],
    ]

if "datos" not in st.session_state:
    st.session_state.datos = {
        "Juan Pérez": {"Numero": "555-0001", "Correo": "juan@correo.com", "Direccion": "Calle Morelos #123, Ciudad Guzmán", "Instagram": "@juanp_123"},
    }

if "datos_tuplas" not in st.session_state:
    st.session_state.datos_tuplas = [
        ("Juan Pérez", "555-0001", "juan@correo.com", "Calle Morelos #123, Ciudad Guzmán", "@juanp_123"),
    ]

agenda = st.session_state.agenda
datos = st.session_state.datos
datos_tuplas = st.session_state.datos_tuplas

limpia = sorted(list(set(datos_tuplas)))


#Datos que muestran segun la opcion

# Opción 1: Ver lista simple de contactos
if opcion == "1":
    st.markdown(":blue[agenda]")
    st.subheader("Lista de contactos")
    st.table(agenda)

# Opción 2: Consultar datos completos de un contacto
elif opcion == "2":
    st.subheader("Consultar datos de los contactos")
    
    vistos = set()
    contactos_limpios = {}

    for nombre, info in datos.items():
        identificador = (info["Numero"], info["Correo"], info["Direccion"], info["Instagram"])
        if identificador not in vistos:
            vistos.add(identificador)
            contactos_limpios[nombre] = info

    contacto_seleccionado = st.selectbox(
        label="Lista de contactos limpia",
        options=list(contactos_limpios.keys())
    )

    if contacto_seleccionado:
        info_contacto = contactos_limpios[contacto_seleccionado]
        st.write(f"Numero: {info_contacto['Numero']}")
        st.write(f"Correo: {info_contacto['Correo']}")
        st.write(f"Direccion: {info_contacto['Direccion']}")
        st.write(f"Instagram: {info_contacto['Instagram']}")

# Opción 3: Ver tabla completa de datos
elif opcion == "3":
    st.subheader("Lista de contactos")
    # Se genera la tabla directamente desde la variable estructurada "limpia"
    st.table([{"Nombre": c[0], "Teléfono": c[1], "Correo": c[2], "Direccion": c[3], "Instagram": c[4]} for c in limpia])

# Opción 4: Agregar contacto
elif opcion == "4":
    st.subheader("Agregar un nuevo contacto a la agenda")
    
    with st.form("formulario_alta"):
        nombre_nuevo = st.text_input("Nombre completo:")
        tel_nuevo = st.text_input("Teléfono:")
        correo_nuevo = st.text_input("Correo electrónico:")
        dir_nueva = st.text_input("Dirección:")
        insta_nuevo = st.text_input("Instagram:")
        
        ejecutar_alta = st.form_submit_button("Registrar Contacto")
        
        if ejecutar_alta:
            if nombre_nuevo.strip() == "":
                st.error("El nombre no puede estar vacío.")
            else:
                # registrar un usuario
                st.session_state.agenda.append([nombre_nuevo])
                st.session_state.datos[nombre_nuevo] = {
                    "Numero": tel_nuevo, 
                    "Correo": correo_nuevo, 
                    "Direccion": dir_nueva, 
                    "Instagram": insta_nuevo
                }
                st.session_state.datos_tuplas.append(
                    (nombre_nuevo, tel_nuevo, correo_nuevo, dir_nueva, insta_nuevo)
                )
                st.success(f"Contacto {nombre_nuevo} agregado de forma correcta.")
                st.rerun()

# Opción 5: Eliminar contactos
elif opcion == "5":
    st.subheader("Eliminar un contacto de la agenda")
    
    nombre_baja = st.selectbox(
        "Selecciona el nombre de la persona que deseas eliminar:",
        options=["-- Selecciona un contacto --"] + list(datos.keys())
    )
    
    if nombre_baja != "-- Selecciona un contacto --":
        confirmar_baja = st.button(f"Confirmar eliminación de {nombre_baja}", type="primary")
        
        if confirmar_baja:
            # 1. Eliminar de agenda
            st.session_state.agenda = [item for item in st.session_state.agenda if item[0] != nombre_baja]
            
            # 2. Eliminar de datos (diccionario)
            if nombre_baja in st.session_state.datos:
                del st.session_state.datos[nombre_baja]
                
            # 3. Eliminar de datos_tuplas (lista de tuplas)
            st.session_state.datos_tuplas = [c for c in st.session_state.datos_tuplas if c[0] != nombre_baja]
            
            st.success(f"El contacto {nombre_baja} ha sido removido.")
            st.rerun()

# opcion no valida
elif opcion != "":
    st.warning("Por favor introduce un número de opción válido (1 al 5).")