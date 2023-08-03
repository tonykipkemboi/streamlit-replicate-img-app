# cSpell: disable
# --- Required Libraries and Modules --- #
import replicate
import streamlit as st
import requests

from utils import icon
from streamlit_image_select import image_select

# --- UI Configurations --- #
st.set_page_config(page_title="Replicate Image Generator",
                   page_icon=":bridge_at_night:",
                   layout="wide")

icon.show_icon(":magic_wand:")

# --- Secret Sauce (API Tokens and Endpoints) --- #
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
REPLICATE_MODEL_ENDPOINTSTABILITY = st.secrets["REPLICATE_MODEL_ENDPOINTSTABILITY"]

# --- Placeholders for Images and Gallery --- #
generated_images_placeholder = st.empty()
gallery_placeholder = st.empty()

# --- Sidebar Elements --- #
with st.sidebar:
    st.title(":orange[✨ Image Generation App ✨]", anchor=False)
    with st.form("my_form"):
        st.info("Yo fam! Start here ↓", icon="👋🏾")
        with st.expander(":blue[**Check under the hood? 🤷🏾‍♂️**]"):
            # Advanced Settings (for the curious minds!)
            width = st.number_input("Width of output image", value=1024)
            height = st.number_input("Height of output image", value=1024)
            num_outputs = st.slider(
                "Number of images to output", value=1, min_value=1, max_value=4)
            scheduler = st.selectbox('Scheduler', ('DDIM', 'DPMSolverMultistep', 'HeunDiscrete',
                                                'KarrasDPM', 'K_EULER_ANCESTRAL', 'K_EULER', 'PNDM'))
            num_inference_steps = st.slider(
                "Number of denoising steps", value=50, min_value=1, max_value=500)
            guidance_scale = st.slider(
                "Scale for classifier-free guidance", value=7.5, min_value=1.0, max_value=50.0, step=0.1)
            prompt_strength = st.slider(
                "Prompt strength when using img2img/inpaint(1.0 corresponds to full destruction of infomation in image)", value=0.8, max_value=1.0, step=0.1)
            refine = st.selectbox(
                "Select refine style to use (left out the other 2)", ("expert_ensemble_refiner", "None"))
            high_noise_frac = st.slider(
                "Fraction of noise to use for `expert_ensemble_refiner`", value=0.8, max_value=1.0, step=0.1)
        prompt = st.text_area(
            ":orange[**Enter prompt: start typing, Shakespeare ✍🏾**]", 
            value="An astronaut riding a rainbow unicorn, cinematic, dramatic")
        negative_prompt = st.text_area(":orange[**Party poopers you don't want in image? 🙅🏽‍♂️**]", 
                                       value="the absolute worst quality, distorted features", 
                                       help="This is a negative prompt, basically type what you don't want to see in the generated image")
        
        # The Big Red "Submit" Button!
        submitted = st.form_submit_button(
            "Submit", type="primary", use_container_width=True)

# --- Image Generation --- #
if submitted:
    try:
        # Calling the replicate API to get the image
        output = replicate.run(
            REPLICATE_MODEL_ENDPOINTSTABILITY,
            input={
                "prompt": prompt,
                "width": width,
                "height": height,
                "num_outputs": num_outputs,
                "scheduler": scheduler,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "prompt_stregth": prompt_strength,
                "refine": refine,
                "high_noise_frac": high_noise_frac
            }
        )

        # Displaying the image and download option
        for image in output:
            with generated_images_placeholder.container():
                st.image(image, caption="Generated Image 🎈", use_column_width=True)
                response = requests.get(image)
                if response.status_code == 200:
                    image_data = response.content
                    btn = st.download_button(
                        ":red[**Download**]", data=image_data, file_name="output_file.png", mime="image/png", use_container_width=True)
                else:
                    st.error(
                        f"Failed to fetch image from {image}. Error code: {response.status_code}", icon="🚨")

    except Exception as e:
        st.error(f'Encountered an error: {e}', icon="🚨")

# If not submitted, chill here 🍹
else: pass
    
# --- Gallery Display for inspiration or just plain admiration --- #
with gallery_placeholder.container():
    img = image_select(
        label="Like what you see? Right-click and save! It's not stealing if we're sharing! 😉",
        images=[
            "gallery/farmer_sunset.png", "gallery/astro_on_unicorn.png", 
            "gallery/friends.png", "gallery/wizard.png", "gallery/puppy.png",
            "gallery/cheetah.png", "gallery/viking.png",
        ],
        captions=["A farmer tilling a farm with a tractor during sunset, cinematic, dramatic", 
                "An astronaut riding a rainbow unicorn, cinematic, dramatic",
                "A group of friends laughing and dancing at a music festival, joyful atmosphere, 35mm film photography",
                "A wizard casting a spell, intense magical energy glowing from his hands, extremely detailed fantasy illustration",
                "A cute puppy playing in a field of flowers, shallow depth of field, Canon photography",
                "A cheetah mother nurses her cubs in the tall grass of the Serengeti. The early morning sun beams down through the grass. National Geographic photography by Frans Lanting",
                "A close-up portrait of a bearded viking warrior in a horned helmet. He stares intensely into the distance while holding a battle axe. Dramatic mood lighting, digital oil painting",
        ],
        use_container_width=True
    )