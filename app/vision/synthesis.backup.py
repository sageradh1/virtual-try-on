from diffusers import AutoPipelineForInpainting, AutoencoderKL
from diffusers.utils import load_image
import torch
from time import time
import platform

def get_device():
    os_name = platform.system()
    if torch.backends.mps.is_available():
        device = torch.device("mps")  # Use Metal Performance Shaders
        print("Using MPS (GPU acceleration enabled on macOS)")
    elif torch.cuda.is_available():
        device = torch.device("cuda:0")
        print("Using CUDA on Linux (GPU acceleration enabled)")
    else:
        device = torch.device("cpu")
        print(f"Using CPU")
    return device

def get_autoencoder():
    starting1 = time()
    print("Loading autoencoder")
    vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
    print(f"Autoencoder loading completed in {time() - starting1:.2f} seconds")
    return vae

def get_autopipeline():
    starting2 = time()
    print("Loading autopipeline")
    device = get_device()
    vae = get_autoencoder()
    pipeline = AutoPipelineForInpainting.from_pretrained(
        "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
        vae=vae,
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    ).to(device)
    print(f"Autopipeline loading completed in {time() - starting2:.2f} seconds")
    return pipeline

def load_ip_adapter(pipeline,adapter="h94/IP-Adapter",subfolder_model="sdxl_models", weights="ip-adapter_sdxl.bin"):
    starting3 = time()
    print("Loading IP adapter")
    pipeline.load_ip_adapter(adapter, subfolder=subfolder_model, weight_name=weights, low_cpu_mem_usage=True)
    print(f"IP Adapter loading completed in {time() - starting3:.2f} seconds")
    return pipeline

def set_ip_scale(pipeline, ip_scale=1.0):
    starting3 = time()
    print("Setting IP Scale")
    pipeline.set_ip_adapter_scale(ip_scale)
    print(f"Setting IP scale completed in {time() - starting3:.2f} seconds")
    return pipeline

# image = load_image('https://cdn-uploads.huggingface.co/production/uploads/648a824a8ca6cf9857d1349c/jpFBKqYB3BtAW26jCGJKL.jpeg').convert("RGB")
# image.resize((512, 512))
# ip_image = load_image('https://cdn-uploads.huggingface.co/production/uploads/648a824a8ca6cf9857d1349c/NL6mAYJTuylw373ae3g-Z.jpeg').convert("RGB")
# ip_image.resize((512, 512))

# # ! git clone https://github.com/TonyAssi/Segment-Body.git
# # %cd /content/Segment-Body
# # ! pip install -r requirements.txt
# # ! cp ./SegBody.py ..
# # %cd ..
from app.vision.segment import segment_body
# seg_image, mask_image = segment_body(image, face=False)
# mask_image.resize((512, 512))
# pipeline.set_ip_adapter_scale(1.0)
# images = pipeline(
#     prompt="photorealistic, perfect body, beautiful skin, realistic skin, natural skin",
#     negative_prompt="ugly, bad quality, bad anatomy, deformed body, deformed hands, deformed feet, deformed face, deformed clothing, deformed skin, bad skin, leggings, tights, stockings",
#     image=image,
#     mask_image=mask_image,
#     ip_adapter_image=ip_image,
#     strength=0.99,
#     guidance_scale=7.5,
#     num_inference_steps=100,
# ).images
# # images[0]


def virtual_try_on(img, clothing, prompt, negative_prompt, pipeline, ip_scale=1.0, strength=0.99, guidance_scale=7.5, steps=100):
    _, mask_img = segment_body(img, face=False)
    images = pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=img,
        mask_image=mask_img,
        ip_adapter_image=clothing,
        strength=strength,
        guidance_scale=guidance_scale,
        num_inference_steps=steps,
    ).images
    return images[0]

# Assuming segment_body and pipeline have been defined and initialized elsewhere.


def produce_synthesized_image(
        pipeline,
        person_image_path='/Users/sagar/working_dir/github_personal/virtual-try-on/app/static/uploaded/75eec2960b49802f465d69f35943c154.jpg', 
        cloth_image_path='/Users/sagar/working_dir/github_personal/virtual-try-on/app/static/uploaded/NL6mAYJTuylw373ae3g-Z.jpeg'
        ):
    # Load images
    person_image = load_image(person_image_path)
    print("Person image loaded")

    ip_image = load_image(cloth_image_path)
    print("Clothes loaded")

    starting4 = time()
    print("Function started")
    # Perform virtual try-on
    result_image = virtual_try_on(img=person_image,
                                clothing=ip_image,
                                prompt="photorealistic, perfect body, beautiful skin, realistic skin, natural skin",
                                negative_prompt="ugly, bad quality, bad anatomy, deformed body, deformed hands, deformed feet, deformed face, deformed clothing, deformed skin, bad skin, leggings, tights, stockings",
                                pipeline=pipeline
                                )

    # Save the result
    result_image.save('output_image.png')
    print(f"Virtual try-on completed in {time() - starting4:.2f} seconds. Result saved as 'output_image.png'.")