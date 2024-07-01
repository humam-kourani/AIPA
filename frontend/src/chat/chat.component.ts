import {
  AfterViewChecked,
  Component,
  ElementRef,
  Input,
  NgZone,
  OnDestroy,
  OnInit,
  ViewChild
} from '@angular/core';
import {OpenaiChatService} from "../services/openai-chat.service";
import {NgForOf, NgIf} from "@angular/common";
import {MatButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatProgressBar} from "@angular/material/progress-bar";
import {Router} from "@angular/router";
import {fromEvent, map, Observable, Subscription, tap} from "rxjs";
import {BackendConnectionService} from "../services/backend-connection.service";
import {ErrorHandlingService} from "../error-dialog/error-handling.service";
import {FormsModule} from "@angular/forms";
import {environment} from "../environments/environment";
import {MatTooltip} from "@angular/material/tooltip";
import {VoiceRecognitionService} from "../services/voice-recognition.service";
import {MatRipple} from "@angular/material/core";
import {SpeechService} from "../services/speech.service";


class Message{
  index: number | undefined
  text: string | undefined
  reply: Boolean | undefined
  user: any
}


@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    NgForOf,
    MatButton,
    MatIcon,
    MatProgressBar,
    NgIf,
    FormsModule,
    MatTooltip,
    MatRipple
  ],
  // @ts-ignore
  providers: [],
  templateUrl: './chat.component.html',
  styleUrls: [
    './chat.component.scss',
    "./../../node_modules/bootstrap/dist/css/bootstrap.min.css",
    "./../../node_modules/font-awesome/css/font-awesome.css"
  ]
})

export class ChatComponent implements OnInit, OnDestroy, AfterViewChecked {

  @Input() resetConvo!: Observable<void>;
  private resetConvoSubscription: Subscription | undefined;

  messages: Message[] = [];
  chatInputMessage = '';
  showLoader: boolean = false
  resetSubscription = new Subscription();
  // for disabling the reset of the chat when the selection in the BPMN changes unless "ENABLE_SENDING_SUBMODEL" is set to true
  enableSendingSubmodel: boolean = false;
  @ViewChild('scrollMe') private myScrollContainer: ElementRef | undefined;
  voices$!: Observable<SpeechSynthesisVoice[]>;
  subscription = new Subscription();


  constructor(private openaiChatService: OpenaiChatService,
              private router: Router,
              private ngZone: NgZone,
              private backendConnectionService: BackendConnectionService,
              private errorHandlingService: ErrorHandlingService,
              public voiceRecognitionService : VoiceRecognitionService,
              private speechService: SpeechService) {
    this.voiceRecognitionService.init()

  }

  mouseup() {
    this.voiceRecognitionService.stop()
  }

  mousedown() {
    this.voiceRecognitionService.start()
  }

  ngOnInit(): void {

    this.enableSendingSubmodel = environment.ENABLE_SENDING_SUBMODEL

    document.body.classList.add('nb-theme-corporate');

    this.resetSubscription = this.openaiChatService.resetSubject.subscribe((data)=>{
      this.resetConversation()
    });

    this.resetConvoSubscription = this.resetConvo.subscribe(() => this.resetConversation());

    this.voiceRecognitionService.newVoiceInputMessage.subscribe((data)=>{
      this.chatInputMessage = data
    });

    this.voices$ = fromEvent(speechSynthesis, 'voiceschanged').pipe(
      map(() => speechSynthesis.getVoices().filter((voice) => voice.lang.includes('en'))),
      tap((voices) => this.speechService.setVoices(voices)),
    );
  }

  ngAfterViewChecked() {
    // this.scrollToBottom();
  }

  ngOnDestroy() {
    this.resetSubscription.unsubscribe();
    this.voiceRecognitionService.newVoiceInputMessage.unsubscribe();
  }

  speakMessage(message: string | undefined){
    this.speechService.updateSpeech(message)
  }

  send(message: any) {
    if (message === ''){
      return
    }

    this.showLoader = true

    this.messages.push({
      index: this.messages.length + 1,
      text: message,
      reply: true,
      user: {
        name: 'You',
        avatar: './assets/human.png',
      }
    });
    setTimeout(()=>{
      this.scrollToBottom();
    },10)

    let postDataContent = {
      message: message,
      textualRepresentation: this.openaiChatService.textualRepresentation,
      modelXmlString: this.openaiChatService.modelXmlString,
      modelSvg: this.openaiChatService.modelSvg,
      parameters: {}
    };

    this.backendConnectionService.sendMessage(postDataContent).subscribe({
        next: (data: any) => {
          this.addBotMessageToChatBox(data.response)
          this.showLoader = false
          this.chatInputMessage = ''
        },
        error: error => {
          this.addBotMessageToChatBox('Sorry, there was an error processing your message.')
          this.errorHandlingService.showErrorDialog(error)
          this.showLoader = false
          this.chatInputMessage = ''
        }
    })
  }

  resetConversation() {
    if (this.enableSendingSubmodel){
      this.backendConnectionService.resetConversation().subscribe({
        next: data => {
          if(this.messages.length != 1){
            this.addBotMessageToChatBox('Hello! I am your AI assistant. How may I assist you with the uploaded BPMN model?', false)
          }
        },
        error: error => {
          this.errorHandlingService.showErrorDialog('There was an error while resetting the conversation.')
        }
      })
    }
  }

  addBotMessageToChatBox(message: string, append= true){
    const formattedMessage: Message = new Message()
    formattedMessage.index = this.messages.length + 1,
    formattedMessage.text = message,
    formattedMessage.reply = false,
    formattedMessage.user = {
      name: 'Bot',
      avatar: './assets/robot.png',
    }

    if(append){
      this.messages.push(formattedMessage)
    }
    else{
      this.messages = [formattedMessage]
    }
    setTimeout(()=>{
      this.scrollToBottom();
    },10)
  }

  scrollToBottom(): void {
    try {
      // @ts-ignore
      this.myScrollContainer.nativeElement.scrollTop = this.myScrollContainer.nativeElement.scrollHeight;
    } catch(err) { }
  }

}
