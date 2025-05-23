import streamlit_authenticator as stauth

passwords = ['admin123', 'clave123']
hashes = stauth.Hasher(passwords).generate()
for h in hashes:
    print(h)
