from diffusers import AutoPipelineForInpainting, AutoencoderKL
from diffusers.utils import load_image
import torch
from time import time
from app.vision.segment import segment_body
import platform

# TODO: Add logging logic instead of printing
class ImageSynthesiser:
    def __init__(self):
        self.pipeline = None
        self.loaded = False
    
    def preload(self):
        if not self.loaded:
            starting1 = time()
            print("Loading ImageSynthesiser")
            self.pipeline = self._initialize_pipeline()
            self.loaded = True
            print(f"ImageSynthesiser loading completed in {time() - starting1:.2f} seconds")

    def _initialize_pipeline(self):
        device = self._get_device()
        vae = self._get_autoencoder()
        pipeline = AutoPipelineForInpainting.from_pretrained(
            "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
            vae=vae,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        ).to(device)
        pipeline = self._load_ip_adapter(pipeline)
        pipeline = self._set_ip_scale(pipeline,ip_scale=1.0)
        return pipeline

    def _get_device(self):
        os_name = platform.system()
        if torch.backends.mps.is_available():
            device = torch.device("mps")
            print("Using MPS (GPU acceleration enabled on macOS)")
        elif torch.cuda.is_available():
            device = torch.device("cuda:0")
            print("Using CUDA on Linux (GPU acceleration enabled)")
        else:
            device = torch.device("cpu")
            print("Using CPU")
        return device

    def _get_autoencoder(self):
        print("Loading autoencoder")
        vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
        print(f"Autoencoder loading completed")
        return vae

    def _load_ip_adapter(self, pipeline, adapter="h94/IP-Adapter", subfolder_model="sdxl_models", weights="ip-adapter_sdxl.bin"):
        print("Loading IP adapter")
        pipeline.load_ip_adapter(adapter, subfolder=subfolder_model, weight_name=weights, low_cpu_mem_usage=True)
        print(f"IP Adapter loading completed")
        return pipeline

    def _set_ip_scale(self, pipeline, ip_scale=1.0):
        print("Setting IP Scale")
        pipeline.set_ip_adapter_scale(ip_scale)
        print(f"Setting IP scale completed")
        return pipeline

    def virtual_try_on(self, img, clothing, prompt, negative_prompt, ip_scale=1.0, strength=0.99, guidance_scale=7.5, steps=100):
        _, mask_img = segment_body(img, face=False)
        images = self.pipeline(
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

    def produce_synthesized_image(self, person_image_path, cloth_image_path):
        self.load()
        person_image = load_image(person_image_path)
        ip_image = load_image(cloth_image_path)
        result_image = self.virtual_try_on(
            img=person_image,
            clothing=ip_image,
            prompt="photorealistic, perfect body, beautiful skin, realistic skin, natural skin",
            negative_prompt="ugly, bad quality, bad anatomy, deformed body, deformed hands, deformed feet, deformed face, deformed clothing, deformed skin, bad skin, leggings, tights, stockings",
            ip_scale=1.0,
            strength=0.99,
            guidance_scale=7.5,
            steps=100)
        result_image.save('output_image.png')
        print(f"Virtual try-on completed in {time() - starting4:.2f} seconds. Result saved as 'output_image.png'.")
