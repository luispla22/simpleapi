from flask import Flask, redirect, request, session, url_for
from requests_oauthlib import OAuth2Session

app = Flask(__name__)
app.secret_key = 'una_clave_secreta_muy_segura'

# Debes reemplazar estos valores con tus propios datos de Authentik
AUTHENTIK_CLIENT_ID = 'dwd8ibAbMj2S7hUScpLLzxSgBAfZ7xIuOS5McSZ1'
AUTHENTIK_CLIENT_SECRET = 'oSXDONeOspGtuf3CLsXQfSurWFRXiZKJSXwGOvalG8pypg1YjSkQXxkwshwzxFPsJEaAaffRbcBPN5vHxnFgw6Mah2lCapgrEf87N7GsJ3JGafQuvJ896O1PRsGdEB9G'
AUTHENTIK_REDIRECT_URI = 'https://casaos.taile22a8.ts.net:5000/callback'
AUTHENTIK_AUTHORIZATION_BASE_URL = 'https://casaos.taile22a8.ts.net:5443/application/o/authorize/'
AUTHENTIK_TOKEN_URL = 'https://casaos.taile22a8.ts.net:5443/application/o/token/'

@app.route("/")
def index():
    authentik = OAuth2Session(AUTHENTIK_CLIENT_ID, redirect_uri=AUTHENTIK_REDIRECT_URI)
    authorization_url, state = authentik.authorization_url(AUTHENTIK_AUTHORIZATION_BASE_URL)

    # Guarda el estado en la sesión para usarlo en la callback
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route("/callback", methods=["GET"])
def callback():
    authentik = OAuth2Session(AUTHENTIK_CLIENT_ID, state=session['oauth_state'])
    token = authentik.fetch_token(
        AUTHENTIK_TOKEN_URL,
        client_secret=AUTHENTIK_CLIENT_SECRET,
        authorization_response=request.url
    )

    # Guarda el token en la sesión y redirige al usuario a la página de inicio
    session['oauth_token'] = token

    return redirect(url_for('.index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc', debug=True)


