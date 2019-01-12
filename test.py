from clarifai.rest import ClarifaiApp

# Create your API key in your account's `Manage your API keys` page:
# https://clarifai.com/developer/account/keys
myApi = '32256d518ae94e9597fe852eb356250a'
app = ClarifaiApp(api_key=myApi)

# You can also create an environment variable called `CLARIFAI_API_KEY`
# and set its value to your API key.
# In this case, the construction of the object requires no `api_key` argument.
