<<<<<<< HEAD
import os
import gradio as gr
import subprocess
import tempfile
import uuid
from pathlib import Path

# Define paths
SADTALKER_ROOT = os.path.dirname(os.path.abspath(__file__))
INFERENCE_SCRIPT = os.path.join(SADTALKER_ROOT, "inference.py")
RESULT_DIR = os.path.join(SADTALKER_ROOT, "results")
os.makedirs(RESULT_DIR, exist_ok=True)

def generate_talking_face(source_image, driven_audio, still=True, preprocess="full", enhancer="gfpgan"):
    """
    Generate a talking face animation using SadTalker.
    """
    if not os.path.exists(INFERENCE_SCRIPT):
        return None

    session_id = str(uuid.uuid4())
    temp_result_dir = os.path.join(RESULT_DIR, session_id)
    os.makedirs(temp_result_dir, exist_ok=True)

    cmd = [
        "python", INFERENCE_SCRIPT,
        "--driven_audio", driven_audio,
        "--source_image", source_image,
        "--result_dir", temp_result_dir,
        "--preprocess", preprocess
    ]

    if still:
        cmd.append("--still")
    if enhancer:
        cmd.extend(["--enhancer", enhancer])

    print("Running SadTalker command:", " ".join(cmd))

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=SADTALKER_ROOT
        )
        stdout, stderr = process.communicate()

        print("SadTalker Output:\n", stdout.decode())
        print("SadTalker Error:\n", stderr.decode())

        if process.returncode != 0:
            print(f"SadTalker failed with code {process.returncode}")
            return None

        video_files = list(Path(temp_result_dir).glob("*.mp4"))
        if not video_files:
            print("No video file was generated.")
            return None

        return str(video_files[0])

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        return None

def process_inputs(image, audio, use_still, preprocess_method, use_enhancer):
    """Process inputs and generate the talking face animation."""
    if image is None or audio is None:
        return None, "Please upload both an image and an audio file."

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
        image_path = temp_img.name
        image.save(image_path)

    audio_path = audio
    enhancer = "gfpgan" if use_enhancer else None

    try:
        video_path = generate_talking_face(
            image_path,
            audio_path,
            still=use_still,
            preprocess=preprocess_method,
            enhancer=enhancer
        )
        if video_path:
            return video_path, "Animation generated successfully!"
        else:
            return None, "Failed to generate animation. Please check logs."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
    finally:
        if os.path.exists(image_path):
            os.unlink(image_path)

# Build Gradio Interface
with gr.Blocks(title="SadTalker: Talking Face Animation") as demo:
    gr.Markdown("## 🎭 SadTalker: Generate a talking face animation from an image and audio.")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(label="Upload Source Image", type="pil")
            audio_input = gr.Audio(label="Upload Driven Audio", type="filepath")

            with gr.Accordion("Advanced Settings", open=False):
                still_checkbox = gr.Checkbox(label="Use Still Mode (less movement)", value=True)
                preprocess_dropdown = gr.Dropdown(
                    label="Preprocessing Method",
                    choices=["full", "crop", "resize"],
                    value="full"
                )
                enhancer_checkbox = gr.Checkbox(label="Use GFPGAN Face Enhancer", value=True)

            generate_btn = gr.Button("Generate Animation")

        with gr.Column():
            video_output = gr.Video(label="Generated Talking Animation")
            message_output = gr.Textbox(label="Status Message")

    generate_btn.click(
        fn=process_inputs,
        inputs=[
            image_input,
            audio_input,
            still_checkbox,
            preprocess_dropdown,
            enhancer_checkbox
        ],
        outputs=[
            video_output,
            message_output
        ]
    )

# LAUNCH GRADIO APP
if __name__ == "__main__":
   demo.queue().launch(share=False)
=======
import os
import gradio as gr
import subprocess
import tempfile
import uuid
from pathlib import Path

# Define paths
SADTALKER_ROOT = os.path.dirname(os.path.abspath(__file__))
INFERENCE_SCRIPT = os.path.join(SADTALKER_ROOT, "inference.py")
RESULT_DIR = os.path.join(SADTALKER_ROOT, "results")
os.makedirs(RESULT_DIR, exist_ok=True)

def generate_talking_face(source_image, driven_audio, still=True, preprocess="full", enhancer="gfpgan"):
    """
    Generate a talking face animation using SadTalker.
    """
    if not os.path.exists(INFERENCE_SCRIPT):
        return None

    session_id = str(uuid.uuid4())
    temp_result_dir = os.path.join(RESULT_DIR, session_id)
    os.makedirs(temp_result_dir, exist_ok=True)

    cmd = [
        "python", INFERENCE_SCRIPT,
        "--driven_audio", driven_audio,
        "--source_image", source_image,
        "--result_dir", temp_result_dir,
        "--preprocess", preprocess
    ]

    if still:
        cmd.append("--still")
    if enhancer:
        cmd.extend(["--enhancer", enhancer])

    print("Running SadTalker command:", " ".join(cmd))

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=SADTALKER_ROOT
        )
        stdout, stderr = process.communicate()

        print("SadTalker Output:\n", stdout.decode())
        print("SadTalker Error:\n", stderr.decode())

        if process.returncode != 0:
            print(f"SadTalker failed with code {process.returncode}")
            return None

        video_files = list(Path(temp_result_dir).glob("*.mp4"))
        if not video_files:
            print("No video file was generated.")
            return None

        return str(video_files[0])

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        return None

def process_inputs(image, audio, use_still, preprocess_method, use_enhancer):
    """Process inputs and generate the talking face animation."""
    if image is None or audio is None:
        return None, "Please upload both an image and an audio file."

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
        image_path = temp_img.name
        image.save(image_path)

    audio_path = audio
    enhancer = "gfpgan" if use_enhancer else None

    try:
        video_path = generate_talking_face(
            image_path,
            audio_path,
            still=use_still,
            preprocess=preprocess_method,
            enhancer=enhancer
        )
        if video_path:
            return video_path, "Animation generated successfully!"
        else:
            return None, "Failed to generate animation. Please check logs."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
    finally:
        if os.path.exists(image_path):
            os.unlink(image_path)

# Build Gradio Interface
with gr.Blocks(title="SadTalker: Talking Face Animation") as demo:
    gr.Markdown("## 🎭 SadTalker: Generate a talking face animation from an image and audio.")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(label="Upload Source Image", type="pil")
            audio_input = gr.Audio(label="Upload Driven Audio", type="filepath")

            with gr.Accordion("Advanced Settings", open=False):
                still_checkbox = gr.Checkbox(label="Use Still Mode (less movement)", value=True)
                preprocess_dropdown = gr.Dropdown(
                    label="Preprocessing Method",
                    choices=["full", "crop", "resize"],
                    value="full"
                )
                enhancer_checkbox = gr.Checkbox(label="Use GFPGAN Face Enhancer", value=True)

            generate_btn = gr.Button("Generate Animation")

        with gr.Column():
            video_output = gr.Video(label="Generated Talking Animation")
            message_output = gr.Textbox(label="Status Message")

    generate_btn.click(
        fn=process_inputs,
        inputs=[
            image_input,
            audio_input,
            still_checkbox,
            preprocess_dropdown,
            enhancer_checkbox
        ],
        outputs=[
            video_output,
            message_output
        ]
    )

# LAUNCH GRADIO APP
if __name__ == "__main__":
   demo.queue().launch(share=False)
>>>>>>> 0450461 (Your commit message here)
