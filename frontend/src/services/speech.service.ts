import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SpeechService {
  private voices: SpeechSynthesisVoice[] = [];

  updateSpeech(message: any): void {
    this.toggle(message, true);
  }

  setVoices(voices: SpeechSynthesisVoice[]): void {
    this.voices = voices;
  }

  private findVoice(voiceName: string): SpeechSynthesisVoice | null {
    const voice = this.voices.find(v => v.name === voiceName);
    return voice ? voice : null;
  }

  toggle(message: string, startOver = true): void {
    const speech = this.makeRequest(message);
    speechSynthesis.cancel();
    if (startOver) {
      speechSynthesis.speak(speech);
    }
  }

  private makeRequest(message: string) {
    const speech = new SpeechSynthesisUtterance();
    speech.text = message;
    speech.rate = 1;
    speech.pitch = 1;

    const voice = this.findVoice(localStorage.getItem('voice') || '');
    if (voice) {
      speech.voice = voice;
    }
    return speech;
  }
}
