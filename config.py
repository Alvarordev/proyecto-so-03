TITLE='Reservas académicas de laboratorio'
EMOJI='🎓'
SCENARIO='Una coordinación académica requiere una aplicación sencilla para registrar reservas de laboratorios usados en cursos de programación, redes, sistemas operativos y ciberseguridad. El sistema debe registrar el curso, el responsable y la cantidad de horas solicitadas. En un despliegue monolítico, el servicio web, la lógica de negocio y la base de datos SQLite se ejecutan sobre el mismo sistema operativo. El estudiante debe identificar riesgos relacionados con procesos detenidos, puertos mal configurados, respaldos manuales del archivo de datos y dificultad para reproducir la instalación en otro servidor. La reflexión debe conectar el caso con conceptos de servicios, procesos, almacenamiento local y administración de recursos, antes de comparar con el despliegue usando contenedores.'
PORT=5003
DB_NAME='reservas.db'
FIELDS=[('curso', 'Curso', 'text'), ('responsable', 'Responsable', 'text'), ('horas', 'Horas', 'number')]
SEED=[('Sistemas Operativos', 'Docente A', 4), ('Redes', 'Docente B', 3), ('DevOps', 'Docente C', 5)]
SUMMARY_COL='horas'
SUMMARY_LABEL='Horas reservadas'

