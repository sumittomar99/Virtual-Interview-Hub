import streamlit as st
import streamlit.components.v1 as components

def apply_styles():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def camera_component(width="200px", height="315px"):
    camera_html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          .camera-container {{
            position: relative;
            width: {width};
            height: {height};
            border: 1px solid #ddd;
            background-color: white;
            overflow: hidden; /* Ensure that video doesn't overflow the container */
          }}
          video {{
            width: 100%;
            height: 100%;
            object-fit: cover; /* Ensure the video covers the container without distortion */
          }}
        </style>
      </head>
      <body>
        <div class="camera-container">
          <video id="video" autoplay></video>
        </div>
        <script>
          async function startCamera() {{
            try {{
              const stream = await navigator.mediaDevices.getUserMedia({{ video: true }});
              document.getElementById('video').srcObject = stream;
            }} catch (err) {{
              console.error('Error accessing camera:', err);
            }}
          }}
          startCamera();
        </script>
      </body>
    </html>
    """
    # The height parameter in components.html should match the height of the camera-container
    components.html(camera_html, height=int(height[:-2]))

def footer():
    st.markdown('<div class="footer">Developed with ❤️ by Sumit Tomar</div>', unsafe_allow_html=True)

def header():
    st.markdown('<h1 class="main-title">Virtual Interview Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">A modern interface for simulating HR interviews</p>', unsafe_allow_html=True)

def remove_expand():
    st.markdown("""
    <style>
    [data-testid="StyledFullScreenButton"] {
        display: none;
    }   
    </style>
    """, unsafe_allow_html=True)

def mic_speaker():
    components.html("""
    <div>
        <video id="audio-stream" autoplay style="display:none;"></video>
    </div>
    """, height=0)