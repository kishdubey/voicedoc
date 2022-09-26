> editing audio as simple as editing a doc. 

voicedoc is a paltform where users can edit audio by editing text. trim audio by deleting words. forgot to say something while recording? no worries! a unique audio profile is created through an ai model that sounds just like you to add those words in.

<img src="https://i.ibb.co/ZWjJSGV/Screenshot-from-2022-09-25-22-00-17.png"/>


## Local Installation & Setup

```sh
git clone https://github.com/kishdubey/voicedoc.git
cd voicedoc
```

```sh
pip3 install -e .
pip3 install -r requirements.txt
cd application
```

```sh
python3 app.py
```
Go to,
```sh
http://localhost:5000/
```
## Demo
![Voicedoc Demo](https://github.com/kishdubey/voicedoc/blob/main/application/static/assets/img/voicedoc-demo.gif)

## Technologies
- Silero STT
- Coqui TTS (YourTTS, https://arxiv.org/abs/2112.02418)
