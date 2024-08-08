import streamlit as st
import streamlit.components.v1 as components
import whisper
from candidate_input import record_audio, transcribe_audio
from hr_simulation import generate_hr_response, speak_text
import warnings
import time
from components import camera_component, apply_styles, header, remove_expand, mic_speaker, footer

warnings.filterwarnings("ignore", category=FutureWarning, message=".*torch.load.*weights_only.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*FP16 is not supported on CPU.*")


# Function to run the interview process
def run_interview():

    whisper_model = whisper.load_model("small")

    conversation = [
        {"role": "system", "content": "You are an HR interviewer conducting an interview with a candidate."},
        {"role": "assistant", "content": "Hello, and welcome to Nvidia Corporation! My name is Shimmer, and I'll be conducting your interview today. Could you please tell me a bit about yourself?"}
    ]
    
    print(conversation[-1]['content'])
    speak_text(conversation[-1]['content'])

    question_count = 1
    max_questions = 5

    while question_count <= max_questions:
        # Record audio from the candidate
        record_audio("candidate_response.wav", duration=None)

        # Check if the interview is still ongoing
        if not st.session_state.interview_started:
            break

        # Transcribe the candidate's response
        candidate_transcription = transcribe_audio("candidate_response.wav", whisper_model)
        conversation.append({"role": "user", "content": candidate_transcription})

        # Determine HR response based on question count
        if question_count == max_questions - 1:
            hr_response = "Thank you for your time today. This concludes our interview. Do you have any final questions or comments?"
        elif question_count == max_questions:
            if candidate_transcription.strip():
                hr_response = generate_hr_response(conversation)
                hr_response += " Thank you for your participation. We will review your responses and get back to you soon. Have a great day!"
            else:
                hr_response = "Thank you for your participation. We will review your responses and get back to you soon. Have a great day!"
        else:
            hr_response = generate_hr_response(conversation)

        conversation.append({"role": "assistant", "content": hr_response})
        print(f"\nHR: {hr_response}")
        speak_text(hr_response)

        # End the interview if the candidate says "thank you" or after max questions
        if "thank you" in candidate_transcription.lower():
            st.write("Interview has ended.")
            break

        question_count += 1
        time.sleep(0.1)

    if question_count >= max_questions:
        st.write("Interview has ended. Thank you for participating.")
        st.session_state.interview_started = False
        st.rerun() 

# Page configuration
st.set_page_config(page_title="Virtual Interview Hub", layout="centered")

# Apply custom styles
apply_styles()

# Header and description
header()

# Initialize interview state
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False


# Remove Streamlit's expand button
remove_expand()

# Layout with image and camera component
left_co, cent_co, last_co = st.columns(3)
with left_co:
    st.image("assets/HR.jpg", width=200)
with last_co:
    camera_component()

# Start/Stop Interview button
if st.session_state.interview_started:
    if st.button("Stop Interview"):
        st.session_state.interview_started = False
        st.write("Interview has ended.")
        time.sleep(1)
        st.rerun()  
else:
    if st.button("Start Interview"):
        st.session_state.interview_started = True
        st.rerun()  # Force a rerun to update the UI



# Display the interview running state
if st.session_state.interview_started:
    components.html("""
        <script>
            async function getMedia() {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
                    document.getElementById('audio-stream').srcObject = stream;
                } catch (err) {
                    console.error('Error accessing microphone:', err);
                }
            }
            getMedia();
        </script>
    """, height=0)
    run_interview()

# Microphone and Speaker Settings
mic_speaker()

# Footer
footer()
