import hashlib
import pathlib
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.core.files.base import ContentFile

from users.identifiers import (
    PORTRAIT_EDGE,
    PORTRAIT_GLYPH_SIZE,
    PORTRAIT_PALETTE,
    PORTRAIT_TYPEFACE,
)


def _initial_glyph(member_record):
    raw = getattr(member_record, 'name', None) or ''
    return (raw.strip() or 'U')[0].upper()


def _palette_index(member_record):
    if member_record.pk:
        return member_record.pk

    digest = hashlib.blake2b(
        (member_record.email or 'user').encode('utf-8'),
        digest_size=4,
    ).digest()
    return int.from_bytes(digest, byteorder='big')


def _load_typeface():
    font_path = pathlib.Path(settings.BASE_DIR) / PORTRAIT_TYPEFACE
    try:
        return ImageFont.truetype(str(font_path), PORTRAIT_GLYPH_SIZE)
    except (IOError, OSError):
        return ImageFont.load_default()


def _rasterize_letter(glyph, backdrop):
    surface = Image.new('RGB', (PORTRAIT_EDGE, PORTRAIT_EDGE), backdrop)
    brush = ImageDraw.Draw(surface)
    midpoint = PORTRAIT_EDGE // 2
    brush.text(
        (midpoint, midpoint),
        glyph,
        fill='white',
        font=_load_typeface(),
        anchor='mm',
    )
    return surface


def build_initial_portrait(member_record):
    """Создаёт PNG-аватар с первой буквой имени на цветном фоне."""

    glyph = _initial_glyph(member_record)
    backdrop = PORTRAIT_PALETTE[_palette_index(member_record) % len(PORTRAIT_PALETTE)]
    raster = _rasterize_letter(glyph, backdrop)

    payload = BytesIO()
    raster.save(payload, format='PNG')
    payload.seek(0)

    mailbox = member_record.email.split('@')[0] if member_record.email else 'user'
    asset_name = f'avatar_{mailbox}_{glyph}.png'
    return ContentFile(payload.getvalue(), name=asset_name)
