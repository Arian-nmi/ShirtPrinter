import os
import time
import uuid
from celery import shared_task
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from .models import Mockup, MockupImage


@shared_task
def generate_mockup_images_task(task_id):
    try:
        mockup = Mockup.objects.get(task_id=task_id)
        mockup.status = 'PENDING'
        mockup.save()

        time.sleep(1)

        source_dir = os.path.join(settings.BASE_DIR, 'static', 'mockup_templates')
        dest_dir = os.path.join(settings.MEDIA_ROOT, 'mockups', str(mockup.task_id))
        os.makedirs(dest_dir, exist_ok=True)

        template_files = [
            f for f in os.listdir(source_dir)
            if f.lower().endswith('.png')
        ]

        if not template_files:
            raise FileNotFoundError("No mockup template images found in static/mockup_templates/")

        for file_name in template_files:
            color_name = os.path.splitext(file_name)[0]
            src_path = os.path.join(source_dir, file_name)

            img = Image.open(src_path).convert("RGBA")
            draw = ImageDraw.Draw(img)

            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSans.ttf')
            try:
                font = ImageFont.truetype(font_path, size=48)
            except Exception:
                font = ImageFont.load_default()

            text = mockup.text
            text_color = "#000000" if "black" not in color_name.lower() else "#FFFFFF"

            image_w, image_h = img.size
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
            except AttributeError:
                text_w, text_h = draw.textsize(text, font=font)

            x = (image_w - text_w) // 2
            y = (image_h - text_h) // 2

            draw.text((x, y), text, font=font, fill=text_color)

            filename = f"{color_name}_{uuid.uuid4().hex[:8]}.png"
            save_path = os.path.join(dest_dir, filename)
            img.save(save_path, format="PNG")

            rel_path = os.path.relpath(save_path, settings.MEDIA_ROOT)
            image_url = f"/media/{rel_path}"

            MockupImage.objects.create(
                mockup=mockup,
                shirt_color=color_name,
                image_url=image_url
            )

        mockup.status = 'SUCCESS'
        mockup.save()
        return True

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        mockup.status = 'FAILURE'
        mockup.save()
        raise e