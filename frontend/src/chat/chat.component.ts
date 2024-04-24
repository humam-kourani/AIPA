import {Component, importProvidersFrom, NgZone, ViewEncapsulation} from '@angular/core';
import {OpenaiChatService} from "../services/openai-chat.service";
import {NbChatModule, NbLayoutModule, NbThemeModule} from "@nebular/theme";
import {NgForOf, NgIf} from "@angular/common";
import {MatButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatProgressBar} from "@angular/material/progress-bar";
import {Router} from "@angular/router";
import {Subscription} from "rxjs";
import {BackendConnectionService} from "../services/backend-connection.service";
import {ErrorHandlingService} from "../error-dialog/error-handling.service";

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    NbThemeModule,
    NbChatModule,
    NbLayoutModule,
    NgForOf,
    MatButton,
    MatIcon,
    MatProgressBar,
    NgIf,
  ],
  // @ts-ignore
  providers: [NbThemeModule.forRoot({name: 'corporate'}).providers],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss',
  // encapsulation: ViewEncapsulation.Emulated
})

export class ChatComponent {

  messages: any[] = [];
  showLoader: boolean = false
  resetSubscription = new Subscription();

  constructor(private openaiChatService: OpenaiChatService,
              private router: Router,
              private ngZone: NgZone,
              private backendConnectionService: BackendConnectionService,
              private errorHandlingService: ErrorHandlingService) {

  }

  ngOnInit(): void {
    document.body.classList.add('nb-theme-corporate');
    this.resetSubscription = this.openaiChatService.resetSubject.subscribe((data)=>{
      this.resetConversation()
    });
  }

  ngOnDestroy() {
    this.resetSubscription.unsubscribe();
  }


  sendMessage(event: any) {
    this.showLoader = true

    this.messages.push({
      text: event.message,
      date: new Date(),
      reply: true,
      user: {
        name: 'You',
        avatar: './assets/human.png',
      },
    });

    let postDataContent = {
      message: event.message,
      textualRepresentation: this.openaiChatService.textualRepresentation,
      modelXmlString: this.openaiChatService.modelXmlString,
      modelSvg: this.openaiChatService.modelSvg,
      parameters: {}
    };

    this.backendConnectionService.sendMessage(postDataContent).subscribe({
        next: (data: any) => {
          this.addBotMessageToChatBox(data.response)
          this.showLoader = false
        },
        error: error => {
          this.addBotMessageToChatBox('Sorry, there was an error processing your message.')
          this.errorHandlingService.showErrorDialog(error)
          this.showLoader = false
        }
    })
  }

  resetConversation() {
    this.backendConnectionService.resetConversation().subscribe({
        next: data => {
          if(this.messages.length != 1){
            this.addBotMessageToChatBox('Hello! I am your AI assistant. How may I assist you with the uploaded BPMN model?', false)
          }
        },
        error: error => {
          this.errorHandlingService.showErrorDialog('There was an error resetting the conversation.')
        }
    })

  }

  addBotMessageToChatBox(message: string, append= true){
    const formattedMessage =  {
      text: message,
      reply: false,
      user: {
        name: 'Bot',
        avatar: './assets/robot.png',
      }
    }
    if(append){
      this.messages.push(formattedMessage)
    }
    else{
      this.messages = [formattedMessage]
    }
  }


  // reset_button_listener() {
  // var resetButton = document.getElementById("reset_button");
  // if (resetButton) {
  //   resetButton.addEventListener("click", function () {
  //     reset_conversation();
  //   });
  // }

  reset_conversation() {
    // axios
    //   .post("/reset_conversation")
    //   .then(function (response) {
    //     console.log(response.data.success);
    //     var chatBox = document.getElementById("chat-box");
    //     // chatBox.innerHTML = "";
    //
    //     $('#chat-history').empty()
    //     sendInitialSystemMessage();
    //   })
    //   .catch(function (error) {
    //     console.error(error);
    //   });
  }

}
