import {EventEmitter, Injectable} from '@angular/core';

declare var webkitSpeechRecognition: any;

@Injectable({
  providedIn: 'root'
})
export class VoiceRecognitionService {

  isVoiceRecognitionAvailableInBrowser = false
  recognition;
  isStoppedSpeechRecog = true;
  public text = '';
  tempWords: string = '';
  newVoiceInputMessage = new EventEmitter<string>();

  constructor() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window ){
      this.isVoiceRecognitionAvailableInBrowser = true
      this.recognition = new webkitSpeechRecognition()
    }
  }

  init() {
    if(this.isVoiceRecognitionAvailableInBrowser){
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';

      this.recognition.addEventListener('result', (e: any) => {
        // @ts-ignore
        const transcript = Array.from(e.results)
          .map((result: any) => result[0])
          .map((result) => result.transcript)
          .join('');
        this.tempWords = transcript;
        console.log(transcript);
      });
    }
  }

  start() {
    if (this.isStoppedSpeechRecog){
      this.isStoppedSpeechRecog = false;
      this.recognition.start();
      console.log("Speech recognition started")
      this.recognition.addEventListener('end', (condition: any) => {
        this.wordConcat()
      });
    }
  }

  stop() {
    if(!this.isStoppedSpeechRecog){
      this.isStoppedSpeechRecog = true;
      this.wordConcat()
      this.recognition.stop();
      console.log("End speech recognition")
    }
  }

  wordConcat() {
    if (this.tempWords != ''){
      this.text = this.tempWords;
      this.newVoiceInputMessage.next(this.text)
      this.tempWords = '';
    }
  }
}
