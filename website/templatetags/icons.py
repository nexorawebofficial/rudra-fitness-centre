from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Self-hosted inline SVG icon set (no external icon font / CDN — keeps the
# site fully functional offline and on slow mobile connections).
_ICONS = {
    'dumbbell': '<path d="M2 12h2M20 12h2M6 8v8M18 8v8M6 12h12" stroke-linecap="round"/>'
                 '<rect x="4" y="9" width="2" height="6" rx="0.5"/><rect x="18" y="9" width="2" height="6" rx="0.5"/>',
    'members': '<circle cx="9" cy="8" r="3"/><path d="M2 21v-1a6 6 0 0 1 6-6h2a6 6 0 0 1 6 6v1" stroke-linecap="round"/>'
               '<circle cx="17" cy="8" r="2.5"/><path d="M17 12a5 5 0 0 1 5 5v1" stroke-linecap="round"/>',
    'trophy': '<path d="M8 4h8v4a4 4 0 0 1-8 0V4z"/><path d="M8 5H5a2 2 0 0 0 2 4M16 5h3a2 2 0 0 1-2 4"/>'
              '<path d="M12 12v3M9 19h6M10 15h4v4h-4z" stroke-linecap="round"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4" stroke-linecap="round"/>',
    'qr': '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>'
          '<rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM19 14h2v2h-2zM14 19h2v2h-2zM19 19h2v2h-2z"/>',
    'apple': '<path d="M12 8c-1.5-2-4-2-5 0-1.5 3 0 9 3 11 1 .7 2 .7 3 0 1-2 1-2 2 0 1 .7 2 .7 3 0 3-2 4.5-8 3-11-1-2-3.5-2-5 0z"/>'
             '<path d="M12 8c0-2 1-3 2-3.5" stroke-linecap="round"/>',
    'shield-check': '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4" stroke-linecap="round" stroke-linejoin="round"/>',
    'card': '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4" stroke-linecap="round"/>',
    'check': '<path d="M5 12l5 5L19 7" stroke-linecap="round" stroke-linejoin="round"/>',
    'star': '<path d="M12 3l2.6 5.6 6.1.6-4.6 4.1 1.3 6-5.4-3.1-5.4 3.1 1.3-6-4.6-4.1 6.1-.6z" stroke-linejoin="round"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2" stroke-linecap="round"/>',
    'phone': '<path d="M5 4h4l1.5 4.5-2.3 1.8a12 12 0 0 0 5.5 5.5l1.8-2.3L20 15v4a1 1 0 0 1-1 1C10.7 20 4 13.3 4 5a1 1 0 0 1 1-1z" stroke-linejoin="round"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M4 7l8 6 8-6" stroke-linecap="round" stroke-linejoin="round"/>',
    'location': '<path d="M12 21s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    'instagram': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
    'facebook': '<path d="M14 21v-8h3l.5-4H14V6.5c0-1.2.4-2 2.1-2H18V1.2C17.6 1.1 16.4 1 15 1c-3 0-5 1.8-5 5.1V9H7v4h3v8z"/>',
    'youtube': '<rect x="2" y="6" width="20" height="12" rx="3"/><path d="M10 9.5l6 2.5-6 2.5z"/>',
    'whatsapp': '<path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z"/>'
                '<path d="M8.5 8.5c-.3 1 .2 2.4 1.5 3.7s2.7 1.8 3.7 1.5c.4-.1.7-.9.5-1.3l-.7-1.1c-.2-.3-.6-.3-.9-.1l-.5.3c-.6-.3-1.3-1-1.7-1.7l.3-.5c.2-.3.2-.7-.1-.9L9.5 8c-.4-.2-1.2.1-1 .5z" fill="currentColor" stroke="none"/>',
    'diet': '<path d="M12 7c-1.7 0-3 1.6-3 4 0 4 2 8 3 8s3-4 3-8c0-2.4-1.3-4-3-4z"/><path d="M12 7c0-2 1-3.5 2.5-4" stroke-linecap="round"/>',
    'renew': '<path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3" stroke-linecap="round"/>'
             '<path d="M18 4v4h-4M6 20v-4h4" stroke-linecap="round" stroke-linejoin="round"/>',
}


@register.simple_tag
def icon(name, css_class='icon'):
    body = _ICONS.get(name, '')
    return mark_safe(
        f'<svg class="{css_class}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.6" aria-hidden="true">{body}</svg>'
    )
