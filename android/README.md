# Ollama Studio Android

Primeiro shell Android instalável do projeto.

## Builds
- Debug: `./gradlew assembleDebug`
- Release: `./gradlew assembleRelease`

O release usa assinatura quando estas variáveis existem:
`ANDROID_KEYSTORE_PATH`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD`.

A chave privada nunca deve entrar no repositório.
