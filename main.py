import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified language
    - Remember the format and the beginning and end of the email, this can design by yourself with tone.
    - If picture is Yes,you need to choose a word in email to fill it in <keywords>: Use markdown syntax when displaying pictures (https://source.unsplash.com/960x640/?<keywords>).

    Here are some examples different Tones:
    - Formal: We went to Taipei for the weekend. We have a lot of things to tell you.
    - Informal: Went to Taipei for the weekend. Lots to tell you.  
    - Funny: So, we went to Taipei for the weekend and let's just say it was a "Tai-peachy" experience. We've got some hilarious tales to share with you!
    - Profession: As part of a business trip, we ventured to Taipei over the weekend. We had a productive time, but also managed to fit in some leisure activities. Allow us to share our experience with you.
    - Dramatic: The trip to Taipei was a rollercoaster of emotions. We laughed, we cried, we almost missed our flight back. You won't believe the stories we have to share.
    
    Here are some examples of words in different languages:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each language:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.
    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and language:
    TONE: {tone}
    LANGUAGE: {language}
    EMAIL: {email}
    PICTURE: {picture}
    
    YOUR {language} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone","language","email","picture"],
    template=template,
)

def load_LLM(openai_api_key):
    llm = OpenAI(temperature=.7,openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Email Assistant",page_icon=":robot:")
st.header("Improve Your Content")

col1,col2 = st.columns(2)

with col1:
    st.markdown("Often people would like to improve their emails, but don't have the skills to do so. \n\n This tool \
                will help you improve your email skills by converting your emails into a more professional format and you can \
                also change different style you want.The most special ability is that it can also create a picture for you, \
                according to your content. This tool is powered by [LangChain](https://langchain.com/) and \
                [OpenAI](https://openai.com) and made by [@LucienLin](https://medium.com/@lucien1999s.pro).")

with col2:
    st.image(image='girl.png', width=500, caption='')

st.markdown("## Enter Your Email To Convert")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2, col3  = st.columns(3)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal' ,'Funny', 'Profession','Dramatic'))
    
with col2:
    option_language = st.selectbox(
        'Which dialect would you like?',
        ('American', 'British'))
    
with col3:
    option_picture = st.selectbox(
        'Do you need picture?',
        ('Yes','No'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Lucia I'm working with Alpha right now"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Email:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="🫣")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, language=option_language, email=email_input, picture = option_picture)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)