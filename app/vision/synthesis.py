from diffusers import AutoPipelineForInpainting, AutoencoderKL
from diffusers.utils import load_image
import torch
from time import time
from app.vision.segment import segment_body
import platform
from app.logger import app_logger



class ImageSynthesiser:
    def __init__(self):
        self.pipeline = None
        self.loaded = False
    
    def preload(self):
        if not self.loaded:
            starting1 = time()
            app_logger.info("Loading ImageSynthesiser......")
            self._initialize_pipeline()
            self._load_ip_adapter(adapter="h94/IP-Adapter", subfolder_model="sdxl_models", weights="ip-adapter_sdxl.bin")
            self._set_ip_scale(ip_scale=1.0)
            self.loaded = True
            app_logger.info(f"ImageSynthesiser loading completed in {time() - starting1:.2f} seconds")

    def _initialize_pipeline(self):
        device = self._get_device()
        vae = self._get_autoencoder()
        self.pipeline = AutoPipelineForInpainting.from_pretrained(
            "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
            vae=vae,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        ).to(device)
 
    def _get_device(self):
        os_name = platform.system()
        if torch.backends.mps.is_available():
            device = torch.device("mps")
            app_logger.info("Using MPS (GPU acceleration enabled on macOS).....")
            print("Using MPS (GPU acceleration enabled on macOS)")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
            app_logger.info("Using CUDA on Linux (GPU acceleration enabled)....")
        else:
            device = torch.device("cpu")
            app_logger.info("Using CPU as a device....")
        return device

    def _get_autoencoder(self):
        app_logger.info("Loading Autoencoder.....")
        vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
        app_logger.info("Autoencoder loading completed")
        return vae

    def _load_ip_adapter(self, adapter="h94/IP-Adapter", subfolder_model="sdxl_models", weights="ip-adapter_sdxl.bin"):
        app_logger.info("Loading IP adapter.....")
        self.pipeline.load_ip_adapter(adapter, subfolder=subfolder_model, weight_name=weights, low_cpu_mem_usage=True)
        app_logger.info("IP Adapter loading completed")

    def _set_ip_scale(self, ip_scale=1.0):
        app_logger.info("Setting IP Scale")
        self.pipeline.set_ip_adapter_scale(ip_scale)
        app_logger.info("Setting IP scale completed")


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

    # @shared_task(bind=True)
    def produce_synthesized_image(self, data):
        try:
            person_image_path = data['person_image_path']
            cloth_image_path = data['cloth_image_path']

            print("data",data)
            print("person_image_path",person_image_path)
            print("cloth_image_path",cloth_image_path)

            starting4 = time()
            app_logger.info("Synthesis Function started")
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
                # TODO increase as per need default: 100
                steps=2)
            app_logger.info(f"Image synthesis completed in {time() - starting4:.2f} seconds.")
            return result_image
        except Exception as e:
            print("Error while trying to produce image", e)
            app_logger.error("Error while trying to produce image", e)