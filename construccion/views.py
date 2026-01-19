from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def contacto_form(request):
    """
    Procesa el formulario de contacto y envía notificación por email.
    """
    try:
        # Parsear datos JSON
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['nombre', 'email', 'mensaje']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }, status=400)
        
        # Extraer y limpiar datos
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip()
        telefono = data.get('telefono', 'No proporcionado').strip()
        proyecto = data.get('tipoProyecto', 'No especificado').strip()
        mensaje = data.get('mensaje', '').strip()
        
        # Validaciones básicas
        if len(nombre) > 100 or len(email) > 100:
            return JsonResponse({
                'success': False,
                'error': 'Los campos nombre y email no pueden exceder 100 caracteres'
            }, status=400)
        
        if len(mensaje) > 2000:
            return JsonResponse({
                'success': False,
                'error': 'El mensaje no puede exceder 2000 caracteres'
            }, status=400)
        
        # Logging
        logger.info(f"Nuevo contacto recibido de: {nombre} ({email})")
        
        # Enviar email
        _enviar_email_contacto(nombre, email, telefono, proyecto, mensaje)
        
        # Guardar respaldo en archivo (opcional)
        _guardar_respaldo_contacto(nombre, email, telefono, proyecto, mensaje)
        
        return JsonResponse({
            'success': True,
            'message': '¡Gracias por contactarnos! Te responderemos pronto.'
        })
        
    except json.JSONDecodeError:
        logger.error("Error al parsear JSON del request")
        return JsonResponse({
            'success': False,
            'error': 'Formato de datos inválido'
        }, status=400)
        
    except BadHeaderError:
        logger.error("Intento de inyección de headers en email")
        return JsonResponse({
            'success': False,
            'error': 'Datos inválidos detectados'
        }, status=400)
        
    except Exception as e:
        logger.exception(f"Error inesperado en formulario de contacto: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Ocurrió un error al procesar tu solicitud. Por favor intenta nuevamente.'
        }, status=500)


def _enviar_email_contacto(nombre, email, telefono, proyecto, mensaje):
    """
    Envía email de notificación de nuevo contacto.
    """
    try:
        asunto = f'🔨 Nuevo Contacto IronPrime: {nombre}'
        
        # Crear versión HTML del email
        html_mensaje = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #667eea; }}
                .value {{ margin-top: 5px; padding: 10px; background: white; border-radius: 4px; }}
                .mensaje-box {{ background: white; padding: 20px; border-left: 4px solid #667eea; 
                               margin-top: 20px; border-radius: 4px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">🔨 IronPrime Construcción</h1>
                    <p style="margin: 10px 0 0 0;">Nuevo Contacto Recibido</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="label">👤 Nombre:</div>
                        <div class="value">{nombre}</div>
                    </div>
                    <div class="field">
                        <div class="label">📧 Email:</div>
                        <div class="value"><a href="mailto:{email}">{email}</a></div>
                    </div>
                    <div class="field">
                        <div class="label">📱 Teléfono:</div>
                        <div class="value">{telefono}</div>
                    </div>
                    <div class="field">
                        <div class="label">🏗️ Tipo de Proyecto:</div>
                        <div class="value">{proyecto}</div>
                    </div>
                    <div class="mensaje-box">
                        <div class="label">💬 Mensaje:</div>
                        <div style="margin-top: 10px;">{mensaje}</div>
                    </div>
                    <div class="footer">
                        <p>⏰ Recibido el {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}</p>
                        <p style="color: #667eea; font-weight: bold;">⚡ Responder lo antes posible</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Versión texto plano (fallback)
        texto_plano = f"""
        NUEVO CONTACTO - IRONPRIME CONSTRUCCIÓN
        ========================================
        
        Nombre: {nombre}
        Email: {email}
        Teléfono: {telefono}
        Tipo de proyecto: {proyecto}
        
        Mensaje:
        {mensaje}
        
        Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        """
        
        send_mail(
            subject=asunto,
            message=texto_plano,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@ironprime.com'),
            recipient_list=[getattr(settings, 'CONTACT_EMAIL', 'm.medelrojo@gmail.com')],
            html_message=html_mensaje,
            fail_silently=False,
        )
        
        logger.info(f"Email de contacto enviado exitosamente para: {nombre}")
        
    except Exception as e:
        logger.error(f"Error al enviar email de contacto: {str(e)}")
        raise


def _guardar_respaldo_contacto(nombre, email, telefono, proyecto, mensaje):
    """
    Guarda un respaldo del contacto en archivo de texto.
    """
    try:
        ruta_archivo = getattr(settings, 'CONTACT_BACKUP_FILE', 'contactos_recibidos.txt')
        
        with open(ruta_archivo, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Nombre: {nombre}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Teléfono: {telefono}\n")
            f.write(f"Proyecto: {proyecto}\n")
            f.write(f"Mensaje: {mensaje}\n")
            
        logger.info(f"Respaldo de contacto guardado en {ruta_archivo}")
        
    except Exception as e:
        # No fallar si el respaldo falla
        logger.warning(f"No se pudo guardar respaldo de contacto: {str(e)}")