from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer


OUTPUT = Path("Entrega_Practica_Semana_12_Caso_1.pdf")
EVIDENCIA = Path("evidencia")


def portada(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawString(2 * cm, 1.4 * cm, "UNIVERSIDAD NACIONAL DEL CENTRO DEL PERU")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TituloCentro",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=18,
    leading=22,
))
styles.add(ParagraphStyle(
    name="SubtituloCentro",
    parent=styles["Heading2"],
    alignment=TA_CENTER,
    fontSize=12,
    leading=16,
))

story = [
    Spacer(1, 2.5 * cm),
    Paragraph("UNIVERSIDAD NACIONAL DEL CENTRO DEL PERÚ", styles["TituloCentro"]),
    Spacer(1, 0.4 * cm),
    Paragraph("FACULTAD DE INGENIERÍA DE SISTEMAS", styles["SubtituloCentro"]),
    Spacer(1, 1.2 * cm),
    Paragraph("PRÁCTICA GRUPAL - SEMANA 12", styles["TituloCentro"]),
    Paragraph("Caso 1: Sistema de Gestión de Préstamos de Equipos", styles["SubtituloCentro"]),
    Spacer(1, 1.2 * cm),
    Paragraph("Asignatura: Desarrollo de Aplicaciones Web (IS093A)", styles["Normal"]),
    Spacer(1, 0.5 * cm),
    Paragraph("<b>Integrante:</b>", styles["Heading3"]),
    Paragraph("CASTILLO LAVADO FAVIO SAMIR", styles["Normal"]),
    Paragraph("<b>Código:</b> 2022100529A", styles["Normal"]),
    Spacer(1, 0.5 * cm),
    Paragraph("<b>Fecha:</b> 19 de noviembre de 2026", styles["Normal"]),
    PageBreak(),
    Paragraph("1. Repositorio del proyecto", styles["Heading1"]),
    Paragraph(
        "Repositorio público: https://github.com/fv2315/semana--12g",
        styles["Normal"],
    ),
    Paragraph(
        "El repositorio contiene el proyecto Django completo, instrucciones de instalación, "
        "datos de prueba, pruebas automatizadas y configuración de control de versiones.",
        styles["Normal"],
    ),
    Spacer(1, 0.5 * cm),
    Paragraph("2. Evidencias de implementación", styles["Heading1"]),
]

evidencias = (
    ("01_catalogo.png", "Catálogo público", "Muestra el listado de equipos disponibles y su estado, accesible sin autenticación."),
    ("02_login_admin.png", "Inicio de sesión administrativo", "Presenta la pantalla de autenticación institucional de Django Admin."),
    ("03_panel_admin.png", "Panel administrativo", "Demuestra el acceso mediante el usuario administrador y los módulos disponibles."),
    ("04_admin_equipos.png", "Django Admin de equipos", "Evidencia la gestión de equipos con filtros por laboratorio y estado."),
    ("05_admin_prestamos.png", "Django Admin de préstamos", "Presenta el listado de préstamos con fechas, estado y días de retraso."),
)

for nombre, titulo, descripcion in evidencias:
    ruta = EVIDENCIA / nombre
    if ruta.exists():
        story.extend([
            PageBreak(),
            Paragraph(titulo, styles["Heading2"]),
            Paragraph(descripcion, styles["Normal"]),
            Spacer(1, 0.3 * cm),
            Image(str(ruta), width=17 * cm, height=10.6 * cm, kind="proportional"),
        ])

story.extend([
    PageBreak(),
    Paragraph("3. Evidencias técnicas adicionales", styles["Heading1"]),
    Paragraph("Login y autenticación: /login/ y /admin/", styles["Normal"]),
    Paragraph("Sesión: timeout configurado de 30 minutos e HttpOnly.", styles["Normal"]),
    Paragraph("Middleware: registra accesos denegados y acciones críticas en RegistroAuditoria.", styles["Normal"]),
    Paragraph("Validaciones: fechas, estado operativo, stock disponible y límite de tres préstamos activos.", styles["Normal"]),
    Paragraph("Datos de prueba: 10 equipos, 8 usuarios y 15 préstamos.", styles["Normal"]),
    PageBreak(),
    Paragraph("4. Reflexión individual", styles["Heading1"]),
    Paragraph(
        "El desarrollo del módulo de gestión de equipos y formulario de préstamos me permitió comprender "
        "a profundidad la importancia de trasladar las reglas de negocio complejas directamente a la capa "
        "de validación de Django. Implementar validaciones cruzadas en el método clean() —como restringir "
        "el límite de 3 préstamos activos por docente, verificar la disponibilidad del stock e impedir la "
        "reserva de equipos en estado de mantenimiento— garantizó la integridad de los datos desde el "
        "momento del ingreso de la información.",
        styles["Normal"],
    ),
    Spacer(1, 0.5 * cm),
    Paragraph(
        "Asimismo, descubrí el potencial del Django Admin al personalizar vistas con campos calculados "
        "(como la diferencia de días desde el último mantenimiento y el semáforo visual de estado) y "
        "acciones masivas para el envío de alertas de devolución, convirtiendo una herramienta de gestión "
        "interna en un panel operativo eficiente.",
        styles["Normal"],
    ),
])

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm,
)
doc.build(story, onFirstPage=portada, onLaterPages=portada)
print(OUTPUT.resolve())
