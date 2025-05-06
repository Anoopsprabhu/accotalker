<<<<<<< HEAD
import os
import streamlit as st
import subprocess
import tempfile
import uuid
from pathlib import Path
from PIL import Image

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

    st.write("Running SadTalker command:", " ".join(cmd))

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=SADTALKER_ROOT
        )
        stdout, stderr = process.communicate()

        st.write("SadTalker Output:\n", stdout.decode())
        st.write("SadTalker Error:\n", stderr.decode())

        if process.returncode != 0:
            st.error(f"SadTalker failed with code {process.returncode}")
            return None

        video_files = list(Path(temp_result_dir).glob("*.mp4"))
        if not video_files:
            st.error("No video file was generated.")
            return None

        return str(video_files[0])

    except FileNotFoundError as fnf_error:
        st.error(f"Error: {fnf_error}")
        return None

def main():
    st.title("🎭 SadTalker: Talking Face Animation")
    st.markdown("Generate a talking face animation from an image and audio.")

    with st.form("talking_face_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            image_file = st.file_uploader("Upload Source Image", type=["png", "jpg", "jpeg"])
            audio_file = st.file_uploader("Upload Driven Audio", type=["wav", "mp3"])
            
            with st.expander("Advanced Settings"):
                still_mode = st.checkbox("Use Still Mode (less movement)", value=True)
                preprocess_method = st.selectbox(
                    "Preprocessing Method",
                    options=["full", "crop", "resize"],
                    index=0
                )
                use_enhancer = st.checkbox("Use GFPGAN Face Enhancer", value=True)
            
        submit_button = st.form_submit_button("Generate Animation")

    if submit_button:
        if image_file is None or audio_file is None:
            st.error("Please upload both an image and an audio file.")
            return

        with st.spinner("Processing..."):
            # Save uploaded files to temp files
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
                img = Image.open(image_file)
                img.save(temp_img.name)
                image_path = temp_img.name

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio.write(audio_file.read())
                audio_path = temp_audio.name

            enhancer = "gfpgan" if use_enhancer else None

            try:
                video_path = generate_talking_face(
                    image_path,
                    audio_path,
                    still=still_mode,
                    preprocess=preprocess_method,
                    enhancer=enhancer
                )
                
                if video_path:
                    st.success("Animation generated successfully!")
                    st.video(video_path)
                else:
                    st.error("Failed to generate animation. Please check logs.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
            finally:
                if os.path.exists(image_path):
                    os.unlink(image_path)
                if os.path.exists(audio_path):
                    os.unlink(audio_path)

if __name__ == "__main__":
=======
import os
import streamlit as st
import subprocess
import tempfile
import uuid
from pathlib import Path
from PIL import Image

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

    st.write("Running SadTalker command:", " ".join(cmd))

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=SADTALKER_ROOT
        )
        stdout, stderr = process.communicate()

        st.write("SadTalker Output:\n", stdout.decode())
        st.write("SadTalker Error:\n", stderr.decode())

        if process.returncode != 0:
            st.error(f"SadTalker failed with code {process.returncode}")
            return None

        video_files = list(Path(temp_result_dir).glob("*.mp4"))
        if not video_files:
            st.error("No video file was generated.")
            return None

        return str(video_files[0])

    except FileNotFoundError as fnf_error:
        st.error(f"Error: {fnf_error}")
        return None

def main():
    st.title("🎭 SadTalker: Talking Face Animation")
    st.markdown("Generate a talking face animation from an image and audio.")

    with st.form("talking_face_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            image_file = st.file_uploader("Upload Source Image", type=["png", "jpg", "jpeg"])
            audio_file = st.file_uploader("Upload Driven Audio", type=["wav", "mp3"])
            
            with st.expander("Advanced Settings"):
                still_mode = st.checkbox("Use Still Mode (less movement)", value=True)
                preprocess_method = st.selectbox(
                    "Preprocessing Method",
                    options=["full", "crop", "resize"],
                    index=0
                )
                use_enhancer = st.checkbox("Use GFPGAN Face Enhancer", value=True)
            
        submit_button = st.form_submit_button("Generate Animation")

    if submit_button:
        if image_file is None or audio_file is None:
            st.error("Please upload both an image and an audio file.")
            return

        with st.spinner("Processing..."):
            # Save uploaded files to temp files
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
                img = Image.open(image_file)
                img.save(temp_img.name)
                image_path = temp_img.name

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio.write(audio_file.read())
                audio_path = temp_audio.name

            enhancer = "gfpgan" if use_enhancer else None

            try:
                video_path = generate_talking_face(
                    image_path,
                    audio_path,
                    still=still_mode,
                    preprocess=preprocess_method,
                    enhancer=enhancer
                )
                
                if video_path:
                    st.success("Animation generated successfully!")
                    st.video(video_path)
                else:
                    st.error("Failed to generate animation. Please check logs.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
            finally:
                if os.path.exists(image_path):
                    os.unlink(image_path)
                if os.path.exists(audio_path):
                    os.unlink(audio_path)

if __name__ == "__main__":
>>>>>>> 0450461 (Your commit message here)
    main()