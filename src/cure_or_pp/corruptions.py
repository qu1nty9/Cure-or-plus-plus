from __future__ import annotations

from io import BytesIO
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

try:
    RESAMPLE_BICUBIC = Image.Resampling.BICUBIC
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
except AttributeError:  # pragma: no cover - Pillow < 9 compatibility.
    RESAMPLE_BICUBIC = Image.BICUBIC
    RESAMPLE_LANCZOS = Image.LANCZOS


RecipeFn = Callable[[Image.Image, dict, np.random.Generator], Image.Image]


def ensure_rgb(image: Image.Image) -> Image.Image:
    if image.mode == "RGB":
        return image
    return image.convert("RGB")


def jpeg_classic(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    return jpeg_recompress(image, quality=int(params["quality"]))


def resize_roundtrip(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    image = ensure_rgb(image)
    width, height = image.size
    scale = float(params["scale"])
    small_size = bounded_size(width, height, scale)
    return image.resize(small_size, RESAMPLE_BICUBIC).resize((width, height), RESAMPLE_BICUBIC)


def blur_classic(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    return ensure_rgb(image).filter(ImageFilter.GaussianBlur(radius=float(params["radius"])))


def screenshot_chain(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    image = resize_roundtrip(image, {"scale": params["scale"]}, rng)
    image = ImageEnhance.Sharpness(image).enhance(float(params["sharpness"]))
    return jpeg_recompress(image, quality=int(params["quality"]))


def messenger_chain(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    image = ensure_rgb(image)
    max_side = int(params["max_side"])
    width, height = image.size
    if max(width, height) > max_side:
        scale = max_side / max(width, height)
        image = image.resize(bounded_size(width, height, scale), RESAMPLE_LANCZOS)
    return jpeg_recompress(image, quality=int(params["quality"]))


def video_call_frame(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    image = resize_roundtrip(image, {"scale": params["scale"]}, rng)
    image = image.filter(ImageFilter.GaussianBlur(radius=float(params["blur"])))
    image = add_gaussian_noise(image, sigma=float(params["noise_sigma"]), rng=rng)
    return jpeg_recompress(image, quality=int(params["quality"]))


def low_light_upload(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    image = ensure_rgb(image)
    image = ImageEnhance.Brightness(image).enhance(float(params["brightness"]))
    image = add_gaussian_noise(image, sigma=float(params["noise_sigma"]), rng=rng)
    image = image.filter(ImageFilter.GaussianBlur(radius=float(params["denoise_blur"])))
    return jpeg_recompress(image, quality=int(params["quality"]))


def dirty_lens_recompress(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    image = ensure_rgb(image)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    width, height = image.size

    count = int(params["stain_count"])
    alpha = int(params["stain_alpha"])
    for _ in range(count):
        radius = int(rng.integers(max(8, min(width, height) // 18), max(12, min(width, height) // 5)))
        x = int(rng.integers(-radius, width))
        y = int(rng.integers(-radius, height))
        color = int(rng.integers(190, 245))
        draw.ellipse((x, y, x + radius, y + radius), fill=(color, color, color, alpha))

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=max(3, min(width, height) // 80)))
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    return jpeg_recompress(image, quality=int(params["quality"]))


def restoration_artifact(image: Image.Image, params: dict, rng: np.random.Generator) -> Image.Image:
    image = ensure_rgb(image)
    width, height = image.size
    image = image.filter(ImageFilter.GaussianBlur(radius=float(params["pre_blur"])))

    upscale = float(params["upscale"])
    up_size = (max(1, int(width * upscale)), max(1, int(height * upscale)))
    image = image.resize(up_size, RESAMPLE_LANCZOS).resize((width, height), RESAMPLE_LANCZOS)
    image = ImageEnhance.Sharpness(image).enhance(float(params["sharpness"]))
    image = ImageEnhance.Contrast(image).enhance(1.08)
    return jpeg_recompress(image, quality=int(params["quality"]))


def jpeg_recompress(image: Image.Image, quality: int) -> Image.Image:
    buffer = BytesIO()
    ensure_rgb(image).save(buffer, format="JPEG", quality=quality, subsampling=2, optimize=False)
    buffer.seek(0)
    with Image.open(buffer) as compressed:
        return compressed.convert("RGB")


def add_gaussian_noise(image: Image.Image, sigma: float, rng: np.random.Generator) -> Image.Image:
    array = np.asarray(ensure_rgb(image)).astype(np.float32)
    noise = rng.normal(loc=0.0, scale=sigma, size=array.shape)
    noisy = np.clip(array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy, mode="RGB")


def bounded_size(width: int, height: int, scale: float) -> tuple[int, int]:
    return (max(1, int(width * scale)), max(1, int(height * scale)))


RECIPES: dict[str, RecipeFn] = {
    "jpeg_classic": jpeg_classic,
    "resize_roundtrip": resize_roundtrip,
    "blur_classic": blur_classic,
    "screenshot_chain": screenshot_chain,
    "messenger_chain": messenger_chain,
    "video_call_frame": video_call_frame,
    "low_light_upload": low_light_upload,
    "dirty_lens_recompress": dirty_lens_recompress,
    "restoration_artifact": restoration_artifact,
}


def apply_recipe(
    image: Image.Image,
    recipe_name: str,
    params: dict,
    rng: np.random.Generator,
) -> Image.Image:
    try:
        recipe = RECIPES[recipe_name]
    except KeyError as exc:
        known = ", ".join(sorted(RECIPES))
        raise ValueError(f"Unknown recipe '{recipe_name}'. Known recipes: {known}") from exc
    return recipe(image, params, rng)

