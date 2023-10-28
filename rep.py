import os
import openai
import streamlit as st
# Load your API key from an environment variable or secret management service
openai.api_key = os.environ['OPENAI_API_KEY']
st.title('Customer Retention Email Generation')
'\n'
#st.header('Customer Profile')
#gender = st.radio(
#    "Gender of the customer",
#    ('Male', 'Female', 'Undisclosed'))
#if gender=='Male':
#	pronoun = 'him'
#	tag=' male '
#elif gender=='Female':
#	pronoun = 'her'
#	tag=' female '
#else:
#	pronoun='them'
#	tag=''
spend = st.number_input('How much did the customer spend in last 6 months',value=3000)
prob = st.slider('How likely is the customer to churn?', 0, 100, 90)
discount = st.slider('What discount are we willing to offer?', 0, 100, 5)
text = st.text_area('Enter a template email.',value='''Subject line: Thanks for being a loyal customer! Here's [discount]% off your next purchase.

Copy:

Hey there,

We wanted to reach out and thank you for being a loyal customer. We love having you around, and we're always working hard to make sure your experience with us is the best it can be.

To show our appreciation, we'd like to offer you [discount]% off your next order with [company name]. Just enter the coupon code "[code]" at checkout, and we'll take care of the rest.

Thanks again for being awesome!''')

if st.button('Generate Email'):
	#prompt= '''Acustomer has spent {}$ on a website in last 6 months. Our system predicts that the customer is about to churn with {}% probability. Write a 120 word email to {} mentioning the {}% discount on selective items on website. Make {} feel like a valued customer and stop him from churning.Do not let {} know that we predicted they will churn.'''.format(tag,prob,pronoun,discount,pronoun,pronoun)
	prompt = '''Rephrase the follwoing email in 150 words.Discount is {}. \n'''.format(discount)+text+'Re-write:\n'
	response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0.8, max_tokens=200)
	mail = response['choices'][0]['text']
	st.header('Email')
	st.write(mail)

