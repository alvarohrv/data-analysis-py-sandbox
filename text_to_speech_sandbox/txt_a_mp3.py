import os
import azure.cognitiveservices.speech as speechsdk

# Lee la clave y la región desde variables de entorno
speech_key = os.environ.get("SPEECH_KEY")
speech_region = os.environ.get("SPEECH_REGION")
#---
if not speech_key or not speech_region:
    raise RuntimeError("Faltan SPEECH_KEY o SPEECH_REGION en las variables de entorno")
#---
# Configuración básica del servicio (objeto SpeechConfig)
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=speech_region
    #endpoint=os.environ.get('ENDPOINT') # Si usas un endpoint personalizado
)
#---
# Configuración de salida de audio (opcional) - aquí no se usa porque guardamos en archivo
# audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) # salida por defecto (altavoces)
# audio_config = speechsdk.audio.AudioOutputConfig(filename="path/to/write/file.wav")
#---
# Formato de salida: MP3 mono, 32 kbit/s, 16 kHz # mas adelante se usa en AudioDataStream
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
)
# Formatos disponibles ver: https://learn.microsoft.com/es-es/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechsynthesisoutputformat?view=azure-python
#---
# Caso 1: solo idioma (voz por defecto de ese idioma)
# speech_config.speech_synthesis_language = "es-ES" (opcional, para síntesis de voz)
# speech_config.speech_recognition_language="en-US" (opcional, para reconocimiento de voz)
# Caso 2: voz concreta (omite speech_synthesis_language si estuviera) (se trabajo de esta manera)
# Voz (puedes cambiarla por otra de la lista de voces neuronales de Azure)
speech_config.speech_synthesis_voice_name = "en-US-AndrewMultilingualNeural"
# caso 3: SSML con <voice name="..."> (tiene prioridad sobre los anteriores)
# NOTA: use speak_ssml_async() en lugar de speak_text_async() si usas SSML
# Ejemplo de SSML (Speech Synthesis Markup Language):
# <speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US">
#   <voice name="en-US-Ava:DragonHDLatestNeural">
#     When you're on the freeway, it's a good idea to use a GPS.
#   </voice>
# </speak>
#--- Formatos de archivo para entrada de texto:
# .xml	Recomendada
# .ssml	Específica
# .txt	Funcional con ssml pero limitado
#---
# <break time="4000ms" />
# <emphasis level="strong">Hola mundo</emphasis>.
# <lang xml:lang="es-ES"> Este texto está en español.</lang>
# <lang xml:lang="en-US"> This text is in English.</lang>
# Hola, <prosody rate="slow">esta es una prueba</prosody> de SSML.





#---
def txt_a_mp3(ruta_txt, ruta_mp3):

    # No se usa entrada por consola, se lee desde archivo
    # print("Enter some text that you want to speak >")
    # text = input()

    # Leer texto del archivo
    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()

    # Sintetizar a memoria (instancia de SpeechSynthesizer sin AudioConfig porque no se usa salida directa)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    #Al usar None para AudioConfig, en lugar de omitirlo como lo hizo en el ejemplo de salida del altavoz anterior, el audio no se reproduce de manera predeterminada en el dispositivo de salida activo actual.
    speech_synthesis_result = speech_synthesizer.speak_text_async(texto).get() # texto en memoria
    # Puede trabajar con este objeto manualmente, o bien puede usar la clase AudioDataStream para administrar la secuencia en memoria.
    # NOTA: use speak_ssml_async() en lugar de speak_text_async() si usas SSML
    #EJEMPLO:
    # ssml_string = open("ssml.xml", "r").read()
    # speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_string).get()
 

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #evento SynthesisCompleted

        # print("Speech synthesized for text [{}]".format(text))
        # print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        # cancellation_details = speech_synthesis_result.cancellation_details

        # Guardar audio en MP3 # Personalización del formato de audio
        stream = speechsdk.AudioDataStream(speech_synthesis_result) # crea flujo de datos de audio en memoria
        stream.save_to_wav_file(ruta_mp3)  # El SDK usa WAV internamente, pero respeta el formato configurado como MP3, anteriormente definido.
        print(f"Generado: {ruta_mp3}")
    # elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    #      cancellation_details = speech_synthesis_result.cancellation_details
    #      print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    else: # cancellation_details.reason == speechsdk.CancellationReason.Error:
        details = speech_synthesis_result.cancellation_details
        print("Error details: {}".format(details.error_details))
        raise RuntimeError(f"Error en síntesis: {details.reason} - {details.error_details}")

if __name__ == "__main__":
    # Cambia estos nombres de archivo según tus necesidades
    entrada = "entrada.txt"
    salida = "salida.mp3"
    txt_a_mp3(entrada, salida)

'''
Si solo configuras speech_config.speech_synthesis_language = "es-ES", usa la voz predeterminada para español de España.​ (no fue el caso)
Si configuras speech_config.speech_synthesis_voice_name = "es-ES-ElviraNeural", entonces esa voz manda y el lenguaje explícito se ignora.​ (fue el caso, porque se configuró la voz en inglés)
Si usas SSML con <voice name="...">, ese <voice> tiene prioridad sobre speech_synthesis_voice_name y sobre speech_synthesis_language.​


Cree una instancia de AudioOutputConfig para escribir automáticamente la salida en un archivo .wav mediante el parámetro de constructor filename:

Python
audio_config = speechsdk.audio.AudioOutputConfig(filename="path/to/write/file.wav")
'''





###//////////////////////
# Configuración para reconocimiento de voz desde micrófono (opcional)
# Sacado de la documentación oficial de Microsoft
'''
def recognize_from_microphone():
     # This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
     # Replace with your own subscription key and endpoint, the endpoint is like : "https://YourServiceRegion.api.cognitive.microsoft.com"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), endpoint=os.environ.get('ENDPOINT'))
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and endpoint values?")

recognize_from_microphone()
'''